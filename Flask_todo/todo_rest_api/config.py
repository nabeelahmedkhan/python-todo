from app import app
DEBUG = True
app.config['MONGO_DBNAME'] = 'todoapi'
app.config['MONGO_URI'] = 'mongodb://admin:nabeel123@ds123532.mlab.com:23532/todoapi'
app.config['SECRET_KEY'] = 'jababababajaja123'
