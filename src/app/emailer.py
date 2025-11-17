import os
import requests
from .config import FROM_EMAIL, FROM_NAME

BREVO_API_KEY = os.getenv("BREVO_API_KEY")

def send_thank_you_email(to_email: str, to_name: str | None):
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "sender": {"email": FROM_EMAIL, "name": FROM_NAME},
        "to": [{"email": to_email, "name": to_name or ""}],
        "subject": "You're on the waitlist!",
        "htmlContent": f"<p>Hi {to_name or ''},</p><p>Thanks for joining the waitlist. You're in.</p><p>- The {FROM_NAME} Team</p>"
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending email via Brevo API: {e}")