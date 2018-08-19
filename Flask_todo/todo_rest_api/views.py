from app import app,mongo,jsonify,request,json
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

@app.route("/")
def index():
    return 'ToDo App'

@app.route("/todo/api/v1.0/tasks/", methods = ['GET'])
def get_all_tasks():
    data = []
    db_task = mongo.db.tododb
    if db_task.count_documents({}) > 0:
        for task in db_task.find():
            data.append({"id": str(task["_id"]), "title": task["title"], "description": task["description"], "done": task["done"]})
    return jsonify({'tasks':data})


@app.route("/todo/api/v1.0/task/<task_id>", methods = ['GET'])
def get_task(task_id):
    data = []
    task = mongo.db.tododb.find_one_or_404({"_id": ObjectId(task_id)})
    data.append({"id": str(task["_id"]), "title": task["title"], "description": task["description"], "done": task["done"]})
    return jsonify({'tasks':data}) , 404


@app.route("/todo/api/v1.0/task/", methods = ['POST'])
def create_tasks():
    data = request.get_json(silent=True)
    db_task = mongo.db.tododb
    new_task_id = db_task.insert({
        'title': data['title'], 
        "description": data['description'], 
        "done": bool(data['done'])
        }
    ) # bool()
    
    return jsonify({'Created data successfuly ': str(new_task_id)}) , 201


@app.route("/todo/api/v1.0/task/<ObjectId:task_id>", methods = ['PUT'])
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
    response = {'status': 'success', 'status_code': '200', 'message': 'Task Updated'}

    return jsonify({'response': response})


@app.route("/todo/api/v1.0/task/<ObjectId:task_id>", methods = ['DELETE'])
def delete_task(task_id):
    mongo.db.tododb.find_one_or_404({"_id": task_id})
    mongo.db.tododb.delete_one({"_id": task_id})
    response = {'status': 'success', 'status_code': '200', 'message': 'Task Deleted'}
    return jsonify({'response': response})
