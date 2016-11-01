class ReservationIdentityMap:
    # Naive implementation with no error checking
    def __init__(self):
        self.ids = {}

    def add(obj):
        ids[obj.hashCode()] = obj
    
    def delete(obj):
        del ids[obj.hashCode()]

    def update(obj):
        # Could be split into more specialized updates (ex: updateTimeslot)
        pass

    def find(obj):
        return ids[obj.hashCode()]
