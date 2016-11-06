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
        self.identitymap.add(r)
        self.uow.registerNew(r)

    # Called by ReservationsManager
    def delete(self, username, roomNumber, timeslot):
        r = self.identitymap.find(self.getHash(username, roomNumber, timeslot))
        # Error: What if object doesn't exist in identitymap?
        # Occurence: Restart Server (lose identitymap information)
        # Solution: Use the TDG to get the record from the database

        # Temporary
        if r is not None:
            self.identitymap.delete(r)
            self.uow.registerRemoved(r)

    # Called by ReservationsManager
    def update(self):
        pass

    # Called by ReservationsManager
    def updateWaitingList(self):
        pass
  
    # Called by UnitOfWork
    def applyInsert(self, objects):
        for obj in objects:
            self.tdg.insert(obj.username, obj.roomNumber, obj.timeslot, obj.status, obj.timestamp)

    def applyDelete(self, objects):
        for obj in objects:
            self.tdg.delete(obj.username, obj.roomNumber, obj.timeslot)

    def applyUpdate(self, obj):
        pass

    def commit(self):
        self.uow.commit()

    def getHash(self, username, roomNumber, timeslot):
        lst = [username, roomNumber, timeslot]
        return md5(''.join(str(s) for s in lst)).hexdigest()

