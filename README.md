# 🎣 AI-Powered Phishing Email Detector

<p align="center">

  🚀 **LIVE PROJECT DEMO**
  <br>
  <a href="https://phishing-email-detector1.streamlit.app/">
    🌐 Open AI Phishing Email Detector
  </a>

  <br><br>

  <a href="https://github.com/Ameenkhalander/AI-Phishing-Email-Detector">
    📂 View Source Code on GitHub
  </a>

</p>



A Python machine-learning + NLP project that classifies emails as **phishing** or **legitimate**.

- Cleans and preprocesses raw email text (lowercase, HTML/URL/email-address handling, punctuation removal)
- Extracts text features with **TF-IDF** (unigrams + bigrams)
- Trains and compares **Logistic Regression, Naive Bayes and Random Forest**, then saves the best one
- Interactive **Streamlit** web app with confidence score and red-flag signals

## Project structure

```
phishing-email-detector/
├── app.py                  # Streamlit web app
├── train.py                # Train + evaluate + save model
├── requirements.txt
├── src/preprocess.py       # Text cleaning + red-flag signals
├── data/
│   ├── emails.csv          # Small synthetic sample dataset (columns: text, label)
│   └── generate_sample_data.py
├── models/                 # Trained model is saved here
└── .streamlit/config.toml
```

## Run in VS Code

1. Open the `phishing-email-detector` folder in VS Code (File → Open Folder).
2. Open a terminal (Ctrl + `) and create a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS / Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Train the model:
   ```bash
   python train.py
   ```
5. Launch the app:
   ```bash
   streamlit run app.py
   ```

## IMPORTANT: use a real dataset

The bundled `data/emails.csv` is **synthetic** (template-generated), so it scores ~100% and
is only there so the project runs immediately. For real results and for your resume/viva,
download a real dataset, e.g. the Kaggle **"Phishing Email Dataset"** (`Phishing_Email.csv`,
columns `Email Text` / `Email Type`), put it in `data/`, and run:

```bash
python train.py --data data/Phishing_Email.csv
```

`train.py` auto-detects common column names (`Email Text`/`Email Type`, `text`/`label`, etc.).
Expect realistic accuracy around 95–98% on real data.

## Deploy on Streamlit Community Cloud

1. Create a GitHub repo and push this folder (the `.venv` folder is already git-ignored):
   ```bash
   git init
   git add .
   git commit -m "Phishing email detector"
   git branch -M main
   git remote add origin https://github.com/<your-username>/phishing-email-detector.git
   git push -u origin main
   ```
2. Go to https://share.streamlit.io → **New app** → select your repo, branch `main`, main file `app.py` → **Deploy**.
3. If you trained on a real dataset, keep that CSV in the repo (or commit `models/phishing_model.joblib`).
   If the model file is missing, the app trains itself on `data/emails.csv` at first launch.
   Note: GitHub rejects files over 100 MB, so use a smaller sample of very large datasets.

## Tech stack

Python · pandas · scikit-learn · TF-IDF · Streamlit · joblib
