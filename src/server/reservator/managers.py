import datetime
from datamappers import ReservationMapper,RoomMapper


class ReservationsManager:
    maxReservationsPerWeekPerUser = 3

    def __init__(self):
        self.reservationMapper = ReservationMapper()
        self.roomMapper = RoomMapper()

    def makeReservation(self, username, roomNumber, timeslot):
        # ========================= ERRORS =====================================#
        # ERROR SCENARIO 1: Reservation already exists for that room and timeslot
        # OUTPUT: Reservation is placed on a waiting list (timeslot already reserved)

        # ERROR SCENARIO 2: Username has reached maximum amount of reservation per week (week of the timeslot)
        # OUTPUT: Error msg (maximum reservations reached for this week)

        # ERROR SCENARIO 3: Failed to make reservation
        # OUTPUT: Error msg (could not make reservation)

        # ========================= REQUIREMENTS ================================#
        # 1. User can only make 3 reservations per week across all rooms.
        # 2. User cannot make a reservation for the same timeslot in more than one room.
        # 3. User is removed from all waiting lists for the same timeslot if the user's reservation succeeds. 
        # 4. User is automatically put on the waiting list for a timeslot that is unavailable, if condition (1) holds.

        # ========================= BASIC FUNCTION FLOW ==========================#
        # 1. Check if a reservation exists for that timeslot (database query)
        #       If True, place User's reservation on the waiting list..
        # 2. Check if number of user's weekly reservations >= maxReservationsPerWeekPerUser 
        #       If True, return error
        # 3. Make reservation for user
        #       3.1 Create Reservation object (through reservationMapper)
        #       3.2 Add Reservation object to identityMap (internally done)
        #       3.3 Register Reservation object with UnitOfWork (internally done)
        #       3.4 Send commit() message to reservationMapper to persist changes..
        # 4. Process data operation
        #       - If insertion is successful, return confirmation msg
        #       - If insertion is unsucessful, return error msg

        response = {}
        if self.reservationMapper.getNumOfReservations(username, timeslot) >= self.maxReservationsPerWeekPerUser:
            response['error'] = 'Maximum reservations reached for this week.'
            return response

        status = 'filled'
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.reservationMapper.hasReservation(username, roomNumber, timeslot):
            response['error'] = 'Cannot make two reservations for the same date in the same room.'
            return response
        elif self.reservationMapper.isTimeslotReserved(roomNumber, timeslot):
            status = 'pending'

        self.reservationMapper.insert(username, roomNumber, status, timeslot, timestamp)
        self.reservationMapper.commit()

        response['reservation_status'] = status
        return response

    def modifyReservation(self, username, oldRoomNumber, oldTimeslot, newRoomNumber, newTimeslot):
        # ========================= REQUIREMENTS ================================#
        # 1. User can modify the room and the timeslot of his own reservations.
        # 2. If the new timeslot if unavailable, User's reservation placed on the waiting list.

        # ========================= BASIC FUNCTION FLOW ==========================#
        # 1. Check if a reservation exists for that timeslot (database query)
        #       If True, place User's reservation on the waiting list.
        #       If False, update User's reservation.

        response = {}
        status = 'filled'
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.reservationMapper.hasReservation(username, newRoomNumber, newTimeslot):
            response['error'] = 'Cannot make two reservations for the same date in the same room.'
            return response
        elif self.reservationMapper.isTimeslotReserved(newRoomNumber, newTimeslot):
            status = 'pending'

        self.reservationMapper.delete(username, oldRoomNumber, oldTimeslot)
        self.reservationMapper.insert(username, newRoomNumber, status, newTimeslot, timestamp)
        self.reservationMapper.updatePendingReservation(oldRoomNumber, oldTimeslot)
        self.reservationMapper.commit()

        response['reservation_status'] = status

        return response

    def cancelReservation(self, username, roomNumber, timeslot):
        # ========================= REQUIREMENTS ================================#
        # 1. User can cancel his reservations at any time.

        # ========================= BASIC FUNCTION FLOW ==========================#
        # 1. Delete User's reservation

        response = {}
        self.reservationMapper.delete(username, roomNumber, timeslot)
        self.reservationMapper.updatePendingReservation(roomNumber, timeslot)
        self.reservationMapper.commit()

        return response

    def getReservations(self, roomNumber, startTimeslot):
        # Default week is the current week
        response = self.reservationMapper.getReservations(roomNumber, startTimeslot)

        return response

    def getRooms(self):
        # Default week is the current week
        response = self.roomMapper.getRooms()

        return response




