from flask import request

from apps.remote import remote

from apps import database

import db

remoteDb = db.Remote(database)


@remote.route('/remotedata', methods=['POST'])
def remotedata():
    if request.json is not None:
        remoteDb.add_dump(request.json)
