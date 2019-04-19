from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from datetime import datetime
import bleach
from markdown import markdown

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model): 
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    default = db.Column(db.Boolean, default = False, index = True) # build index to look for
    permission = db.Column(db.Integer)
    
    #relationship join two tables, you can find another table easily by it
    #backref defines the back ralationship, you can find Role table by role obj
    user = db.relationship('User', backref = 'role', lazy = 'dynamic') #define the relationship between Role and User table

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs) #find Role's father to init
        if self.permission is None: #the permission is None when first defined, so set it to 0
            self.permission = 0
            
    def add_permission(self, perm): #self
        if not self.has_permission(perm):
            self.permission += perm #the permission is added by add
            
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permission -= perm
            
    def has_permission(self, perm):
        return self.permission & perm == perm # & operation, even a none binary number can use it 
        
    def reset_permission(self):
        self.permission = 0

    # insert 3 roles to the Role table
    @staticmethod
    def insert_role():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderate' : [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:      
            role = Role.query.filter_by(name=r).first() # look for the table first, insert role by update
            if role == None:              
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (default_role == r)
            db.session.add(role)
        db.session.commit()
                
                

#define user table
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.INTEGER, primary_key = True, autoincrement = True)
    username = db.Column(db.String(128), unique = True)
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128), nullable = False) #can't be null
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default = datetime.utcnow) #register time
    last_seen = db.Column(db.DateTime(), default = datetime.utcnow)

    avatar = db.Column(db.String(128))

    post = db.relationship('Post', backref='author', lazy='dynamic') # build relationship with Post
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first() #allocate role, not create new
        if self.email:
            self.avatar = self.generate_avatar()

    #define some related func there
    #define static method
    @staticmethod
    def addUser(username, password, email):        
        newuser = User(username = username, password= password, email=email) #password1 will pass to the password()
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

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)
    
    def ping(self): #update the last_seen time
        self.last_seen = datetime.utcnow() #current time
        db.session.add(self)
        db.session.commit()

    def generate_avatar(self, size=256, default='identicon', rating='g'):
        if self.email is not None and (self.avatar is None or size!=256):
            import hashlib
            url = 'https://cdn.v2ex.com/gravatar'
            hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
            return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url,hash=hash,size=size,default=default,rating=rating)
            
    
# define this class, we don't need to see whether user is login when we want to check his perm
class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False
    def is_administrator(self):
        return False
 
login_manager.anonymous_user = AnonymousUser
  
        
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.INTEGER, primary_key = True, autoincrement = True)
    body = db.Column(db.TEXT, nullable = False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))

    body_html = db.Column(db.TEXT) #for markdown text

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = [ 'a', 'p', 'h1', 'h2', 'h3', 'abbr', 'acronym', 'b', 'blockquote', 'code',
        'em', 'i', 'li', 'ul', 'ol', 'pre', 'strong']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                            tags=allowed_tags, strip=True))
                            
from . import login_manager

#this propriety registe the func to Flask_Login, the func will be loaded when we need to know the info of the current user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



#db.create_all()
db.event.listen(Post.body, 'set', Post.on_changed_body)




    
    
    
