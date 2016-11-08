from hashlib import md5
from unitofwork import UnitOfWork
from identitymaps import ReservationIdentityMap
from datagateways import ReservationTDG
from models import Reservation

class ReservationMapper:

    def __init__(self):
        self.uow = UnitOfWork(self) 
        self.identitymap = ReservationIdentityMap() 
        self.tdg = ReservationTDG()

    # Called by ReservationsManager 
    # TODO: Check if already in the cache (idmap)
    def insert(self, username, roomNumber, timeslot, status, timestamp):
        r = Reservation(username, roomNumber, timeslot, status, timestamp)
        # If already exists in identity map, throw error
        self.identitymap.add(r)
        self.uow.registerNew(r)

    # Called by ReservationsManager
    def delete(self, username, roomNumber, timeslot):
        r = self.identitymap.find(self.getHash(username, roomNumber, timeslot))
        if r is None:
            r = self.loadReservation(self.tdg.find(username, roomNumber, timeslot))
            if r is None:
                return 'Reservation does not exist.'
            else:
                self.uow.registerRemoved(r)
        else:
            self.identitymap.delete(r)
            self.uow.registerRemoved(r)

    # Called by ReservationsManager
    def updatePendingReservation(self, roomNumber, timeslot):
        r = self.identitymap.findNextPendingReservation(roomNumber, timeslot)
        if r is None:
            r = self.loadReservation(self.tdg.findNextPendingReservation(roomNumber, timeslot))
            if r is not None:
                self.identitymap.add(r)
                self.uow.registerDirty(r)
        else:
            self.identitymap.setFilled(r)
            self.uow.registerDirty(r)

    # Change to counter method
    def isTimeslotReserved(self, roomNumber, timeslot):
        # Could use a counter instead (tdg)
        found = False
        r = self.identitymap.findReserved(roomNumber, timeslot)
        if r is None:
            r = self.loadReservation(self.tdg.findFilled(roomNumber, timeslot))
            if r is not None:
                found = True
        return found

    # Change to counter method
    def hasReservation(self, username, roomNumber, timeslot):
        isWaiting = False
        r = self.identitymap.isOnWaitingList(username, roomNumber, timeslot)
        if r is None:
            r = self.loadReservation(self.tdg.isWaitlisted(username, roomNumber, timeslot))
            if r is not None:
                isWaiting = True
        return isWaiting

    def getReservations(self, roomNumber, startWeek):
        pass

    def getNumOfReservations(self, username, timeslot):
        pass

    # Called by UnitOfWork
    def applyInsert(self, objects):
        for obj in objects:
            self.tdg.insert(obj.username, obj.roomNumber, obj.timeslot, obj.status, obj.timestamp)

    def applyDelete(self, objects):
        for obj in objects:
            self.tdg.delete(obj.username, obj.roomNumber, obj.timeslot)

    def applyUpdate(self, objects):
        # Update the status of a reservation
        for obj in objects:
            self.tdg.setFilled(obj.username, obj.roomNumber, obj.timeslot)

    def commit(self):
        self.uow.commit()

    def loadReservation(self, attributes):
        pass

    def getHash(self, username, roomNumber, timeslot):
        lst = [username, roomNumber, timeslot]
        return md5(''.join(str(s) for s in lst)).hexdigest()

