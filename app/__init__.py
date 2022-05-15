from flask import Flask
import sqlalchemy
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap



db = SQLAlchemy
bootstrap = Bootstrap

#Initialising the apllication

def create_app(config_name):
    app = Flask(__name__)
    #creating the app configurations
    app.config.from_object(config_options[config_name])      
    
    #initializing flask extensions
    db.init_app(app)
    
    #registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)




    return app