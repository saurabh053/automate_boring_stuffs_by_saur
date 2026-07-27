
from awd_main.celery import app
import time
from django.core.management import call_command
from .utils import send_email_notification, generate_csv_file
from django.conf import settings

@app.task
def celery_test_task():
    time.sleep(10)
    # send an email
    mail_subject = "Test Subject"
    message = "This is a test email"
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email)
    return "Task executed successfully"


@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)

    # Agar import ke time koi error aaye to usse raise kar do.
    except Exception as e:
        raise e
    # notify the user by email
    mail_subject = "Import Data Completed"
    message = "Your data import has been successfully completed"
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email)
    return "Data imported successfully"

@app.task
def export_data_task(model_name):
    try:
        call_command('exportdata', model_name)
    except Exception as e:
        raise e
    file_path = generate_csv_file(model_name)
    print(file_path)
    # Send email with the attachment
    mail_subject = "Export Data Successfu"
    message = "Your export data is successfully completed"
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email, attachment=file_path)
    return "Export Data task executed successfully."

