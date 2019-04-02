from flask import Blueprint

#the second param defines its related path
#url_prefix make all the url add 'auth', such as 'auth/login'
auth = Blueprint('auth', __name__, url_prefix='/auth')


from . import view
