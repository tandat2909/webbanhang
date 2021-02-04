from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from API import config
from flask_login import LoginManager
app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
login = LoginManager(app)