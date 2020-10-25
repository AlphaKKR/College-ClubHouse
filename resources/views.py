from django.shortcuts import render, redirect
from django.conf import settings
from .models import CAT1files, Subject

def index(request):
    return render(request, 'resources/index.html')

def upload(request):
    if request.method == 'POST':
        if Subject.objects.filter(course_code=request.POST['course'])==None:
            sub = Subject(subject=request.POST['subject'], course_code=request.POST['course'])
            sub.save()
            instance = CAT1files(course=sub,  cat_1=request.FILES['myfile'])
            instance.save()
            print('sub doesnt exist')
            url = instance.cat_1.url
            instance = CAT1files.objects.update(cat_1_url=url)
            
            return render(request, 'resources/upload.html', {
                'uploaded_file_url': url
            })
        else:
            print('sub exists')

            sub1 = Subject.objects.get(course_code=request.POST['course'])
            instance = CAT1files(course=sub1,  cat_1=request.FILES['myfile'])
            instance.save()
            url = instance.cat_1.url
            instance = CAT1files.objects.update(cat_1_url=url)
            
            return render(request, 'resources/upload.html', {
                'uploaded_file_url': url
            })


    return render(request, 'resources/upload.html')
    