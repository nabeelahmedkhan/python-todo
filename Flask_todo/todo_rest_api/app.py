from flask import Flask,request,jsonify,json
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_restful import Resource,Api

app = Flask(__name__)
app.config.from_pyfile('config.py')
api = Api(app)
mongo = PyMongo(app)
from views import *    

app.run( port=3000)