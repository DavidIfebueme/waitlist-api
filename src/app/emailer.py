import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD, FROM_EMAIL, FROM_NAME

def send_thank_you_email(to_email: str, to_name: str | None):
    msg = MIMEMultipart()
    msg['Subject'] = "You're on the waitlist!"
    msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg['To'] = to_email

    html_content = f"""
    <p>Hi {to_name or ""},</p>
    <p>Thanks for joining the waitlist. You're in.</p>
    <p>- The {FROM_NAME} Team</p>
    """

    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {e}")