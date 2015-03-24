from flask import request, redirect, url_for
from flask.ext.cors import cross_origin

from apps.remote import remote

from apps import login_required
from apps import database
from apps.users.db import User
from apps import Sessions

import db

sessions = Sessions()
user = User(database)
remoteDb = db.Remote(database)


@remote.route('/remotedata', methods=['POST'])
@cross_origin(origins='*')
def remotedata():
    if request.json is not None:
        remoteDb.add_clickdata(request.json)
        return 'data posted'
    else:
        return 'error in server, data not posted'


@remote.route('/cleardata', methods=['GET'])
@login_required
def cleardata():
    if 'url' in request.args:
        # delete the datapoints
        check = user.get_user_pages(request.args['url'], sessions.logged_in())
        if check is not None:
            remoteDb.delete_clickdata(request.args['url'])

        return redirect(url_for('dashboard.dashboard_index', url=request.args['url']))
    else:
        return redirect(url_for('dashboard.dashboard_index'))
