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

# CSV file ko read karne ke liye csv module import kar rahe hain.
import csv

# Django ke installed apps aur unke models ko dynamically access karne ke liye apps import kar rahe hain.
from django.apps import apps

# Custom management command banane aur custom errors raise karne ke liye import kar rahe hain.
from django.core.management.base import BaseCommand, CommandError


# Command class custom Django management command ko define karti hai.
class Command(BaseCommand):

    # Command ki short description define kar rahe hain.
    # Agar hum "python manage.py help importdata" chalaye,
    # to ye description terminal me dikhai degi.
    help = "Import data from csv file"

    # Command line arguments define karne ke liye ye method use hota hai.
    def add_arguments(self, parser):

        # User se CSV file ka path command line ke through receive karte hain.
        parser.add_argument(

            # CSV file ka positional argument define kar rahe hain.
            'file_path',

            # Input string type ka hona chahiye.
            type=str,

            # Help message display karne ke liye.
            help="Path to the csv file:"
        )

        # User se model ka naam command line ke through receive karte hain.
        parser.add_argument(

            # Model name positional argument define kar rahe hain.
            'model_name',

            # Input string type ka hona chahiye.
            type=str,

            # Help message display karne ke liye.
            help="Name of the model"
        )

    # Ye function command execute hone par automatically call hota hai.
    def handle(self, *args, **kwargs):

        # kwargs dictionary se CSV file ka path retrieve kar rahe hain.
        file_path = kwargs['file_path']

        # kwargs dictionary se model name retrieve karke uska first letter capital kar rahe hain.
        model_name = kwargs['model_name'].capitalize()

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

            # CSV ki har row ko ek-ek karke read kar rahe hain.
            for row in reader:

                # Current row ki values ko unpack karke database me new record create kar rahe hain.
                model.objects.create(**row)

        # Terminal me success message display kar rahe hain.
        self.stdout.write(

            # Success message ko green color me print karne ke liye SUCCESS style use kar rahe hain.
            self.style.SUCCESS(

                # Final success message.
                'Data imported from csv successfully!'
            )
        )
##########################################################################################################
##########################################################################################################