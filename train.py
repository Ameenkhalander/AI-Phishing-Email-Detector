"""Train and compare phishing-email classifiers, then save the best one.

Usage:
    python train.py                              # uses data/emails.csv
    python train.py --data data/Phishing_Email.csv
"""
import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from src.preprocess import clean_text

MODEL_DIR = Path("models")
TEXT_COLS = ["text", "Email Text", "email_text", "body", "Body", "message", "Message", "email"]
LABEL_COLS = ["label", "Email Type", "Label", "class", "Class", "type", "Type", "target"]
PHISH_WORDS = {"phishing", "phishing email", "spam", "1", "malicious", "fraud"}


def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    text_col = next((c for c in TEXT_COLS if c in df.columns), None)
    label_col = next((c for c in LABEL_COLS if c in df.columns), None)
    if text_col is None or label_col is None:
        raise SystemExit(
            f"Could not find text/label columns. Found: {list(df.columns)}. "
            f"Rename them to 'text' and 'label'."
        )
    df = df[[text_col, label_col]].dropna()
    df.columns = ["text", "label"]
    df["label"] = df["label"].astype(str).str.strip().str.lower().map(lambda v: 1 if v in PHISH_WORDS else 0)
    return df


def main(data_path: str) -> None:
    df = load_dataset(data_path)
    print(f"Loaded {len(df)} emails  |  phishing: {df.label.sum()}  legitimate: {(df.label == 0).sum()}")

    print("Cleaning text...")
    df["clean"] = df["text"].map(clean_text)
    df = df[df["clean"].str.len() > 0]

    X_train, X_test, y_train, y_test = train_test_split(
        df["clean"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )

    candidates = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "Naive Bayes": MultinomialNB(),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
    }

    results, best_name, best_pipe, best_f1 = {}, None, None, -1.0
    for name, clf in candidates.items():
        pipe = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=20000,
                                      stop_words="english", sublinear_tf=True)),
            ("clf", clf),
        ])
        pipe.fit(X_train, y_train)
        preds = pipe.predict(X_test)
        acc, f1 = accuracy_score(y_test, preds), f1_score(y_test, preds)
        results[name] = {"accuracy": round(acc, 4), "f1": round(f1, 4)}
        print(f"  {name:<20} accuracy={acc:.4f}  f1={f1:.4f}")
        if f1 > best_f1:
            best_name, best_pipe, best_f1 = name, pipe, f1

    print(f"\nBest model: {best_name}")
    preds = best_pipe.predict(X_test)
    print(classification_report(y_test, preds, target_names=["legitimate", "phishing"]))
    print("Confusion matrix:\n", confusion_matrix(y_test, preds))

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(best_pipe, MODEL_DIR / "phishing_model.joblib")
    (MODEL_DIR / "metrics.json").write_text(json.dumps({"best_model": best_name, "results": results,
                                                        "trained_on": len(df)}, indent=2))
    print(f"\nSaved model to {MODEL_DIR / 'phishing_model.joblib'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/emails.csv", help="CSV with text + label columns")
    main(ap.parse_args().data)
