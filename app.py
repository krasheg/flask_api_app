from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps

# create app
app = Flask(__name__)

# create database connection

client = MongoClient('mongo', 27017)
db = client.mongodb


@app.route('/api/create', methods=['POST'])
def create():
    """ create new key:value pair and save it to db """
    data = request.get_json()
    db.values.insert_one(data)
    return jsonify({'message': 'Value created successfully!'}), 201


@app.route('/api/read', methods=['GET'])
def read():
    """read all objects in database"""
    data = db.values.find()
    return dumps(data)


@app.route('/api/read/<string:key>', methods=['GET'])
def read_by_key(key):
    """returns object by key"""
    data = db.values.find({'key': key})
    if data:
        return dumps(data)
    return jsonify({"message": f'object with key {key} doesn`t exist'}), 404


@app.route('/api/update', methods=['PUT'])
def update():
    """updates object in database"""
    data = request.get_json()
    db.values.update_one({'key': data['key']}, {'$set': {'value': data['value']}})
    return jsonify({'message': 'Value updated successfully!'}), 204


# run
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
