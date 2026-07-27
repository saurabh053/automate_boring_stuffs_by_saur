from django.urls import path
from . import views

urlpatterns = [
    # need to attach this url in proj-dir urls.py
    path('import-data/', views.import_data, name='import-data'),
    path('export-data/', views.export_data, name='export_data'),

]