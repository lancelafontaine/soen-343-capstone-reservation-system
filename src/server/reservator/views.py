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

    # Checking if user can be validated with given username and password
    isUserAuthenticated = userMapper.isRegistered(username, password)

    if isUserAuthenticated:
        # Sets a session variable 'is-logged-in' to True 
        request.session['is-logged-in'] = True 
        request.session['username'] = username 
        response['logged-in'] = isUserAuthenticated
        return JsonResponse(response)
    else:
        response['loginError'] = 'The username or password provided is incorrect.'
        return JsonResponse(response)

def log_out(request):
    response = {}

    # Clearing the session variable 'is-logged-in' and 'username'
    del request.session['is-logged-in']
    del request.session['username']

    # Checks whether the session variable 'is-logged-in' is cleared
    if not 'is-logged-in' in request.session:
        response['logged-out'] = True
    else:
        response['logged-out'] = False

    return JsonResponse(response)

def getSessionInfo(request):
    response = {}

    # Checks whether the session key 'is-logged-in' exists 
    if not 'is-logged-in' in request.session:
        isLoggedIn = False
    else:
        isLoggedIn = True
        
    response['is-logged-in'] = isLoggedIn

    return JsonResponse(response)

def makeReservation(request):
    response = {}
    username = request.session.get('username','')
    roomNumber = request.POST.get('roomNumber', '')
    timeslot = request.POST.get('timeslot', '')

    if not username or not roomNumber or not timeslot:
        response['parameterError'] = 'username, roomNumber and timeslot are required parameters.'
        return JsonResponse(response)

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
        return JsonResponse(response)

    oldReservation = reservationMapper.find(username, oldRoomNumber, oldTimeslot)
    if oldReservation is None:
        response['reservationError'] = 'Cannot modify nonexistent reservation.'
        return JsonResponse(response)

    status = 'pending'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not reservationMapper.isTimeslotReserved(newRoomNumber, newTimeslot):
        status = 'filled'
        reservationMapper.removeFromAllOtherWaitingLists(username, newRoomNumber, newTimeslot)

    reservationMapper.delete(username, oldRoomNumber, oldTimeslot)
    reservationMapper.insert(username, newRoomNumber, status, newTimeslot, timestamp)

    if oldReservation.status == 'filled':
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

    currentReservation = reservationMapper.find(username, roomNumber, timeslot)
    if currentReservation is None:
        response['reservationError'] = 'Cannot cancel nonexistent reservation.'
        return JsonResponse(response)

    reservationMapper.delete(username, roomNumber, timeslot)
    if currentReservation.status == 'filled':
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
