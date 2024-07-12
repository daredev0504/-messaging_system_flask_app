# tasks.py

from celery import shared_task
import smtplib
from email.message import EmailMessage
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='/var/log/messaging_system.log', level=logging.INFO)


@shared_task
def send_email_task(recipient_email, message):
    try:
        # SMTP server configuration (adjust as per your SMTP server)
        smtp_server = 'smtp.yourserver.com'
        smtp_port = 587
        smtp_user = 'your_smtp_username'
        smtp_password = 'your_smtp_password'

        # Compose email message
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = 'Subject'
        msg['From'] = smtp_user
        msg['To'] = recipient_email

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        logger.info(f"Email sent to {recipient_email}")

    except Exception as e:
        logger.error(f"Failed to send email to {recipient_email}: {str(e)}")
