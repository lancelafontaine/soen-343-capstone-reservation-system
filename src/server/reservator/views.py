#from django.shortcuts import render
#from django.http import HttpResponse
from .managers import ReservationsManager
from django.db import connection
from django.http import JsonResponse
rm = ReservationsManager()

def home(request):
    listy = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT symbol from stocks LIMIT 1')
        for row in cursor:
            listy.append(row)
    return JsonResponse({'list':'bar'})

def log_in(request):
    # request.session['username'] = 'Jack'
    return JsonResponse({'foo':'bar'})

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


