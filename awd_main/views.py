from django . shortcuts import render
import time
from django.http import HttpResponse
from dataentry.tasks import celery_test_task

def home(request):
    return render(request, 'home.html')


def celery_test(request):
    # want to execute time consuming task here
    celery_test_task.delay()
    return HttpResponse('<h3>Function Executed successfully</h3>')

