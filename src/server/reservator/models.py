from hashlib import md5

class Reservation:
    def __init__(self, username, roomNumber, timeslot, status, timestamp):
        self.username = username
        self.roomNumber = roomNumber
        self.timeslot = timeslot
        self.status = status
        self.timestamp = timestamp

    def hashCode(self):
        lst = [self.username, self.roomNumber, self.timeslot]
        return md5(''.join(str(s) for s in lst)).hexdigest()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Room:
    def __init__(self, roomNumber):
        self.roomNumber = roomNumber
