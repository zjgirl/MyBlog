from flask import Flask
from .db import db    #. means the same path
from flask_bootstrap import Bootstrap #html 
from flask_login import LoginManager
from config import Config

bootstrap = Bootstrap()
login_manager = LoginManager() 
login_manager.login_view = 'auth.register'#if try accessing secure, redirect to the defined page

#app factory, use app to solve requests from client
def create_app():
    app = Flask(__name__) #create an app
    
    #config the app
    app.config.from_object(Config) #load the config
    
    db.init_app(app) #create a sql   
    bootstrap.init_app(app)
    login_manager.init_app(app)
    
    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp)
    from .main.index import main_bp
    app.register_blueprint(main_bp)
    
    app.add_url_rule('/',endpoint='auth.login')

    
    return app



        
    


    
    
