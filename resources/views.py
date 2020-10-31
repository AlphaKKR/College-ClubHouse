from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .models import *

def index(request):
    objects1 = Subject.objects.all()
    objects2 = CAT1files.objects.all()
    objects3 = CAT2files.objects.all()
    objects4 = FATfiles.objects.all()
    param = {'objects1':objects1, 'objects2':objects2, 'objects3': objects3, 'objects4': objects4}
    return render(request, 'resources/index.html',param)


def search(request): 
    if 'term' in request.GET:   
        qs_subject = Subject.objects.filter(subject__icontains=request.GET.get('term'))
        qs_course  = Subject.objects.filter(course_code__icontains=request.GET.get('term'))

        queries = list()
        for query in qs_subject:
            queries.append(query.subject)
            queries.append(query.course_code)

        for query in qs_course:
            queries.append(query.subject)
            queries.append(query.course_code)
        
        print(queries)

        return JsonResponse(queries, safe=False)

def uploadSyllabus(request):
    if request.method == 'POST':
        instance = Subject(subject=request.POST['subject'], course_code=request.POST['course'], syll_file=request.FILES['myfile'])
        instance.save()
        url = instance.syll_file.url
        instance.syll_url = url
        instance.save()
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
            instance.cat_1_url = url
            instance.save()
            
            return render(request, 'resources/uploadcat1.html', {
                'uploaded_file_url': url
            })
        else:
            sub1 = Subject.objects.get(course_code=request.POST['course'])
            instance = CAT1files(course=sub1,  cat_1=request.FILES['myfile'])
            instance.save()
            url = instance.cat_1.url
            instance.cat_1_url = url
            instance.save()
            
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
            instance.cat_2_url = url
            instance.save()
            
            return render(request, 'resources/uploadcat2.html', {
                'uploaded_file_url': url
            })
        else:
            sub1 = Subject.objects.get(course_code=request.POST['course'])
            instance = CAT2files(course=sub1,  cat_2=request.FILES['myfile'])
            instance.save()
            url = instance.cat_2.url
            instance.cat_2_url = url
            instance.save()

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
            instance.fat_url = url
            instance.save()
            
            return render(request, 'resources/uploadfat.html', {
                'uploaded_file_url': url
            })
        else:
            sub1 = Subject.objects.get(course_code=request.POST['course'])
            instance = FATfiles(course=sub1,  fat_paper=request.FILES['myfile'])
            instance.save()
            url = instance.fat_paper.url
            instance.fat_url = url
            instance.save()
            
            return render(request, 'resources/uploadfat.html', {
                'uploaded_file_url': url
            })
    return render(request, 'resources/uploadfat.html')

