# app.py

from fastapi import FastAPI
from my_celery import celery_app
from tasks import send_email_task
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='/var/log/messaging_system.log', level=logging.INFO)

app = FastAPI()

@app.get('/sendmail')
def sendmail(recipient: str):
    try:
        # Example URL: /sendmail?recipient=mailto:destiny@destinedcodes.com
        if recipient.startswith('mailto:'):
            recipient_email = recipient.replace('mailto:', '')

            # Queue email task in Celery
            send_email_task.delay(recipient_email, "I sent you an email regarding my rabbit mq and celery project")

            return {'message': 'Email sending task queued.'}
        else:
            return {'error': 'Invalid recipient format.'}

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
