from django.shortcuts import render, redirect
from accounts.models import UserAccount
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse, JsonResponse
from resources.models import *
from clubs.models import ClubAccount,ClubEvent
from chatapp.models import Room
from django.contrib.postgres.search import SearchVector
from itertools import chain


def index(request): 
    if request.user.is_anonymous:
        return render(request, 'homepage/index.html', {'form_action': 'login', 'button_name': 'Login','objects': Room.objects.all(),'objects1':ClubEvent.objects.all()})
    else:
        return render(request, 'homepage/index.html', {'form_action': 'profile', 'button_name': 'Profile','objects': Room.objects.all(),'objects1':ClubEvent.objects.all()})

def Profile(request):
    user_data = {
            'firstname' : request.user.first_name,
            'lastname' : request.user.last_name,
            'username': request.user.username,
            'email': request.user.email,
        }
    # print(request.user.username)
    if not request.user.is_anonymous:
        if request.method == 'POST':
            time_table = request.POST.get('timetable')

            timetable_converted = [time_table]  
            timetable_binary = {}      

            slots = ['A1', 'TA1', 'TAA1', 'B1', 'TB1', 'C1', 'TC1', 'TCC1', 'D1', 'TD1', 'E1', 'TE1', 'F1', 'TF1', 'G1', 'TG1',
                    'A2', 'TA2', 'TAA2', 'B2', 'TB2', 'TBB2', 'C2', 'TC2', 'TCC2', 'D2', 'TD2', 'TDD2', 'E2', 'TE2', 'F2', 'TF2', 'G2', 'TG2',
                    'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11']

            lab_slots = ['L'+ f'{i}' for i in range(1, 95, 2)]
            for i in lab_slots:
                slots.append(i)
            for slot in slots:
                exec("%s = %d" % (slot,0))
            for j in slots:
                for k in timetable_converted:
                    if j+"-" in k:
                        exec("%s = %d" % (j,1))
            for slot in slots:
                timetable_binary[slot] = vars()[slot]

            
            user_m = UserAccount.objects.get(username=request.user.username)
            user_m.timetable = timetable_binary
            user_m.slot_list = slots
            user_m.save()
            return render(request, 'homepage/profile.html', user_data)

        else:
            return render(request, 'homepage/profile.html', user_data)

    else: 
        return redirect('/accounts/login')

  

def search(request): 
    if 'term' in request.GET:   
        qs_subject = Subject.objects.filter(subject__icontains=request.GET.get('term'))
        qs_course  = Subject.objects.filter(course_code__icontains=request.GET.get('term'))

        queries = list()


        qs_clubs = ClubAccount.objects.filter(club_name__icontains=request.GET.get('term'))
        qs_chatrooms = Room.objects.filter(name__icontains=request.GET.get('term'))

        queries = list()
        for query in qs_subject:
            queries.append(query.subject)
            queries.append(query.course_code)

        for query in qs_course:
            queries.append(query.subject)
            queries.append(query.course_code)

        for query in qs_clubs:
            queries.append(query.club_name)

        for query in qs_chatrooms:
            queries.append(query.name)

        return JsonResponse(queries, safe=False)

def SearchPage(request):
    if 'term' in request.GET:
        qs_subject = Subject.objects.filter(subject__icontains=request.GET.get('term'))
        qs_course = Subject.objects.filter( course_code__icontains=request.GET.get('term'))

        qs_clubs = ClubAccount.objects.filter(club_name__istartswith=request.GET.get('term'))
        qs_chatrooms = Room.objects.filter(name__istartswith=request.GET.get('term'))

        queries = list(chain(qs_subject, qs_course))
    param = {"allposts": queries,'cat1':CAT1files.objects.all(),'cat2': CAT2files.objects.all(), 'fat': FATfiles.objects.all(),'clubs':qs_clubs, 'chat': qs_chatrooms }
    return render(request, 'homepage/searchpage.html',param)
