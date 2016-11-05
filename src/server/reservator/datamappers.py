from unitofwork import UnitOfWork
from identitymaps import ReservationIdentityMap
from datagateways import ReservationTDG

class ReservationMapper:

    def __init__(self):
        self.uow = UnitOfWork(self) 
        self.identitymap = ReservationIdentityMap() 
        self.tdg = ReservationTDG()

    def insert(obj):
        # self.tdg.insert(obj.attribute...)
        pass

    def update(self, obj):
        # self.tdg.update(obj.attribute, ...)
        pass

    def delete(obj):
        # self.tdg.delete(obj.attribute, obj.attribute2,...)
        pass

    def remove(self, obj):
        #self.identitymap.delete(obj)
        #self.uow.register(obj)
        #self.uow.commit()
        pass

    def findAll():
        pass

    def find(identifier):
        pass

