import os
import requests
from .config import FROM_EMAIL, FROM_NAME

BREVO_API_KEY = os.getenv("BREVO_API_KEY")

TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), "templates", "email-template", "index.html"
)

def load_template(name: str | None):
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    html = html.replace("{name}", name or "")
    return html

def send_thank_you_email(to_email: str, to_name: str | None):
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }
    html_content = load_template(to_name)
    data = {
        "sender": {"email": FROM_EMAIL, "name": FROM_NAME},
        "to": [{"email": to_email, "name": to_name or ""}],
        "subject": "You're on the waitlist!",
        "htmlContent": html_content
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending email via Brevo API: {e}")