from django.shortcuts import render
from django.http import HttpResponse


def home(request):
	return render(request, 'reservator/index.html')


def log_in(request):
    return render(request, 'reservator/login.html')


def log_out(request):
    print "log_out"


def modifyReservation(request):
    print "modify"


def cancelReservation(request):
    print "cancel"


def makeReservation(request):
    print "make"


def viewReservations(request):
    print "view"


