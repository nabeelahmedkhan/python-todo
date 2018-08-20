from flask import Flask,request,jsonify,json,Blueprint
from flask_pymongo import PyMongo,pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
app.config.from_pyfile('config.py')
mongo = PyMongo(app)
from views import * 
app.register_blueprint(todo_app,url_prefix='/todo/api/v1.0')
app.run( port=3000)