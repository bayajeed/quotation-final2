from django.db import models
from django.contrib.auth.models import User
import os
from datetime import datetime

def user_directory_path(instance, filename):
    # original filename (without extension)
    base_name = os.path.splitext(filename)[0]

    # extension
    ext = filename.split('.')[-1]

    # add datetime to keep unique
    timestamp = datetime.now().strftime("%Y%m%d_%I%M%S%p")

    # new filename → original + datetime
    final_filename = f"{base_name}_{timestamp}.{ext}"

    # folder name = username
    folder_name = instance.user.username

    # final path → uploads/<username>/<filename>
    return os.path.join("uploads", folder_name, final_filename)

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    # Override the delete method to remove the file from the media folder when the model instance is deleted
    def delete(self, *args, **kwargs):
        # delete file from media folder
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)