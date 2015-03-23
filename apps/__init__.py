from flask import Flask
from config import Config
from flask import Blueprint

# for mongo db operations
import pymongo

app = Flask(__name__)
app.config.from_object(Config)

# database settings
connection = pymongo.MongoClient('localhost', 27017)
database = connection.clicomatic

# import sessions to be included further
from sessions import Sessions
# import decorators to be included further
from decorators import no_cache, login_required

# create master blueprint
master = Blueprint('master', __name__, template_folder='templates', static_folder='static')
from views import *

# import users blueprint
from users import users

app.register_blueprint(master)
app.register_blueprint(users)
