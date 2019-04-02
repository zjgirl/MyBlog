from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


#define user table
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.INTEGER, primary_key = True, autoincrement = True)
    username = db.Column(db.String(128), unique = True)
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128), nullable = False) #can't be null

    #define some related func there
    #define static method
    @staticmethod
    def addUser(username, password):
        newuser = User(username = username, password = password) #password1 will pass to the password()
        db.session.add(newuser)
        db.session.commit()

    #@property change a method to property, at the same time create a @password.setter
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

  
        
class blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.INTEGER, primary_key = True, autoincrement = True)
    content = db.Column(db.TEXT, nullable = False)
    author_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))


from . import login_manager

#this propriety registe the func to Flask_Login, the func will be loaded when we need to know the info of the current user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



#db.create_all()





    
    
    
