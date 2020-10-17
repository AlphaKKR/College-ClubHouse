from django.shortcuts import render, redirect
from accounts.models import UserAccount
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from .models import Room, Message
import json
from django.conf import settings


def chathome(request):
    if request.user.is_anonymous:
        return redirect('/accounts/login')

    rooms = Room.objects.all()
    return render(request, 'chatapp/chathome.html', {'rooms': rooms})


def createroom(request):
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    newroom = request.GET['newroom']

    if Room.objects.filter(name = newroom).exists():
        return HttpResponse('false')
    else:
        clientip = request.META.get('HTTP_X_FORWARDED_FOR')
        room = Room.objects.create(
            user=request.user, name=newroom, ipaddress=clientip)
        return HttpResponse('true')

def activeroom(request, room_name):
    print(room_name)
    if not request.user.is_anonymous:
        if Room.objects.filter(name=room_name).exists():
            messages = Message.objects.filter(name=room_name)
            return render(request, 'chatapp/home.html', {'chat': messages, 'room_key': room_name})
        else:
            return HttpResponseNotFound(render(request, 'chatapp/notfound.html'))

    return redirect('/accounts/login')


def Post(request):
    if request.method == 'POST':
        msg = request.POST.get('msgbox', None)
        room_key = request.POST.get('room_data', None)
        print(request.POST.get('room_data', None))
        c = Message.objects.create(user=request.user, messages=msg, name=room_key)
        print(c.user)
        if msg != '':
            c.save()
        return JsonResponse({ 'msg': msg, 'user': c.user.username,'id': c.id})
    else:
        return HttpResponse('Request must be POST.')

def Messages(request):
    chatid = int( request.GET['id'])
    room_id = request.GET['room_id']
    obj = Message.objects.filter(name=room_id)
    c=[]
    print(obj)
    for i in obj:
        print(i)
        if i.id>chatid:
            print(i)
            c.append(i)

    return render(request,'chatapp/messages.html',{'chat':c})
