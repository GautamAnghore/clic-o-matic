from flask import Flask
from config import Config
from flask import Blueprint

app = Flask(__name__)

app.config.from_object(Config)

master = Blueprint('master', __name__, template_folder='templates', static_folder='static')
from views import *

app.register_blueprint(master)
