from flask import Flask
from app.db.db import mongo
from app.config import Config
from app.routes.userroutes import users_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    mongo.init_app(app)
    with app.app_context():
        mongo.db.users.create_index("email", unique=True)

    
    app.register_blueprint(users_bp)
    
    return app
