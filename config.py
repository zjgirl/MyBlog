#instore the app configuration
class Config:
    DEBUG = True
    SECRET_KEY = "dev"
    #link mysql
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/flaskdb?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    @staticmethod
    def init_app(app):
        pass
    

