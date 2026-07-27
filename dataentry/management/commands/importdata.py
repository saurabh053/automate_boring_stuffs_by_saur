from django.core.management.base import BaseCommand, CommandError
from django.db import DataError

from dataentry.models import Student
import csv

# For single model or table
# class Command(BaseCommand):
#
#     # help attribute command ki short description deta hai.
#     # Agar hum "python manage.py help <command_name>" run kare,
#     # to ye description terminal me display hoti hai.
#     help = "Import data from CSV file"
#
#     # add_arguments() command line se input lene ke liye use hota hai.
#     #
#     # parser:
#     # Django dwara provide kiya gaya ArgumentParser object hai.
#     # Iska kaam command line arguments ko define aur validate karna hota hai.
#     def add_arguments(self, parser):
#
#         # filepath ek positional argument hai.
#         #
#         # Example:
#         # python manage.py importcsv students.csv
#         #
#         # Yaha "students.csv" filepath argument ke andar store ho jayega.
#         parser.add_argument(
#             'filepath',
#             type=str,
#             help="Path to CSV file"
#         )
#
#     # handle() custom management command ka main execution method hai.
#     # Jab command run hoti hai, Django automatically isi method ko execute karta hai.
#     #
#     # *args -> Extra positional arguments receive karta hai.
#     # **kwargs -> add_arguments() ke arguments dictionary ke form me receive hote hain.
#     def handle(self, *args, **kwargs):
#
#         # Command line se diya gaya filepath retrieve kar rahe hain.
#         #
#         # Example:
#         # python manage.py importcsv students.csv
#         #
#         # kwargs = {
#         #     "filepath": "students.csv"
#         # }
#         file_path = kwargs['filepath']
#
#         # CSV file ko read mode ('r') me open kar rahe hain.
#         #
#         # 'with open' use karne ka fayda ye hai ki
#         # file automatically close ho jati hai,
#         # chahe program successfully chale ya error aa jaye.
#         with open(file_path, 'r') as file:
#
#             # csv.DictReader() CSV file ki har row ko
#             # dictionary ke form me convert karta hai.
#             #
#             # Example CSV:
#             #
#             # roll_no,name,age
#             # 1,Saurabh,29
#             #
#             # DictReader output:
#             #
#             # {
#             #   "roll_no": "1",
#             #   "name": "Saurabh",
#             #   "age": "29"
#             # }
#             reader = csv.DictReader(file)
#
#             # CSV ki har row ko ek-ek karke read karenge.
#             for row in reader:
#
#                 # row ek dictionary hai.
#                 #
#                 # Example:
#                 # row = {
#                 #     "roll_no": "1",
#                 #     "name": "Saurabh",
#                 #     "age": "29"
#                 # }
#                 #
#                 # **row dictionary unpacking karta hai.
#                 #
#                 # Ye line internally iske barabar hai:
#                 #
#                 # Student.objects.create(
#                 #     roll_no=row["roll_no"],
#                 #     name=row["name"],
#                 #     age=row["age"]
#                 # )
#                 #
#                 # Isse har row database me ek naye Student record
#                 # ke roop me save ho jati hai.
#                 Student.objects.create(**row)
#
#         # Jab saara CSV data successfully import ho jata hai,
#         # tab terminal me green success message display hota hai.
#         self.stdout.write(
#             self.style.SUCCESS(
#                 "Data imported from CSV successfully."
#             )
#         )

##########################################################################################
##########################################################################################
# Import data to any model.

# Command run karne ka syntax:
# python manage.py importdata file_path model_name
import csv

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from dataentry.utils import check_csv_errors


class Command(BaseCommand):
    help = "Import data from csv file"

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help="Path to the csv file:"
        )

        parser.add_argument(
            'model_name',
            type=str,
            help="Name of the model"
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

        model = check_csv_errors(file_path, model_name)

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                model.objects.create(**row)

        self.stdout.write(
            self.style.SUCCESS(
                'Data imported from csv successfully!'
            )
        )##########################################################################################################
##########################################################################################################