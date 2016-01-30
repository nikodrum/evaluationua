from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'scrt1'

from project import models,database,views,forms