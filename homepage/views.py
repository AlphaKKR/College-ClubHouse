from django.shortcuts import render, redirect
from accounts.models import UserAccount
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse, JsonResponse
from resources.models import *
from clubs.models import ClubAccount
from chatapp.models import Room
from django.db.models import Q, FilteredRelation


def index(request): 
    if request.user.is_anonymous:
        return render(request, 'homepage/index.html', {'form_action': 'login', 'button_name': 'Login'})
    else:
        # print(CAT1.objects.filter(course_code='cse1002'))
        return render(request, 'homepage/index.html', {'form_action': 'profile', 'button_name': 'Profile'})

def Profile(request):
    user_data = {
            'firstname' : request.user.first_name,
            'lastname' : request.user.last_name,
            'username': request.user.username,
            'email': request.user.email,
        }
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
        qs_subject_cat1 = CAT1.objects.filter(subject__istartswith=request.GET.get('term'))
        qs_course_cat1 = CAT1.objects.filter(course_code__istartswith=request.GET.get('term'))
        qs_subject_cat2 = CAT2.objects.filter(subject__istartswith=request.GET.get('term'))
        qs_course_cat2 = CAT2.objects.filter(course_code__istartswith=request.GET.get('term'))
        qs_subject_fat = FAT.objects.filter(subject__istartswith=request.GET.get('term'))
        qs_course_fat = FAT.objects.filter(course_code__istartswith=request.GET.get('term'))
        qs_clubs = ClubAccount.objects.filter(club_name__istartswith=request.GET.get('term'))
        qs_chatrooms = Room.objects.filter(name__istartswith=request.GET.get('term'))

        queries_cat1 = qs_subject_cat1 | qs_course_cat1
        queries_cat2 = qs_subject_cat2 | qs_course_cat2
        queries_fat = qs_subject_fat | qs_course_fat
        queries = list()

        for query in queries_cat1:
            queries.append(query.subject)
            queries.append(query.course_code)
        
        for query in queries_cat2:
            queries.append(query.subject)
            queries.append(query.course_code)

        for query in queries_fat:
            queries.append(query.subject)
            queries.append(query.course_code)

        for query in qs_clubs:
            queries.append(query.club_name)

        for query in qs_chatrooms:
            queries.append(query.name)

        return JsonResponse(queries, safe=False)
