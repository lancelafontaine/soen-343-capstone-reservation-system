
class Reservation:

    def __init__(self, username, roomNumber, timeslot, timestamp):
        self.username = username
        self.roomNumber = roomNumber
        self.timeslot = timeslot
        self.timestamp = timestamp

    def getHolder(self):
        return self.username

    def getRoomNumber(self):
        return self.roomNumber

    def getTimeslot(self):
        return self.timeslot

    def getTimestamp(self):
        return self.timestamp


class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getUsername(self):
        return self.username


class Room:

    def __init__(self, roomNumber):
        self.roomNumber = roomNumber

    def getRoomNumber(self):
        return self.roomNumber

class Timeslot:

    def __init__(self, startWeek, startTime, endTime):
        self.startWeek = startWeek
        self.startTime = startTime
        self.endTime = endTime
    
    def getStartWeek(self):
        return self.startWeek

    def getStartTime(self):
        return self.starTime
