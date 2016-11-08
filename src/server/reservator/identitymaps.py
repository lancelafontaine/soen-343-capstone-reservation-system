class ReservationIdentityMap:
    # Naive implementation with no error checking
    def __init__(self):
        self.ids = {}

    def add(self, obj):
        self.ids[obj.hashCode()] = obj
    
    def delete(self, obj):
        del self.ids[obj.hashCode()]

    def findNextPendingReservation(self, roomNumber, timeslot):
        #reservation = None
        #minTimestamp = ''
        #for key, value in self.ids.iteritems():
        #    if value.roomNumber == roomNumber and value.timeslot == timeslot:
                # Conver to datetime
        #        if value.timestamp



    def findReserved(self, roomNumber, timeslot):
        reservation = None
        for key, value in self.ids.iteritems():
            if value.status =='filled' and value.roomNumber == roomNumber and value.timeslot == timeslot:
                reservation = value
        return reservation

    def setFilled(self, obj):
        self.ids[ob.obj.hashCode()].status = 'filled'

    def find(self, hashCode):
        try:
            reservation = self.ids[hashCode]
        except KeyError:
            reservation = None
        return reservation
