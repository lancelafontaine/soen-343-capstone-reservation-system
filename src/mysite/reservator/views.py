from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout


class Registry(View):
    # ReservationManager(rm) attribute

    def index(request):
        return render(request, 'reservator/login.html')

    def log_in(request):
        # Check if username and password match 
        # Save current Users in a Session Table
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

    def modifyReservation(request):
        # rm.modfiyReservation()
        print "modify"

    def cancelReservation(request):
        # rm.cancelReservation()
        print "cancel"

    def makeReservation(request):
        # rm.makeReservation()
        print "make"
    
    def viewReservations(request):
        # rm.getReservations(roomNumber);
        # Display


