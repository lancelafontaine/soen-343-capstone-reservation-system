class ReservationIdentityMap:
    # Naive implementation with no error checking
    def __init__(self):
        self.ids = {}

    def add(self, obj):
        self.ids[obj.hashCode()] = obj
    
    def delete(self, obj):
        del self.ids[obj.hashCode()]

    def update(self, obj):
        pass

    def find(self, hashCode):
        try:
            reservation = self.ids[hashCode]
        except KeyError:
            reservation = None

        return reservation
