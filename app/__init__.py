from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()  # Create db object globally


def create_app():
    load_dotenv()

    app = Flask(__name__)
    CORS(app, 
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE"])

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)
    from app.routers.auth import auth_bp
    from app.routers.files import files_bp
    from app.routers.folders import folders_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(files_bp,url_prefix='/files')
    app.register_blueprint(folders_bp,url_prefix='/folders')
    
    # with app.app_context():
    #     from app.models import file,folder,user
    #     db.create_all()

    return app

'''

'''