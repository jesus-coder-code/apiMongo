from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/apiMongo'

mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create():
    email = request.json['email']
    user = request.json['user']
    password = request.json['password']
    
    if email and user and password:
        id = mongo.db.users.insert(
            {'email': email, 'user': user, 'password': password}
        )
        return {"message":"done"}
    else:
        return {"message":"please fill all fields"}

@app.route('/users', methods=['GET'])
def get_data():
    data = mongo.db.users.find()
    response = json_util.dumps(data)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id':ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['DELETE'])
def delete(id):
    user = mongo.db.users.delete_one({'_id':ObjectId(id)})
    return {'message':'user was deleted'}

@app.route('/users/<id>', methods=['PUT'])
def update(id):
    email = request.json['email']
    user = request.json['user']
    password = request.json['password']

    if email and user and password:
        mongo.db.users.update_one({'_id':ObjectId(id)}, {'$set':{
            'email': email,
            'user': user,
            'password': password
        }}) 
        response = jsonify({'message':'user was updated successfully'})
        return response


if __name__ == "__main__":
    app.run(debug=True)