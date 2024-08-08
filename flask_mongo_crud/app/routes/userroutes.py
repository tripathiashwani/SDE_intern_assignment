
from flask import Blueprint
from app.views.userviews import UserAPI

users_bp = Blueprint('users', __name__, url_prefix='/users')

users_bp.add_url_rule('/', view_func=UserAPI.as_view('create_user'), methods=['POST'])
users_bp.add_url_rule('/', view_func=UserAPI.as_view('get_users'), methods=['GET'])
users_bp.add_url_rule('/<user_id>', view_func=UserAPI.as_view('get_user'), methods=['GET'])
users_bp.add_url_rule('/<user_id>', view_func=UserAPI.as_view('update_user'), methods=['PUT'])
users_bp.add_url_rule('/<user_id>', view_func=UserAPI.as_view('delete_user'), methods=['DELETE'])
