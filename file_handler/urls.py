from django.urls import path
from .views import upload_file, file_list, download_file, view_file, delete_file

app_name = 'file_handler'

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('list/', file_list, name='file_list'),
    path('download/<int:file_id>/', download_file, name='download_file'),
    path('view/<int:file_id>/', view_file, name='view_file'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
]
