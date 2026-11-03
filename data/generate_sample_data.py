"""Generates a small synthetic sample dataset (data/emails.csv) so the project
runs out of the box. Replace it with a real dataset for real-world accuracy."""
import csv
import random
from pathlib import Path

random.seed(42)

brands = ["PayPal", "Amazon", "Netflix", "Microsoft", "Apple", "HDFC Bank", "SBI", "Google", "Facebook", "DHL"]
bad_links = ["http://secure-login-verify.com/account", "http://bit.ly/3xYz-update", "http://account-check.net/confirm",
             "www.verify-now-support.info/login", "http://192.168.10.5/secure/login", "http://free-prize-claim.biz/win"]

phish_templates = [
    "URGENT: Your {b} account has been suspended. Verify your password immediately at {l} or it will be permanently closed.",
    "Dear customer, we detected unusual activity on your {b} account. Click here to confirm your identity: {l}",
    "Congratulations! You are the lucky winner of a ${n} {b} gift card. Claim your prize now: {l}",
    "Security alert: your {b} password will expire in 24 hours. Update your login details now {l}",
    "Your payment of ${n} to {b} failed. Update your billing information immediately to avoid service interruption {l}",
    "FINAL NOTICE: Your {b} account is limited. Confirm your bank details here {l} to restore access.",
    "Hello, you have a pending refund of ${n} from {b}. Submit your card number and PIN at {l} to receive it.",
    "Action required!!! Someone tried to sign in to your {b} account. Verify now: {l}",
    "Dear user, your mailbox is full. Click {l} and enter your email password to increase storage.",
    "{b} Support: your account will be deleted in 48 hours unless you verify your information at {l}",
]

legit_templates = [
    "Hi team, attaching the minutes from today's project meeting. Please review the action items before Friday.",
    "Your {b} order #{n} has shipped and will arrive on Thursday. You can track it from the Orders page in your account.",
    "Reminder: the quarterly review is scheduled for Monday at 10 AM in the conference room. Please bring your reports.",
    "Thanks for your help yesterday! Let's catch up for lunch next week. Let me know which day works for you.",
    "Hi, here is the invoice for last month's services as discussed. Let me know if you have any questions.",
    "Your monthly statement from {b} is now available. Log in through the official app to view it.",
    "Hello professor, I have attached my assignment on computer networks. Kindly let me know if any changes are required.",
    "Meeting rescheduled to Wednesday 3 PM. The agenda is the same. See you all then.",
    "Weekly newsletter: new articles on cloud computing, networking basics and Python tips are now live on the blog.",
    "Happy birthday! Hope you have a wonderful day. We are planning a small get-together this weekend.",
    "Please find the lecture notes for the data structures course attached. The next class is on Tuesday.",
    "Your {b} subscription renewed successfully for ${n}. No action is required. Thank you for being with us.",
]

rows = []
for _ in range(400):
    t = random.choice(phish_templates)
    rows.append((t.format(b=random.choice(brands), l=random.choice(bad_links), n=random.randint(50, 5000)), "phishing"))
for _ in range(400):
    t = random.choice(legit_templates)
    rows.append((t.format(b=random.choice(brands), n=random.randint(1000, 99999)), "legitimate"))

random.shuffle(rows)
out = Path(__file__).parent / "emails.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["text", "label"])
    w.writerows(rows)
print(f"Wrote {len(rows)} rows to {out}")
