from django.shortcuts import render
from django.http import HttpResponse


# Reservation manager attribute

def index(request):
    return render(request, 'reservator/login.html')

def log_in(request):
    # Check if username and password match 
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

def modifyReservation(self, request):
    # rm.modfiyReservation()


def cancelReservation(self, request):
    # rm.cancelReservation()


def makeReservation(self, request):
    # rm.makeReservation()


def viewReservations(self, request):
    # rm.getReservations(roomNumber);
    # Display


