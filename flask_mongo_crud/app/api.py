

from flask import request, jsonify
from flask.views import MethodView
from app.db.user_dao import UserDAO
from app.cache.cache_manager import CacheManager
from bson.objectid import ObjectId
import json

user_dao = UserDAO()
cache_manager = CacheManager()

class UserAPI(MethodView):

    def post(self):
        data = request.get_json()
        email = data.get("email")

        if cache_manager.get_cache(email):
            return jsonify({"error": "User with this email already exists msg from redis"}), 400

        existing_user = user_dao.get_user_by_email(email)
        if existing_user:
            cache_manager.set_cache(email, str(existing_user['_id']))
            return jsonify({"error": "User with this email already exists"}), 400

        user_id = user_dao.create_user(data)
        cache_manager.set_cache(email, str(user_id))
        cache_manager.delete_cache('all_users')

        return jsonify({"message": "User created", "id": str(user_id)}), 201

    def get(self, user_id=None):
        if user_id:
            cached_user = cache_manager.get_cache(f"user:{user_id}")
            if cached_user:
                return jsonify(json.loads(cached_user)), 200

            user = user_dao.get_user_by_id(user_id)
            if user:
                user['_id'] = str(user['_id'])
                cache_manager.set_cache(f"user:{user_id}", json.dumps(user))
                return jsonify(user), 200

            return jsonify({"error": "User not found"}), 404
        else:
            cached_users = cache_manager.get_cache('all_users')
            if cached_users:
                return jsonify(json.loads(cached_users)), 200

            users = user_dao.get_all_users()
            result = []
            for user in users:
                user['_id'] = str(user['_id'])
                result.append(user)

            cache_manager.set_cache('all_users', json.dumps(result))
            return jsonify(result), 200

    def put(self, user_id):
        data = request.json
        if not data:
            return jsonify({'error': 'Bad Request', 'message': 'No data provided'}), 400

        result = user_dao.update_user(user_id, data)
        if result.matched_count == 0:
            return jsonify({'error': 'Not Found', 'message': 'User not found'}), 404

        cache_manager.delete_cache('all_users')
        cache_manager.delete_cache(f"user:{user_id}")

        return jsonify({'message': 'User updated'}), 200

    def delete(self, user_id):
        result = user_dao.delete_user(user_id)
        if result.deleted_count == 0:
            return jsonify({'error': 'Not Found', 'message': 'User not found'}), 404

        cache_manager.delete_cache('all_users')
        cache_manager.delete_cache(f"user:{user_id}")

        return jsonify({'message': 'User deleted'}), 200
