
from bson.objectid import ObjectId
from app.db.db import mongo

class UserDAO:
    def get_user_by_email(self, email):
        return mongo.db.users.find_one({"email": email})

    def get_user_by_id(self, user_id):
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})

    def get_all_users(self):
        return list(mongo.db.users.find())

    def create_user(self, data):
        return mongo.db.users.insert_one(data).inserted_id

    def update_user(self, user_id, data):
        return mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': data})

    def delete_user(self, user_id):
        return mongo.db.users.delete_one({'_id': ObjectId(user_id)})
