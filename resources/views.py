from django.shortcuts import render, redirect
from django.conf import settings
# from .models import CAT1files

def index(request):
    return render(request, 'resources/index.html')

def upload(request):
    # if request.method == 'POST':
    #     print('valid')
    #     instance = CAT1(subject=request.POST['subject'], course_code=request.POST['course'],  cat_1=request.FILES['myfile'])
    #     instance.save()
    #     url = instance.cat_1
    #     return render(request, 'resources/upload.html', {
    #         'uploaded_file_url': url
    #     })
    
    return render(request, 'resources/upload.html')
    