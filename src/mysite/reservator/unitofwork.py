class UnitOfWork:
    def __init__(self, mapper):
        self.mapper = mapper
        self.newObjects = []
        self.dirtyObjects = []
        self.removedObjects = []

    def registerNew(obj):
        newObjects.append(obj)

    def registerDirty(obj):
        dirtyObjects.append(obj)
    
    def registerRemoved(obj):
        removedObjects.append(obj)

    def commit(self):
        for obj in self.newObjects:
            self.mapper.insert(obj)

        for obj in self.dirtyObjects:
            self.mapper.update(obj)

        for objc in self.removedObjects:
            self.mapper.delete(obj)

    def rollback():
        pass


