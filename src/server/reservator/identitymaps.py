import datetime
class ReservationIdentityMap:
    # Naive implementation with no error checking
    def __init__(self):
        self.ids = {}

    def add(self, obj):
        self.ids[obj.hashCode()] = obj
    
    def delete(self, obj):
        del self.ids[obj.hashCode()]

    def findNextPendingReservation(self, roomNumber, timeslot):
        reservation = None
        lowest = datetime.datetime.max
        format = "%Y-%m-%d %H:%M:%S"
        for key, value in self.ids.iteritems():
            if value.roomNumber == roomNumber and value.timeslot == timeslot and value.status == 'pending':
                timestamp = datetime.datetime.strptime(value.timestamp, format)
                if timestamp < lowest:
                    lowest = timestamp
                    reservation = value
        return reservation

    def findReserved(self, roomNumber, timeslot):
        reservation = None
        for key, value in self.ids.iteritems():
            if value.status =='filled' and value.roomNumber == roomNumber and value.timeslot == timeslot:
                reservation = value
        return reservation

    def setFilled(self, obj):
        self.ids[obj.hashCode()].status = 'filled'

    def find(self, hashCode):
        try:
            reservation = self.ids[hashCode]
        except KeyError:
            reservation = None
        return reservation

class RoomIdentityMap:
    def __init__(self):
        self.ids = {}

    def add(self, obj):
        self.ids[obj.hashCode()] = obj

class UserIdentityMap:
    def __init__(self):
        self.ids = {}

    def add(self, obj):
        self.ids[obj.hashCode()] = obj