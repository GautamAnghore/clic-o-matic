import pymongo


class Remote():

    def __init__(self, database):
        self.db = database
        self.collection = database.clickdata

    def add_clickdata(self, clickdata):
        # data will be added only if the pageurl exists in users collection
        # this function will be called after checking the existence

        # in this function, we have to check if the data points already exists
        # if yes, increase the value by 1,
        # else, insert the data points in the list

        search_doc = {'page': clickdata['pageurl'],
                      'datapoints.x': clickdata['datapoint']['x'],
                      'datapoints.y': clickdata['datapoint']['y']}

        try:
            doc = self.collection.find_one(search_doc)
        except pymongo.errors.OperationFailure:
            print "Mongodb operationFailure db: remote"

        if doc is not None:
            try:
                self.collection.find_and_modify(search_doc, {'$inc': {'datapoints.$.value': 1}})
            except pymongo.errors.OperationFailure:
                print "Mongodb operationFailure db: remote"
                return False
        else:
            # datapoints does not exists
            search_doc = {'page': clickdata['pageurl']}
            update_doc = {'$push': {'datapoints': {'x': clickdata['datapoint']['x'],
                                                   'y': clickdata['datapoint']['y'],
                                                   'value': 1}}}
            option_doc = {'upsert': True}

            try:
                self.collection.find_and_modify(search_doc, update_doc, option_doc)
            except pymongo.errors.OperationFailure:
                print "Mongodb operationFailure db: remote"
                return False

        return True

    def get_clickdata(self, pageurl):
        # get the dataset for url
        try:
            doc = self.collection.find_one({'page': pageurl})
        except:
            print "Mongodb error"
            return None

        if doc is not None:
            return doc['datapoints']
        else:
            return None
