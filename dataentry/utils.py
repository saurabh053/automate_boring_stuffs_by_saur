# we define helper function here
from django.apps import apps


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
