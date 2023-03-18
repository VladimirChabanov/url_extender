from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
app.db_connection = None

from app import views
