from datagateways import ReservationTDG
from datamappers import ReservationMapper 
from identitymaps import ReservationIdentityMap
from unitofwork import UnitOfWork


class ReservationsManager:
    maxReservationsPerWeekPerUser = 3

    def __init__(self):
        self.mapper = ReservationMapper()
        self.uow = UnitOfWork()
        self.identitymap = ReservationIdentityMap()

        # Create links
        self.uow.attachMapper(self.mapper)
        self.mapper.attachUnitOfWork(self.uow)
        self.mapper.attachIdentityMap(self.identitymap)


    def makeReservation(self, username, roomNumber, timeslot):
        #========================= ERRORS =====================================#
        # ERROR SCENARIO 1: Reservation already exists for that room and timeslot
        # OUTPUT: Reservation is placed on a waiting list (timeslot already reserved)

        # ERROR SCENARIO 2: Username has reached maximum amount of reservation per week (week of the timeslot)
        # OUTPUT: Error msg (maximum reservations reached for this week)

        # ERROR SCENARIO 3: Failed to make reservation
        # OUTPUT: Error msg (could not make reservation)

        #========================= REQUIREMENTS ================================#
        # 1. User can only make 3 reservations per week across all rooms.
        # 2. User cannot make a reservation for the same timeslot in more than one room.
        # 3. User is removed from all waiting lists for the same timeslot if the user's reservation succeeds. 
        # 4. User is automatically put on the waiting list for a timeslot that is unavailable, if condition (1) holds.

        #========================= BASIC FUNCTION FLOW ==========================#
        # 1. Check if a reservation exists for that timeslot (database query)
        #       If True, place User's reservation on the waiting list..
        # 2. Check if number of user's weekly reservations < 3 
        #       If False, return error
        # 3. Make reservation for user
        #       3.1 Create Reservation object
        #       3.2 Add Reservation object to identityMap (internally done)
        #       3.3 Register Reservation object with UnitOfWork (internally done)
        #       3.4 Send commit() message to mapper to persist changes..
        # 4. Process data operation
        #       - If insertion is successful, return confirmation msg
        #       - If insertion is unsucessful, return error msg

        # EXECUTION
        # Check identityMap for existing reservation at that timeslot.
        # If not in Map, check Database using TDG find(timeslot)(SQL exists query)
        # If not in Database, self.mapper.insert(Reservation(username,roomNumber,timeslot,status,timestamp)).

        # Decide how to commit the operation (either through mapper or uow)
        # self.mapper.commit()
        pass


    def modfiyReservation(self, username, roomNumber, timeslot):
        #========================= REQUIREMENTS ================================#
        # 1. User can modify the room and the timeslot of his own reservations.
        # 2. If the new timeslot if unavailable, User's reservation placed on the waiting list.

        #========================= BASIC FUNCTION FLOW ==========================#
        # 1. Check if a reservation exists for that timeslot (database query)
        #       If True, place User's reservation on the waiting list.
        #       If False, update User's reservation.
        pass

    def cancelReservation(self, username, roomNumber, timeslot):
        #========================= REQUIREMENTS ================================#
        # 1. User can cancel his reservations at any time.

        #========================= BASIC FUNCTION FLOW ==========================#
        # 1. Delete User's reservation
        pass


    def getReservations(self, roomNumber, startWeek):
        pass
