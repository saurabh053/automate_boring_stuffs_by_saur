import csv

from django.core.management.base import BaseCommand
from dataentry.models import Student



# For inserting single data
# class Command(BaseCommand):
#     help = "It will insert data to the database"
#
#     def handle(self, *args, **kwargs):
#         # logic goes here
#         Student.objects.all().create(roll_no=1001, name="Rathan", age=20)
#         self.stdout.write(self.style.SUCCESS("Data inserted successfully"))


# For inserting multiple data
# class Command(BaseCommand):
#
#     def handle(self, *args, **options):
#         dataset = [
#             {"roll_no": 1002, 'name': "Sachin", "age": 21},
#             {"roll_no": 1003, 'name': "John", "age": 22},
#             {"roll_no": 1004, "name": "Mike", "age": 23},
#         ]
#         # dataset ek list hai jisme multiple student records stored hain.
#         # Har record ek dictionary ke form me hota hai.
#
#
#         # Student.objects.create() ka use database me naya record insert karne ke liye hota hai.
#         #
#         # 'data' current student ki dictionary hai.
#         # Example:
#         # data = {
#         #     "roll_no": 101,
#         #     "name": "Saurabh",
#         #     "age": 25
#         # }
#         #
#         # data['roll_no'] -> 101
#         # data['name'] -> "Saurabh"
#         # data['age'] -> 25
#         #
#         # Ye values Student model ke corresponding fields me save ho jati hain.
#         for data in dataset:
#             roll_no = data['roll_no']
#             existing_record = Student.objects.filter(roll_no=roll_no).exists()
#             if not existing_record:
#                 Student.objects.create(roll_no=roll_no, name=data['name'], age=data['age'])
#             else:
#                 self.stdout.write(self.style.WARNING(f"Student with roll no {roll_no} already exists:"))
#         self.stdout.write(self.style.SUCCESS('Successfully inserted data'))







class Command(BaseCommand):

    # help attribute command ki short description deta hai.
    # Agar hum "python manage.py help <command_name>" run kare,
    # to ye description terminal me display hoti hai.
    help = "Import data from CSV file"

    # add_arguments() command line se input lene ke liye use hota hai.
    #
    # parser:
    # Django dwara provide kiya gaya ArgumentParser object hai.
    # Iska kaam command line arguments ko define aur validate karna hota hai.
    def add_arguments(self, parser):

        # filepath ek positional argument hai.
        #
        # Example:
        # python manage.py importcsv students.csv
        #
        # Yaha "students.csv" filepath argument ke andar store ho jayega.
        parser.add_argument(
            'filepath',
            type=str,
            help="Path to CSV file"
        )

    # handle() custom management command ka main execution method hai.
    # Jab command run hoti hai, Django automatically isi method ko execute karta hai.
    #
    # *args -> Extra positional arguments receive karta hai.
    # **kwargs -> add_arguments() ke arguments dictionary ke form me receive hote hain.
    def handle(self, *args, **kwargs):

        # Command line se diya gaya filepath retrieve kar rahe hain.
        #
        # Example:
        # python manage.py importcsv students.csv
        #
        # kwargs = {
        #     "filepath": "students.csv"
        # }
        file_path = kwargs['filepath']

        # CSV file ko read mode ('r') me open kar rahe hain.
        #
        # 'with open' use karne ka fayda ye hai ki
        # file automatically close ho jati hai,
        # chahe program successfully chale ya error aa jaye.
        with open(file_path, 'r') as file:

            # csv.DictReader() CSV file ki har row ko
            # dictionary ke form me convert karta hai.
            #
            # Example CSV:
            #
            # roll_no,name,age
            # 1,Saurabh,29
            #
            # DictReader output:
            #
            # {
            #   "roll_no": "1",
            #   "name": "Saurabh",
            #   "age": "29"
            # }
            reader = csv.DictReader(file)

            # CSV ki har row ko ek-ek karke read karenge.
            for row in reader:

                # row ek dictionary hai.
                #
                # Example:
                # row = {
                #     "roll_no": "1",
                #     "name": "Saurabh",
                #     "age": "29"
                # }
                #
                # **row dictionary unpacking karta hai.
                #
                # Ye line internally iske barabar hai:
                #
                # Student.objects.create(
                #     roll_no=row["roll_no"],
                #     name=row["name"],
                #     age=row["age"]
                # )
                #
                # Isse har row database me ek naye Student record
                # ke roop me save ho jati hai.
                Student.objects.create(**row)

        # Jab saara CSV data successfully import ho jata hai,
        # tab terminal me green success message display hota hai.
        self.stdout.write(
            self.style.SUCCESS(
                "Data imported from CSV successfully."
            )
        )
