# app.py
from celery import Celery
from fastapi import FastAPI
#from my_celery import celery_app
#from tasks import send_email_task
import smtplib
from email.message import EmailMessage
import logging
import urllib.parse

logger = logging.getLogger(__name__)
logging.basicConfig(filename='/var/log/messaging_system.log', level=logging.INFO)

app = FastAPI()

# Broker URL format: 'amqp://username:password@host:port/virtual_host'
broker_url = 'amqp://tosingh:peranofo54@172.161.146.165:5672/rabbit'

# Create Celery instance
celery_app = Celery(app.name, broker=broker_url)

@celery_app.task
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


@app.get('/sendmail')
def sendmail(recipient: str):
    try:
        # Decode the recipient URL-encoded string
        recipient_email = urllib.parse.unquote(recipient)
        recipient_email = recipient

         # Example URL: /sendmail?recipient=tosinghdarey2100%40gmail.com
        if recipient_email.startswith('mailto:'):
            recipient_email = recipient_email.replace('mailto:', '')
        else:
            recipient_email = recipient_email

        # Validate if recipient_email is a valid email format (optional)
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", recipient_email):
            return {'error': 'Invalid recipient format.'}

         # Queue email task in Celery
        send_email_task.delay(recipient_email, "I sent you an email regarding my rabbit mq and celery project")

        return {'message': 'Email sending task queued.'}

    except Exception as e:
        logger.error(f"Failed to queue email task: {str(e)}")
        return {'error': 'Failed to queue email task.'}



@app.get('/talktome')
def talktome():
    try:
        # Log current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Talk to me at {current_time}")
        return {'message': f"Logged message at {current_time}"}

    except Exception as e:
        logger.error(f"Failed to log message: {str(e)}")
        return {'error': 'Failed to log message.'}
