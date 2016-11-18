import json
from .managers import ReservationsManager
from datamappers import RoomMapper
from django.http import JsonResponse


reservationsManager = ReservationsManager()
roomMapper = RoomMapper()


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


def getReservations(request):
    if request.method == 'GET':
        params = request.GET

        if params.__contains__('roomNumber'):
            roomNumber = params.__getitem__('roomNumber')
        else:
            return JsonResponse({'error':'roomNumber required as GET parameter'}, status=422)
        if params.__contains__('startTimeslot'):
            startTimeslot = params.__getitem__('startTimeslot')
        else:
            return JsonResponse({'error':'startTimeslot required as GET parameter'}, status=422)

        json = {}
        for v,k in reservationsManager.getReservations(roomNumber,startTimeslot):
            json.update({k:v})

        return JsonResponse(json)

    else:
        return JsonResponse({'error':'POST not supported'}, status=405)

def getRooms(request):
    if request.method == 'GET':

        json = {}
        roomList = [tupl[0] for tupl in roomMapper.getRooms()]
        json.update({'rooms':roomList})

        return JsonResponse(json)

    else:
        return JsonResponse({'error':'POST not supported'}, status=405)


