import csv
import datetime

from django.core.management.base import BaseCommand
from dataentry.models import Student
import datetime


# class Command(BaseCommand):
#     help = 'Export data from Student model to csv file'
#
#     def handle(self, *args, **kwargs):
#         # fetch data from the database
#         student = Student.objects.all()
#
#         # generate the timestamp of current date and time
#         timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
#         # define the csv file name/path
#         file_path = f"exported_students_data_{timestamp}.csv"
#
#         # open the file and write the
#         with open(file_path, 'w', newline='') as file:
#             writer = csv.writer(file)
#
#             #write the csv header
#             writer.writerow(["Roll_no", "Name", "Age"])
#
#             #write data rows
#             for student in student:
#                 writer.writerow([student.roll_no, student.name, student.age])
#         self.stdout.write(self.style.SUCCESS('Data exported successfully!'))


##########################################################################################
##########################################################################################
##########################################################################################





# Export the data from any model or any table
# Parser will allow us to write the argument with the command

from django.apps import apps

# proposed command = python manage.py exportdata model_name
class Command(BaseCommand):
    help = "Export data from the database to a csv file"

    def add_arguments(self, parser):
        parser.add_argument("model_name", type=str, help="Model name")

    def handle(self, *args, **kwargs):
        model_name = kwargs["model_name"].capitalize()
        #search through all the installed apps for the model
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break # stop executing once the model is found
            except LookupError:
                pass

        if not model:
            self.stdout.write(f"Model {model_name} could not found")
            return

        # fetch the data from the database
        data = model.objects.all()

        #generate the timestamp of current date and time
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        #define the csv file name/path
        file_path = f"exported_{model_name}_data_{timestamp}.csv"

        #open the csv file and write the data
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)

            # write the csv header
            # we want to print the field names of the model that we are trying to export
            writer.writerow([field.name for field in model._meta.fields])

            # write data rows
            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields])
        self.stdout.write(self.style.SUCCESS("Successfully exported data"))