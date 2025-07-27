import os
from flask_mail import Message


def send_email(to, subject, body):
    from backend.app import mail
    # Format sender name with email
    sender_name = "MoringaPair"
    sender_email = os.getenv("MAIL_USERNAME")
    sender = f"{sender_name} <{sender_email}>"

    msg = Message(
        subject=subject,
        sender=sender, 
        recipients=[to],
        body=body
    )
    try:
        mail.send(msg)
        print(f"✅ Email sent to {to}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
