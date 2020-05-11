from werkzeug.security import safe_str_cmp
from user import User

#in memory table of users:
users = [ User(1,'bob','asdf')]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}
# that ^ replace this:
#userid_mapping = { 1 : {
        #'id':1,
        #'username' : 'bob',
        #'password' : 'asdf'
    #}
#}

#authenticate the user:

def authenticate(username, password):
    # find the user according to username passed on the api request:
    user = username_mapping.get(username, None)
    # safe_str_cmp is a safe string compare tool that replace the practice of user.password == password
    # if user found, make sure his DB password match the api request passsword:
    if user and safe_str_cmp(user.password,password):
        return user

def identity(paylod):
    user_id = payload['identity']
    return user_id_mapping.get(user_id, None)
