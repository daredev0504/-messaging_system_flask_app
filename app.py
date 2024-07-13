# app.py
from fastapi import FastAPI, Request, Query
from my_celery import celery_app
from tasks import send_email_task
import smtplib
from datetime import datetime
from email.message import EmailMessage
import logging
import urllib.parse

logger = logging.getLogger(__name__)
logging.basicConfig(filename='/var/log/messaging_system.log', level=logging.INFO)

app = FastAPI()

# Define the main endpoint
@app.get('/')
async def handle_request(sendmail: str = Query(None, description="Email address to send mail"), 
                         talktome: bool = Query(False, description="Log the current time")):
    try:
        if sendmail:
            recipient_email = urllib.parse.unquote(sendmail)
            if recipient_email.startswith('mailto:'):
                recipient_email = recipient_email.replace('mailto:', '')

            # Validate email format
            import re
            if not re.match(r"[^@]+@[^@]+\.[^@]+", recipient_email):
                return {'error': 'Invalid recipient format.'}

            # Queue email task in Celery
            send_email_task.delay(recipient_email, "I sent you an email regarding my RabbitMQ and Celery project")
            return {'message': 'Email sending task queued.'}

        elif talktome:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Talk to me at {current_time}")
            return {'message': f"Logged message at {current_time}"}

        else:
            return {'error': 'Invalid parameters.'}

    except Exception as e:
        logger.error(f"Failed to process request: {str(e)}")
        return {'error': 'Failed to process request.'}