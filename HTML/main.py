from classes import SQL_connect
from bottle import route, run, template, request
import bottle_session
import bottle
import json
import hashlib


# https://pypi.org/project/bottle-session/
app = bottle.app()
plugin = bottle_session.SessionPlugin(cookie_lifetime=600)
app.install(plugin)

bottle.TEMPLATE_PATH.append(f"./templates/")
print(f"Templates path : {bottle.TEMPLATE_PATH}")


@route('/')
def index_login(message="", message_type=""):
    return template('index', message=message, message_type=message_type)


@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password').encode('utf-8')
    hashed_password = hashlib.sha256(password).hexdigest()
    if bool(SQL_connect.Mysql().find_user(username)):
        info = SQL_connect.Mysql().get_user_info(username)
        if username == username and hashed_password == hashed_password:
            return template("dashboard", username=info[0][1], password=info[0][2], email=info[0][3])
    else:
        return http_error(401)


@route('/register', method='POST')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password').encode('utf-8')
    hashed_password = hashlib.sha256(password).hexdigest()
    email = request.forms.get('email')
    if not bool(SQL_connect.Mysql().find_user(username)) and not bool(SQL_connect.Mysql().find_email(email)):
        if SQL_connect.Mysql().register_user(username, hashed_password, email) == "success":
            return index_login(message_type="success", message="You succefully created an account")
        else:
            return index_login(message_type="error", message="There was an error during the creation process")
    else:
        return index_login(message_type="info", message="User already exist or email already used")


@route('/error/<error_code:int>')
def http_error(error_code):
    with open("error_codes.json") as f:
        http_errors = json.load(f)
    error_description = "Unknown Error"
    for category, codes in http_errors.items():
        if str(error_code) in codes:
            error_description = codes[str(error_code)]
            break
    return template("errors", error_code=error_code, error_description=error_description)


run(host='0.0.0.0', port=8080)
