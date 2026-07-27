import csv
import datetime
from dataentry.utils import generate_csv_file
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

from django.apps import apps  # Used to access all installed Django apps and their models.

# Run command:
# python manage.py exportdata model_name

class Command(BaseCommand):
    # Description shown when running: python manage.py help exportdata
    help = "Export data from the database to a csv file"

    def add_arguments(self, parser):
        # Accept the model name as a command-line argument.
        parser.add_argument("model_name", type=str, help="Model name")

    def handle(self, *args, **kwargs):
        # Retrieve the model name passed by the user and capitalize it.
        model_name = kwargs["model_name"].capitalize()

        # Initialize model variable with None.
        model = None

        # Search through all installed Django apps for the specified model.
        for app_config in apps.get_app_configs():
            try:
                # Try to find the model in the current app.
                model = apps.get_model(app_config.label, model_name)

                # Stop searching once the model is found.
                break

            except LookupError:
                # Ignore the error if the model is not found in this app
                # and continue searching in the next app.
                pass

        # If the model doesn't exist in any installed app, display a message.
        if not model:
            self.stdout.write(f"Model {model_name} could not found")
            return  # Stop executing the command.

        # Retrieve all records from the model's database table.
        data = model.objects.all()

        # generate csv filepath
        file_path = generate_csv_file(model_name)

        # Open the CSV file in write mode.
        # 'with' automatically closes the file after use.
        # newline="" prevents blank lines in Windows.
        with open(file_path, "w", newline="") as file:

            # Create a CSV writer object.
            writer = csv.writer(file)

            # Write the header row (column names) to the CSV file.
            writer.writerow(
                [field.name for field in model._meta.fields]
            )

            # Loop through every database record.
            for dt in data:

                # Extract each field value from the current object
                # and write it as one row in the CSV file.
                writer.writerow(
                    [getattr(dt, field.name) for field in model._meta.fields]
                )

        # Display a success message after exporting all records.
        self.stdout.write(
            self.style.SUCCESS("Successfully exported data")
        )