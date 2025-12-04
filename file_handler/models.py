from django.db import models
from django.contrib.auth.models import User


class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    # Override the delete method to remove the file from the media folder when the model instance is deleted
    def delete(self, *args, **kwargs):
        # delete file from media folder
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)