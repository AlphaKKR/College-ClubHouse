from django.shortcuts import render, redirect
from accounts.models import UserAccount
from django.contrib.auth import login, logout, authenticate
from clubs.models import ClubAccount
from django.http import HttpResponse


def index(request):
    return render(request, 'clubs/index.html')

def events(request):
    return render(request, 'clubs/events.html')

def recruitments(request):
    return render(request, 'clubs/recruitments.html')

def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            verified = UserAccount.objects.get(email=email)
            if verified.club_verification:
                login(request, user)
                return HttpResponse('Club Hub')
            else:
                return HttpResponse('Not a club account')
        else:
            return HttpResponse('User does not exist')
    return render(request, 'clubs/login.html')

def Logout(request):
    logout(request)
    return redirect('/clubs')

def post_event(request):
    if request == 'POST':
        pass