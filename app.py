# app.py
from fastapi import FastAPI
from my_celery import celery_app
from tasks import send_email_task
import smtplib
from email.message import EmailMessage
import logging
import urllib.parse

logger = logging.getLogger(__name__)
logging.basicConfig(filename='/var/log/messaging_system.log', level=logging.INFO)

app = FastAPI()

# @app.get('/sendmail')
# def sendmail(recipient: str):
#     try:
#         # Decode the recipient URL-encoded string
#         recipient_email = urllib.parse.unquote(recipient)
#         recipient_email = recipient

#          # Example URL: /sendmail?recipient=tosinghdarey2100%40gmail.com
#         if recipient_email.startswith('mailto:'):
#             recipient_email = recipient_email.replace('mailto:', '')
#         else:
#             recipient_email = recipient_email

#         # Validate if recipient_email is a valid email format (optional)
#         import re
#         if not re.match(r"[^@]+@[^@]+\.[^@]+", recipient_email):
#             return {'error': 'Invalid recipient format.'}

#          # Queue email task in Celery
#         send_email_task.delay(recipient_email, "I sent you an email regarding my rabbit mq and celery project")

#         return {'message': 'Email sending task queued.'}

#     except Exception as e:
#         logger.error(f"Failed to queue email task: {str(e)}")
#         return {'error': 'Failed to queue email task.'}



# @app.get('/talktome')
# def talktome():
#     try:
#         # Log current time
#         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         logger.info(f"Talk to me at {current_time}")
#         return {'message': f"Logged message at {current_time}"}

#     except Exception as e:
#         logger.error(f"Failed to log message: {str(e)}")
#         return {'error': 'Failed to log message.'}


# Define the main endpoint
@app.get('/')
async def handle_request(request: Request):
    try:
        sendmail_param = request.query_params.get('sendmail')
        talktome_param = request.query_params.get('talktome')

        if sendmail_param:
            recipient_email = urllib.parse.unquote(sendmail_param)
            if recipient_email.startswith('mailto:'):
                recipient_email = recipient_email.replace('mailto:', '')

            # Validate email format
            import re
            if not re.match(r"[^@]+@[^@]+\.[^@]+", recipient_email):
                return {'error': 'Invalid recipient format.'}

            # Queue email task in Celery
            send_email_task.delay(recipient_email, "I sent you an email regarding my RabbitMQ and Celery project")
            return {'message': 'Email sending task queued.'}

        elif talktome_param is not None:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Talk to me at {current_time}")
            return {'message': f"Logged message at {current_time}"}

        else:
            return {'error': 'Invalid parameters.'}

    except Exception as e:
        logger.error(f"Failed to process request: {str(e)}")
        return {'error': 'Failed to process request.'}
