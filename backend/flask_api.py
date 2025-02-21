from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
CORS(app)

try:
    mongodb_client = PyMongo(app)
    db = mongodb_client.db
    print("Connect to mongodb successfully")
except Exception as e:
    print("Error connect to mongodb:", str(e))

@app.route('/add', methods=['POST'])
def add_data():
    try:
        data = request.json
        result = db.User.insert_one(data)
        return jsonify({"message": "success", "_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"message": "error", "error details": str(e)}), 400

@app.route('/get/<id>', methods=['GET'])
def get_data(id):
    data = db.User.find_one({"_id": ObjectId(id)})
    if data:
        return jsonify({"_id": str(data["_id"]), "data": data})
    return jsonify({"error": "User not found"}), 404

@app.route('/delete/<id>', methods=['DELETE'])
def delete_data(id):
    data = db.User.delete_one({"_id": ObjectId(id)})
    if data:
        return jsonify({"message": "Delete user successfully"})
    return jsonify({"error": "USer not found"}), 404

@app.route('/update/<id>', methods=['PUT'])
def update_data(id):
    try:
        data = request.json
        db.User.update_one({"_id": ObjectId(id)}, {"$set": data})
        return jsonify({"message": "Update user successfully", "data": data}), 200
    except Exception as e:
        return jsonify({"message": "error", "error details": str(e)}), 400

@app.route('/getAll', methods=['GET'])
def get_all_data():
    data = db.User.find()
    results = []
    for item in data:
        item['_id'] = str(item['_id'])
        results.append(item)
    return jsonify(results)

if __name__ == '__main__':
   app.run(debug=True, use_reloader=False)