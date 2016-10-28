# Contains all 'Managers' for User, Room and Reservation

class ReservationsManager:
    maxReservationsPerWeekPerUser = 3

    def makeReservation(username, roomNumber, timeslot):
        # Cannot make a reservation for the same timeslot in different rooms
        # If the chosen timeslot is free:
        #   1. Check maxReservations limit for that week, for that username is less than some number X.
        #       If maxReservation is less than limit X:
        #           Instantiate UnitOfWork
        #           Create a new Reservation instance:
        #               fields: username, roomNumber, startWeek, timeslot, status=filled, timestamp=now
        #           Add the new Reservation to ReservationIdentityMap
        #           Register the new Reservation with UnitOfWork
        #            
        #
        #
        #
        #
        pass


    def modfiyReservation(username, roomNumber, timeslot):
        # Can change the room of the reservation and the timeslot
        # But will be put at the back of the waiting list (due to newer timestamp)
        pass

    def cancelReservation(username, roomNumber, timeslot):
        pass

    def getReservations(roomNumber, startWeek):
        pass
