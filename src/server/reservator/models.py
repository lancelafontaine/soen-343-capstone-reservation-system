import hashlib

class Reservation:
    def __init__(self, username, roomNumber, timeslot, timestamp):
        self.username = username
        self.roomNumber = roomNumber
        self.timeslot = timeslot
        self.timestamp = timestamp

    def hashCode(self):
        lst = [self.username, self.roomNumber, self.timeslot, self.timestamp]
        return hashlib.md5(''.join(str(s) for s in lst))

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Room:
    def __init__(self, roomNumber):
        self.roomNumber = roomNumber

class Timeslot:

    # TODO: Determine attributes
    def __init__(self):
        pass

    def __str__(self):
        # TODO: Return proper representation
        pass
