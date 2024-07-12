from flask import Flask, request, jsonify
from celery import Celery
import smtplib
from datetime import datetime
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Messaging System API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@celery.task
def send_email(email):
    server = smtplib.SMTP('localhost')
    server.sendmail('from@example.com', email, 'This is a test email.')
    server.quit()

@app.route('/api', methods=['GET'])
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    if sendmail:
        send_email.delay(sendmail)
        return jsonify({"message": f"Email will be sent to {sendmail}"})

    if talktome:
        with open('/var/log/messaging_system.log', 'a') as f:
            f.write(f"{datetime.now()}\n")
        return jsonify({"message": "Logged current time."})

    return jsonify({"message": "Specify either sendmail or talktome parameter."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
