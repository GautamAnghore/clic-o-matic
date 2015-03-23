import pymongo


class Remote():

    def __init__(self, database):
        self.db = database
        self.collection = database.remotedump

    def add_dump(self, data):
        catch = {'data': data}

        try:
            self.collection.insert(catch)
        except pymongo.errors.OperationFailure:
            print "Mongodb OperationFailure db: remote"
            return False

        return True
