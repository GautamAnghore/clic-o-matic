from flask import redirect, url_for


# ------------------------------------------------------------
# source : http://arusahni.net/blog/2014/03/flask-nocache.html
# defination of nocache decorator
from datetime import datetime
from flask import make_response
from functools import update_wrapper


def no_cache(f):
    def new_func(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        # resp.cache_control.no_cache = True
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(new_func, f)
# ------------------------------------------------------------


from sessions import *
sessions = Sessions()


def login_required(f):
    def new_func(*args, **kwargs):
        if sessions.logged_in() is not None:
            # user is logged in
            return f(*args, **kwargs)

        else:
            # flag : stage 3
            # flag : bug [ provide proper alert for invalid access ]

            return redirect(url_for('master.index'))

    return update_wrapper(new_func, f)
