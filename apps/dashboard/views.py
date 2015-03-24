from flask import render_template, request, redirect, url_for

from apps.dashboard import dashboard

from apps import no_cache, login_required
from apps import database
from apps import Sessions
from apps.users.db import User
from apps.remote.db import Remote

user = User(database)
remotedb = Remote(database)

sessions = Sessions()


@dashboard.route('/dashboard', methods=['GET'])
@no_cache
@login_required
def dashboard_index():
    if 'url' not in request.args:
        # get request does not contain any url
        page_url = user.get_random_url(sessions.logged_in())
        if page_url is not None:
            return redirect(url_for('.dashboard_index', url=page_url))
        else:
            return redirect(url_for('master.index'))
    else:
        page_url = request.args['url']
        url_list = user.get_user_pages(page_url, sessions.logged_in())

        if url_list is not None:
            # page exists
            # get page data
            clickdata = remotedb.get_clickdata(page_url)
            return render_template('dashboard.html', pageurl=page_url, url_list=url_list, clickdata=clickdata, user=sessions.logged_in())
        else:
            return redirect(url_for('.dashboard_index'))
