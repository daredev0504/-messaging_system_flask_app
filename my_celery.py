from my_celery import Celery

# Broker URL format: 'amqp://username:password@host:port/virtual_host'
broker_url = 'amqp://172.161.146.165/'

# Create Celery instance
celery_app = Celery('tasks', broker=broker_url)

# Optional configuration
celery_app.conf.update(
    result_backend='rpc://',
    task_serializer='json',
    accept_content=['json'],  # Ignore other content types
    timezone='UTC',
)
