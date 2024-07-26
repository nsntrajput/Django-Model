from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class SelectedData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=100)
    selected_at = models.DateTimeField(auto_now_add=True)
class DataFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

