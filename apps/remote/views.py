from flask import request
from flask.ext.cors import cross_origin

from apps.remote import remote

from apps import database

import db

remoteDb = db.Remote(database)


@remote.route('/remotedata', methods=['POST'])
@cross_origin(origins='*')
def remotedata():
    if request.json is not None:
        remoteDb.add_dump(request.json)
        return 'data posted'
    else:
        return 'error in server, data not posted'
