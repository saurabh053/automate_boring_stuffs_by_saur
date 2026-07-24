from django.db import models

# Create your models here.
class Upload(models.Model):
    # we are not storing the file in the database we are storing the filepath in the database
    file = models.FileField(upload_to='uploads/')# upload_to -- where do you want to store this file in server
    model_name = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model_name