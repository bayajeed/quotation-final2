from django.contrib import admin
from .models import UploadedFile

# Register your models here.
#admin.site.register(UploadedFile)

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'file', 'uploaded_at')
    search_fields = ('title', 'user__username')
    list_filter = ('uploaded_at',)