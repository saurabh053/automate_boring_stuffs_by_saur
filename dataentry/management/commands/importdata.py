from django.core.management.base import BaseCommand, CommandError
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


# Import data to any model
# proposed command - python manage.py importdata file_path model_name
import csv
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    # help attribute command ki short description provide karta hai.
    # Agar hum:
    # python manage.py help <command_name>
    # run karein, to ye description terminal me display hoti hai.
    help = "Import data from csv file"

    # add_arguments() command line se input lene ke liye use hota hai.
    #
    # parser:
    # Django dwara provide kiya gaya ArgumentParser object hai.
    # Iska kaam command line arguments ko define aur validate karna hota hai.
    def add_arguments(self, parser):

        # file_path ek positional argument hai.
        #
        # Example:
        # python manage.py importcsv students.csv Student
        #
        # Yaha students.csv file_path me store ho jayega.
        parser.add_argument(
            'file_path',
            type=str,
            help="Path to the csv file:"
        )

        # model_name doosra positional argument hai.
        #
        # Example:
        # python manage.py importcsv students.csv Student
        #
        # Yaha Student model_name me store ho jayega.
        parser.add_argument(
            'model_name',
            type=str,
            help="Name of the model"
        )

    # handle() custom management command ka main execution method hai.
    #
    # Jab bhi command run hoti hai,
    # Django automatically isi function ko call karta hai.
    #
    # *args
    # Extra positional arguments receive karta hai.
    #
    # **kwargs
    # add_arguments() ke saare arguments dictionary ke form me receive hote hain.
    def handle(self, *args, **kwargs):

        # kwargs dictionary se CSV file ka path nikal rahe hain.
        #
        # Example:
        # kwargs = {
        #     "file_path": "students.csv",
        #     "model_name": "Student"
        # }
        file_path = kwargs['file_path']

        # kwargs dictionary se model ka naam retrieve kar rahe hain.
        model_name = kwargs['model_name'].capitalize()

        # Initially model variable ko None assign kar rahe hain.
        #
        # Agar baad me model mil jata hai,
        # to isi variable me model class store hogi.
        model = None

        # apps.get_app_configs()
        #
        # Ye project ke andar installed saare apps ki list return karta hai.
        #
        # Example:
        #
        # dataentry
        # accounts
        # blog
        # inventory
        #
        # Hum ek-ek app me check karenge
        # ki required model exist karta hai ya nahi.
        for app_config in apps.get_app_configs():

            try:

                # apps.get_model()
                #
                # Ye dynamically model ko retrieve karta hai.
                #
                # Parameters:
                #
                # app_config.label
                # Current app ka naam.
                #
                # model_name
                # User dwara command line se diya gaya model name.
                #
                # Example:
                # apps.get_model("dataentry", "Student")
                #
                # Agar model mil gaya,
                # to model variable me store ho jayega.
                model = apps.get_model(
                    app_config.label,
                    model_name
                )

                # Model milte hi loop stop kar dete hain.
                break

            except LookupError:

                # Agar current app me model nahi mila,
                # to LookupError raise hota hai.
                #
                # continue ka matlab:
                # Next app check karo.
                continue

        # Agar loop complete hone ke baad bhi
        # model None hai,
        # iska matlab kisi bhi app me model nahi mila.
        if not model:

            # CommandError Django management command ka
            # built-in exception hai.
            #
            # Ye terminal me proper error message show karta hai.
            raise CommandError(
                f'Model "{model_name}" not found in any app.'
            )

        # CSV file ko read mode me open kar rahe hain.
        #
        # with open ka benefit:
        # File automatically close ho jayegi,
        # chahe error aaye ya na aaye.
        with open(file_path, 'r') as file:

            # csv.reader()
            #
            # CSV file ko line by line read karta hai.
            #
            # Har row ek LIST return karta hai.
            #
            # Example:
            #
            # CSV
            # -------------
            # 1,Saurabh,29
            #
            # Output
            #
            # ['1','Saurabh','29']
            reader = csv.DictReader(file)

            # CSV ki har row ko ek-ek karke read karenge.
            for row in reader:

                # Agar row list hai,
                # to **row work nahi karega.
                #
                # ** sirf dictionary ke saath use hota hai.
                #
                # Is code ko sahi chalane ke liye
                # csv.DictReader() use karna chahiye.
                model.objects.create(**row)

        # Agar saara data successfully import ho gaya,
        # to green color me success message display hoga.
        self.stdout.write(

            # self.style.SUCCESS()
            #
            # Success message ko green color me print karta hai.
            self.style.SUCCESS(
                'Data imported from csv successfully!'
            )
        )

##########################################################################################################
##########################################################################################################