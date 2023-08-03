from flask import Flask
from api import api
from flask_cors import CORS
from dotenv import load_dotenv
from initiate_packages import db
import os 
load_dotenv()

def createApp(testing):
    
    app = Flask(__name__)
    if(testing == True): 
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
    else:
        print("data base info " , f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    db.init_app(app)
    CORS(app)
    app.register_blueprint(api)
    with app.app_context(): 
        db.create_all()
    return app