from flask import Blueprint

remote = Blueprint('remote', __name__)

from views import *