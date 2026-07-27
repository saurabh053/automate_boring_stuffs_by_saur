# we define helper function here
import csv
from django.core.mail import EmailMessage
from django.conf import settings
from django.apps import apps
from django.core.management.base import CommandError
from django.db import DataError


def get_all_custom_models():
    # List of Django's built-in models that we don't want to include.
    # These models are automatically created by Django for authentication,
    # sessions, permissions, admin logs, etc.
    default_models = [
        'ContentType',
        'Session',
        'LogEntry',
        'Group',
        'Permission',
        'User',
        'Upload'
    ]

    # Create an empty list to store the names of custom models.
    custom_models = []

    # apps.get_models() returns all models registered in the Django project,
    # including both built-in Django models and our own application models.
    for model in apps.get_models():

        # Check whether the current model is NOT one of Django's default models.
        # model.__name__ gives only the class name of the model
        # (e.g., "Property", "Customer", "Booking").
        if model.__name__ not in default_models:

            # If it's a custom model, add its name to the list.
            custom_models.append(model.__name__)

    # Return the list containing only custom model names.
    return custom_models



def check_csv_errors(file_path, model_name):
    # Initially model variable ko None assign kar rahe hain.
    model = None

    # Installed apps ke upar loop chala rahe hain.
    for app_config in apps.get_app_configs():

        try:

            # Current app ke andar required model search kar rahe hain.
            model = apps.get_model(

                # Current app ka label pass kar rahe hain.
                app_config.label,

                # User dwara diya gaya model name pass kar rahe hain.
                model_name
            )

            # Agar model mil gaya to loop yahin stop kar do.
            break

        except LookupError:

            # Agar current app me model nahi mila to next app check karo.
            continue

    # Agar model abhi bhi None hai to iska matlab model nahi mila.
    if not model:
        # User ko proper error message dikhane ke liye CommandError raise kar rahe hain.
        raise CommandError(

            # Error message dynamically model name ke saath display hoga.
            f'Model "{model_name}" not found in any app.'
        )
        # Model ke saare field names retrieve kar rahe hain.
        # "id" field ko ignore kar rahe hain kyunki database automatically generate karta hai.
    model_fields = [
            field.name
            for field in model._meta.fields
            if field.name != "id"
        ]

    try:
        # CSV file ko read mode me open kar rahe hain.
        with open(file_path, 'r') as file:

            # CSV file ko dictionary format me read karne ke liye DictReader use kar rahe hain.
            reader = csv.DictReader(file)

            # CSV file ke header names retrieve kar rahe hain.
            csv_header = reader.fieldnames

            # Check kar rahe hain ki CSV ke headers aur model ke fields match karte hain ya nahi.
            if csv_header != model_fields:
                # Agar match nahi karte to DataError raise kar do.
                raise DataError(
                    f"CSV file does not match with the {model_name} table fields"
                )
    except Exception as e:
        raise str(e)
    return model
def check_csv_errors(file_path, model_name):
    model = None

    for app_config in apps.get_app_configs():
        try:
            model = apps.get_model(
                app_config.label,
                model_name
            )
            break

        except LookupError:
            continue

    if not model:
        raise CommandError(
            f'Model "{model_name}" not found in any app.'
        )

    model_fields = [
        field.name
        for field in model._meta.fields
        if field.name != "id"
    ]

    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

            if csv_header != model_fields:
                raise DataError(
                    f"CSV file does not match with the {model_name} table fields"
                )
    except Exception as e:
        raise e

    return model

def send_email_notification(mail_subject, message, to_email):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        mail.send()
    except Exception as e:
        raise e