from django.core.management import BaseCommand

class Command(BaseCommand):
    # python manage.py helloworld --help
    help = "Prints Hello World"



    # we write the logic that we want to perform
    def handle(self, *args, **kwargs):
        #way to print message on the terminal
        self.stdout.write("Hello World")