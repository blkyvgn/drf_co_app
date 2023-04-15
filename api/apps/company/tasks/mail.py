from api.celery import app
from api.vendors.helpers.mail import sender

@app.task 
def send_email_celery_task(user_email, mail_body):
    sender(user_email, mail_body['subject'], mail_body['message'])