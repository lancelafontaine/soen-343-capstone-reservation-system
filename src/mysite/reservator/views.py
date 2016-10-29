from django.shortcuts import render
from django.http import HttpResponse
from .managers import ReservationsManager
from django.db import connection

rm = ReservationsManager()

def home(request):
    listy = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT symbol from stocks LIMIT 1')
        for row in cursor:
            listy.append(row)
    return render(request, 'reservator/index.html', {'test':listy[0]})


def log_in(request):
    # request.session['username'] = 'Jack'
    return render(request, 'reservator/login.html')

def log_out(request):

    return render(request, 'reservator/login.html')


def modifyReservation(request):
    print ("modify")


def cancelReservation(request):
    print ("cancel")


def makeReservation(request):
    print ("make")


def viewReservations(request):
    print ("view")


