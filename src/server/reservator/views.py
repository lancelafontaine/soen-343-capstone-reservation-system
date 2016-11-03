from .managers import ReservationsManager
from django.http import JsonResponse


rm = ReservationsManager()


def home(request):
    return JsonResponse({'list':'bar'})


def log_in(request):
    # request.session['username'] = 'Jack'
    return JsonResponse({'foo':'bar'})


def log_out(request):
    pass


def modifyReservation(request):
    pass


def cancelReservation(request):
    pass


def makeReservation(request):
    pass


def viewReservations(request):
    pass


