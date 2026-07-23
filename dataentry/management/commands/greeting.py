from django.core.management.base import BaseCommand


# Proposed command:
# python manage.py greeting <Name>

class Command(BaseCommand):

    # help attribute command ki short description deta hai.
    # Jab hum "python manage.py help greeting" run karte hain,
    # to ye description terminal par display hoti hai.
    help = "Greeting the user"

    # add_arguments() ka use command line se user input lene ke liye hota hai.
    #
    # parser parameter:
    # -----------------
    # parser ek ArgumentParser object hota hai jo Django automatically
    # hume provide karta hai.
    #
    # Iska kaam hai command line arguments ko define aur validate karna.
    # Hum parser.add_argument() ki help se batate hain ki user ko
    # kaun-kaun se inputs dene honge.
    def add_arguments(self, parser):

        parser.add_argument(
            "name",                   # Positional argument (compulsory input)
            type=str,                 # Input string type ka hona chahiye
            help="Specifies user name"
        )

    # handle() custom management command ka main method hota hai.
    # Jab hum command run karte hain,
    # Django automatically isi method ko execute karta hai.
    #
    # *args:
    # -------
    # Extra positional arguments receive karta hai.
    # Mostly custom commands me iska use nahi hota,
    # lekin Django compatibility ke liye isse include karta hai.
    #
    # **kwargs:
    # ----------
    # add_arguments() me define kiye gaye saare arguments
    # dictionary ke form me yaha receive hote hain.
    #
    # Example:
    # python manage.py greeting Saurabh
    #
    # kwargs = {
    #     "name": "Saurabh"
    # }
    def handle(self, *args, **kwargs):

        # kwargs dictionary se "name" argument retrieve kar rahe hain.
        name = kwargs["name"]

        # Greeting message create kar rahe hain.
        greeting = f"Hi {name}, Good Morning!"

        # self.stdout.write() Django ka recommended output method hai.
        # Ye print() ki jagah use hota hai kyunki testing aur formatting
        # ke liye better support provide karta hai.
        self.stdout.write(self.style.SUCCESS(greeting))