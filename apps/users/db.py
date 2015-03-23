import pymongo
from passlib.hash import pbkdf2_sha256


class User():

    def __init__(self, database):
        self.db = database
        self.users = database.users

    def secure_password(self, password):
        hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
        return hash

    def add_user(self, username, password, fullName, email=None):
        safe_password = self.secure_password(password)

        user = {'_id': username, 'password': safe_password, 'pages': []}

        if email is not None:
            user['email'] = email

        try:
            self.users.insert(user, safe=True)
        except pymongo.errors.DuplicateKeyError:
            print "duplicate user"
            return False
        except pymongo.errors.OperationFailure:
            print "Operation Failure"
            return False

        return True

    def check_user(self, username, password):

        user = None

        try:
            user = self.users.find_one({'_id': username})
        except:
            return None

        if user is None:
            return None

        if pbkdf2_sha256.verify(password, user['password']):
            return user
        else:
            return None

    def get_user(self, username):

        try:
            user = self.users.find_one({'_id': username})
        except:
            print "pymongo error : cannot find user"
            return None

        return user

    def add_page(self, username, pageurl):

        try:
            self.users.update({'username': username},
                              {'$addToSet': {'pages': pageurl}})
        except pymongo.errors.OperationFailure:
            print "pymongo error : cannot insert page url"
            return False

        return True

    def check_page_exists(self, pageurl):
        try:
            page = self.users.find_one({'pages': pageurl})
        except:
            print "pymongo error: page does not exists"
            return False

        if page is not None:
            return True
        else:
            return False
