from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .utils import get_all_custom_models, check_csv_errors
from uploads.models import Upload
from .tasks import import_data_task

# Create your views here.

# Ye view user se CSV file lekar uska data database me import karta hai.
def import_data(request):

    # Check karo ki request POST method se aayi hai ya nahi.
    if request.method == "POST":

        # Uploaded CSV file ko request.FILES se retrieve karo.
        file_path = request.FILES.get('file_path')

        # User ne jo model select kiya hai uska naam request.POST se retrieve karo.
        model_name = request.POST.get('model_name')

        # Debugging ke liye selected model ka naam print karo.
        print("model_name=> ", model_name)

        # Uploaded file aur model name ko Upload model me save karo.
        upload = Upload.objects.create(file=file_path, model_name=model_name)

        # Uploaded file ka relative URL (jaise: /media/uploads/student.csv) retrieve karo.
        relative_path = str(upload.file.url)

        # Project ka base directory path retrieve karo.
        base_url = str(settings.BASE_DIR)

        # Base directory aur relative file path ko jodkar complete file path banao.
        file_path = base_url + relative_path

        #check for csv errors
        try:
            check_csv_errors(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect("import-data")
        #handle the import data task
        import_data_task.delay(file_path, model_name)

        #show the messages to the user
        messages.success(request, "Your data is being imported, you will be notified once it is done")
##################################################################################
##########################################Define this code in Celery taks#########
        # try:                                                                   #
        #     call_command('importdata', file_path, model_name)                  #
        #     messages.success(request, "Data imported successfully")            #
        # # Agar import ke time koi error aaye to usse raise kar do.             #
        # except Exception as e:                                                 #
        #     messages.error(request, str(e))                                    #
##################################################################################
        # Import complete hone ke baad user ko import page par redirect karo.
        return redirect("import-data")

    else:
        # Agar GET request hai to saare custom models ki list retrieve karo.
        custom_models = get_all_custom_models()

        # Models ki list template ko bhejne ke liye context dictionary banao.
        context = {
            'custom_models': custom_models,
        }

        # Debugging ke liye saare custom models print karo.
        all_models = get_all_custom_models()
        print(all_models)

    # Import page ko context ke saath render karke browser me display karo.
    return render(request, 'dataentry/importdata.html', context)