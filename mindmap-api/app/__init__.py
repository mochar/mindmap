from flask import Flask
from flask_cors import CORS
from app.scripts.euretos import Euretos

app = Flask(__name__)
app.config.from_object('config')
CORS(app)
euretos = Euretos(app.config['EURETOS_CONFIG'])

from app import views
