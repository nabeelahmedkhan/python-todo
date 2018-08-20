from app import app,mongo,jsonify,request,json , Blueprint
from flask_pymongo import PyMongo , pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId
todo_app = Blueprint('todo_app',__name__)
@todo_app.route("/")
def index():
    return 'ToDo App'
'''get all tasks''' 
@todo_app.route("/tasks/", methods = ['GET'])
def get_all_tasks():
    data = []
    db_task = mongo.db.tododb
    if db_task.count_documents({}) > 0:
        for task in db_task.find().sort('sorted',pymongo.DESCENDING):
            id = json.loads(dumps(task['_id']))
            data.append(
                {
                    "id": id["$oid"], 
                    "title": task["title"], 
                    "description": task["description"], 
                    "done": bool(task["done"])
                }
            )
        return jsonify({'tasks':data}),200
    else:
        return jsonify({'TodoList':'Todo list is empty'}), 204

'''get specific task'''
@todo_app.route("/task/<task_id>", methods = ['GET'])
def get_task(task_id):
    db_task = mongo.db.tododb
    data = []
    for tasks in db_task.find():
        id = json.loads(dumps(tasks['_id']))
        if task_id in id['$oid']:
            task = db_task.find_one({"_id": ObjectId(task_id)})    
            id = json.loads(dumps(task['_id']))
            data.append(
                {
                    "_id": id["$oid"], 
                    "title": task["title"], 
                    "description": task["description"], 
                    "done": task["done"]   
                }
            )
            return jsonify({'tasks':data}), 200
        

    return jsonify({"Error ": "task is not in list"}), 404 
   
'''create new task''' 
@todo_app.route("/task/", methods = ['POST'])
def create_tasks():
    data = request.get_json(silent=True)
    db_task = mongo.db.tododb
    new_task = db_task.insert(
            {
                'title': data['title'], 
                "description": data['description'], 
                "done": bool(data['done'])
            }
        ) # bool()
    return jsonify({'Created data successfuly ': 'yahooo!!!',
                    'title':data['title'],
                    'description':data['description'],
                    'done':data['done'] 
                    }) , 201

'''update existing task'''
@todo_app.route("/task/<ObjectId:task_id>", methods = ['PUT'])
def update_task(task_id):
    db_task = mongo.db.tododb
    task = db_task.find_one_or_404({"_id": task_id})
    title = request.get_json("title", task["title"])
    description = request.get_json('description', task["description"])
    done = bool(request.get_json("done", task["done"]))
    task["title"] = title
    task["description"] = description
    task["done"] = done
    db_task.save(task)
    response = {
                    'updated data is': 'successfully ', 
                    'title': title, 
                    'description': description,
                    'done': bool(done)
                }

    return jsonify({'response': 'response'}) , 200

'''delete specific task'''
@todo_app.route("/task/<ObjectId:task_id>", methods = ['DELETE'])
def delete_task(task_id):
    mongo.db.tododb.find_one_or_404({"_id": task_id})
    mongo.db.tododb.delete_one({"_id": task_id})
    response = {'status': 'task has been deleted'}
    return jsonify({'response': response}),200