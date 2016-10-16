from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    return render(request, 'reservator/login.html')

def log_in(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        # Redirect to a success
    else:
        render(request, 'reservation/index.html')
        # Return 'invalid' login

def log_out(request):
    logout(request)

    # Redirect to a success page

def register(request):
    print "HELLO"


def modify(request):
    print "HELLO"
