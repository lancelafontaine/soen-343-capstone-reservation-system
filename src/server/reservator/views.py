from .managers import ReservationsManager
from django.http import JsonResponse


rm = ReservationsManager()


def home(request):
    return JsonResponse({'list':'bar'})


def log_in(request):
    # request.session['username'] = 'Jack'

    # For testing purposes
    rm.makeReservation('testuser','H-905','13:00')
    rm.makeReservation('testuser','H-831','15:00')
    rm.cancelReservation('testuser','H-831','15:00')
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


