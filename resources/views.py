from django.shortcuts import render, redirect
from django.conf import settings
from .models import *

def index(request):
    return render(request, 'resources/index.html')


def uploadSyllabus(request):
    if request.method == 'POST':
        instance = Subject(subject=request.POST['subject'], course_code=request.POST['course'], syll_file=request.FILES['myfile'])
        instance.save()
        url = instance.syll_file.url
        instance = Subject.objects.update(syll_url=url)
        
        return render(request, 'resources/syllabus.html', {
            'uploaded_file_url': url
        })


    return render(request, 'resources/syllabus.html')


def uploadCAT1(request):
    if request.method == 'POST':
        if not Subject.objects.filter(course_code=request.POST['course']).exists():
            sub = Subject(subject=request.POST['subject'], course_code=request.POST['course'])
            sub.save()
            instance = CAT1files(course=sub,  cat_1=request.FILES['myfile'])
            instance.save()
            url = instance.cat_1.url
            instance = CAT1files.objects.update(cat_1_url=url)
            
            return render(request, 'resources/uploadcat1.html', {
                'uploaded_file_url': url
            })
        else:
            sub1 = Subject.objects.get(course_code=request.POST['course'])
            instance = CAT1files(course=sub1,  cat_1=request.FILES['myfile'])
            instance.save()
            url = instance.cat_1.url
            instance = CAT1files.objects.update(cat_1_url=url)
            
            return render(request, 'resources/uploadcat1.html', {
                'uploaded_file_url': url
            })


    return render(request, 'resources/uploadcat1.html')

def uploadCAT2(request):
    if request.method == 'POST':
        if not Subject.objects.filter(course_code=request.POST['course']).exists():
            sub = Subject(subject=request.POST['subject'], course_code=request.POST['course'])
            sub.save()
            instance = CAT2files(course=sub,  cat_2=request.FILES['myfile'])
            instance.save()
            print(instance.date)
            url = instance.cat_2.url
            instance = CAT2files.objects.update(cat_2_url=url)
            
            return render(request, 'resources/uploadcat2.html', {
                'uploaded_file_url': url
            })
        else:
            sub1 = Subject.objects.get(course_code=request.POST['course'])
            instance = CAT2files(course=sub1,  cat_2=request.FILES['myfile'])
            instance.save()
            url = instance.cat_2.url
            instance = CAT2files.objects.update(cat_2_url=url)
            
            return render(request, 'resources/uploadcat2.html', {
                'uploaded_file_url': url
            })
    return render(request, 'resources/uploadcat2.html')

def uploadFAT(request):
    if request.method == 'POST':
        if not Subject.objects.filter(course_code=request.POST['course']).exists():
            sub = Subject(subject=request.POST['subject'], course_code=request.POST['course'])
            sub.save()
            instance = FATfiles(course=sub,  fat_paper=request.FILES['myfile'])
            instance.save()
            print(instance.date)
            url = instance.fat_paper.url
            instance = FATfiles.objects.update(fat_url=url)
            
            return render(request, 'resources/uploadfat.html', {
                'uploaded_file_url': url
            })
        else:
            sub1 = Subject.objects.get(course_code=request.POST['course'])
            instance = FATfiles(course=sub1,  fat_paper=request.FILES['myfile'])
            instance.save()
            url = instance.fat_paper.url
            instance = FATfiles.objects.update(fat_url=url)
            
            return render(request, 'resources/uploadfat.html', {
                'uploaded_file_url': url
            })
    return render(request, 'resources/uploadfat.html')

