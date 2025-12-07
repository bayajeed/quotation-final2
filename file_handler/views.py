from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from .models import UploadedFile
from .forms import UploadedFileForm


@login_required
def upload_file(request):
    """Upload a file and assign it to the logged-in user"""
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            return redirect('file_handler:file_list')
    else:
        form = UploadedFileForm()

    return render(request, 'file_handler/upload.html', {'form': form})


@login_required
def file_list(request):
    """Searching and filtering files"""
    

    """List files with permission rules and filtering"""
    category_filter = request.GET.get('category', '')

    """
    Superuser → can see ALL files
    Normal User → can see ONLY their own files
    """
    if request.user.is_superuser:
        files = UploadedFile.objects.all().order_by('-uploaded_at')
    else:
        files = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at')

    # Filter apply
    if category_filter:
        files = files.filter(category=category_filter)

    files = files.order_by('-uploaded_at')
    file_choices = UploadedFile.STATIC_CHOICES

    return render(request, 'file_handler/file_list.html', {
        'files': files,
        'file_choices': file_choices,
        'category_filter': category_filter
    })

@login_required
def download_file(request, file_id):
    """
    Superuser → can download ANY file
    Normal User → can download ONLY their own file
    """
    if request.user.is_superuser:
        uploaded_file = get_object_or_404(UploadedFile, pk=file_id)
    else:
        uploaded_file = get_object_or_404(UploadedFile, pk=file_id, user=request.user)

    try:
        return FileResponse(
            uploaded_file.file.open('rb'),
            as_attachment=True,
            filename=uploaded_file.file.name
        )
    except FileNotFoundError:
        raise Http404("File does not exist")


@login_required
def view_file(request, file_id):
    """
    Superuser → can view ANY file
    Normal User → can view ONLY their own file
    """
    if request.user.is_superuser:
        uploaded_file = get_object_or_404(UploadedFile, pk=file_id)
    else:
        uploaded_file = get_object_or_404(UploadedFile, pk=file_id, user=request.user)

    try:
        content_type = (
            'application/pdf'
            if uploaded_file.file.name.lower().endswith('.pdf')
            else None
        )

        return FileResponse(
            uploaded_file.file.open('rb'),
            content_type=content_type
        )

    except FileNotFoundError:
        raise Http404("File does not exist")

@login_required
def delete_file(request, file_id):
    """Delete file with permission rules"""
    if request.user.is_superuser:
        uploaded_file = get_object_or_404(UploadedFile, pk=file_id)
    else:
        uploaded_file = get_object_or_404(UploadedFile, pk=file_id, user=request.user)

    # Temporarily disabled for template for user confirmation
    # uploaded_file.delete()
    # return redirect('file_handler:file_list')

    # file delete from media folder
    if uploaded_file.file:
        uploaded_file.file.delete(save=False)

    # delete record from database
    uploaded_file.delete()

    return redirect('file_handler:file_list')
