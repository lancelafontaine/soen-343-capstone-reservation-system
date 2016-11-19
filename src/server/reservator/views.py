import datetime
from datamappers import *
from django.http import JsonResponse

reservationMapper = ReservationMapper()
userMapper = UserMapper()
roomMapper = RoomMapper()


def home(request):
    return JsonResponse({'list':'bar'})


def log_in(request):
    response = {}
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    isUserAuthenticated = userMapper.isRegistered(username, password)

    if isUserAuthenticated:
        request.session['is-logged-in'] = True
        response['logged-in'] = isUserAuthenticated
        response['lol'] = request.session['is-logged-in']
        return JsonResponse(response)
    else:
        response['loginError'] = 'The username or password provided is incorrect.'
        return JsonResponse(response)

def log_out(request):
    response = {}
    return JsonResponse(response)


def makeReservation(request):
    response = {}
    username = request.session.get('username','')
    roomNumber = request.POST.get('roomNumber', '')
    timeslot = request.POST.get('timeslot', '')

    if not username or not roomNumber or not timeslot:
        response['parameterError'] = 'username, roomNumber and timeslot are required parameters.'
        return JsonResponse(response)

    # Preconditions
    if reservationMapper.getNumOfReservations(username, timeslot) >= 3:
        response['reservationError'] = 'Maximum reservations reached for this week.'
        return JsonResponse(response)

    if reservationMapper.hasReservation(username, roomNumber, timeslot):
        response['reservationError'] = 'Cannot make two reservations for the same timeslot in the same room.'
        return JsonResponse(response)

    status = 'pending'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not reservationMapper.isTimeslotReserved(roomNumber, timeslot):
        status = 'filled'
        reservationMapper.removeFromAllOtherWaitingLists(username, roomNumber, timeslot)

    reservationMapper.insert(username, roomNumber, status, timeslot, timestamp)
    reservationMapper.commit()

    response['reservationStatus'] = status
    return JsonResponse(response)

def modifyReservation(request):
    response = {}
    username = request.session.get('username','')
    oldRoomNumber = request.POST.get('oldRoomNumber', '')
    newRoomNumber = request.POST.get('newRoomNumber', '')
    oldTimeslot = request.POST.get('oldTimeslot', '')
    newTimeslot = request.POST.get('newTimeslot', '')

    if not username or not oldRoomNumber or not newRoomNumber or not oldTimeslot or not newTimeslot:
        response['parameterError'] = 'username, oldRoomNumber, newRoomNumber, oldTimeslot, newTimeslot are \
                                      required parameters.'
        return JsonResponse(response)

    if reservationMapper.hasReservation(username, newRoomNumber, newTimeslot):
        response['reservationError'] = 'Cannot make two reservations for the same date in the same room.'
        return response

    status = 'pending'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not reservationMapper.isTimeslotReserved(newRoomNumber, newTimeslot):
        status = 'filled'
        reservationMapper.removeFromAllOtherWaitingLists(username, newRoomNumber, newTimeslot)

    reservationMapper.delete(username, oldRoomNumber, oldTimeslot)
    reservationMapper.insert(username, newRoomNumber, status, newTimeslot, timestamp)

    # TODO: Fix by checking previous reservation status
    reservationMapper.updatePendingReservation(oldRoomNumber, oldTimeslot)
    reservationMapper.commit()

    response['reservationStatus'] = status
    return JsonResponse(response)

def cancelReservation(request):
    response = {}
    username = request.session.get('username','')
    roomNumber = request.POST.get('roomNumber', '')
    timeslot = request.POST.get('timeslot', '')

    if not username or not roomNumber or not timeslot:
        response['parameterError'] = 'username, roomNumber and timeslot are required parameters.'
        return JsonResponse(response)

    reservationMapper.delete(username, roomNumber, timeslot)
    # TODO: Fix by checking previous reservation status
    reservationMapper.updatePendingReservation(roomNumber, timeslot)
    reservationMapper.commit()
    response['reservationStatus'] = 'cancelled'
    return JsonResponse(response)


def getReservedList(request):
    username = request.session.get('username','')
    if not username:
        return JsonResponse({'parameterError': 'username is a required parameter'})
    reservedList = reservationMapper.getReservationForUsername(username, 'filled')
    return JsonResponse({'reservedList': reservedList})


def getWaitingList(request):
    username = request.session.get('username','')
    if not username:
        return JsonResponse({'parameterError': 'username is a required parameter'})
    waitingList = reservationMapper.getReservationForUsername(username, 'pending')
    return JsonResponse({'waitingList': waitingList})

def getReservations(request):
    response = {}
    roomNumber = request.GET.get('roomNumber','')
    startTimeslot = request.GET.get('startTimeslot','')

    if not roomNumber or not startTimeslot:
        response['parameterError'] = 'roomNumber and startTimeslot are required parameters.'
        return JsonResponse(response, status=422)

    response['reservations'] = reservationMapper.getReservations(roomNumber, startTimeslot)
    return JsonResponse(response)

def getRooms(request):
    return JsonResponse({'rooms':roomMapper.getRooms()})
