# tasks.py

from Celery import celery
import smtplib
from email.message import EmailMessage
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='/var/log/messaging_system.log', level=logging.INFO)


@celery.task
def send_email_task(recipient_email, message):
    try:
        # SMTP server configuration (adjust as per your SMTP server)
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = 'petoski.ade@gmail.com'
        smtp_password = 'kdqrxllljmvvxcvh'

        # Compose email message
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = 'Messaging using RabbitMQ and Celery'
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
