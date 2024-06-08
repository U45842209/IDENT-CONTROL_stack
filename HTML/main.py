from classes import SQL_connect, Cache
from bottle import route, run, template, request, response, error
from dotenv import load_dotenv, find_dotenv
import os
import redis
import bottle_session
import bottle_redis
import bottle
import json
import hashlib

load_dotenv(find_dotenv())


# https://pypi.org/project/bottle-session/
app = bottle.app()
session_plugin = bottle_session.SessionPlugin(cookie_lifetime=600)
redis_plugin = bottle_redis.RedisPlugin()

connection_pool = redis.ConnectionPool(host='172.20.0.30', port=6379, password=os.environ.get("PASS"))

session_plugin.connection_pool = connection_pool
redis_plugin.redisdb = connection_pool
app.install(session_plugin)
app.install(redis_plugin)

bottle.TEMPLATE_PATH.append(f"./templates/")
print(f"Templates path : {bottle.TEMPLATE_PATH}")


@route('/', method='GET')
def index_login(session, rdb, message="", message_type=""):
    token = request.get_cookie("token")
    if token:
        payload = Cache.Caching().verify_token(token)
        if payload["username"]:
            bottle.redirect(f"/dashboard/{payload['username']}")
    else:
        return template('index', message=message, message_type=message_type)


@route('/login', method='POST')
def login_POST():
    username = request.forms.get('username')
    password = request.forms.get('password').encode('utf-8')
    hashed_password = hashlib.sha256(password).hexdigest()
    token = Cache.Caching().generate_token(username)
    response.set_cookie("token", token, httponly=True, samesite='None')
    if SQL_connect.Mysql().authenticate_user(username, hashed_password):
        bottle.redirect(f"/dashboard/{username}")
    else:
        bottle.redirect("/error/401")


@route('/login', method='GET')
def login_GET():
    token = request.get_cookie("token")
    if token:
        payload = Cache.Caching().verify_token(token)
        if payload["username"]:
            bottle.redirect(f"/dashboard/{payload['username']}")
    else:
        bottle.redirect("/error/401")


@route('/register', method='POST')
def do_register(session, rdb):
    Cache.Caching().get_basic_info(session, rdb)
    username = request.forms.get('username')
    password = request.forms.get('password').encode('utf-8')
    hashed_password = hashlib.sha256(password).hexdigest()
    email = request.forms.get('email')
    if not bool(SQL_connect.Mysql().find_user(username)) and not bool(SQL_connect.Mysql().find_email(email)):
        if SQL_connect.Mysql().register_user(username, hashed_password, email) == "success":
            return index_login(session, rdb, message_type="success", message="You succefully created an account")
        else:
            return index_login(session, rdb, message_type="error", message="There was an error during the creation process")
    else:
        return index_login(session, rdb, message_type="info", message="User already exist or email already used")


@route('/dashboard/<username>', method='GET')
def dashboard(username):
    token = request.get_cookie("token")
    if token:
        payload = Cache.Caching().verify_token(token)
        if payload['username'] == username:
            return template("dashboard", username=payload['username'], email=payload['email'], ListContent=None)
        else:
            bottle.redirect("/error/401")
    else:
        bottle.redirect("/error/401")


@route('/dashboard/<username>', method='POST')
def dashboard(username):
    token = request.get_cookie("token")
    try:
        request.forms.get("List")
        ListContent = SQL_connect.Mysql().get_all_user_info()
    except Exception as e:
        ListContent = None
    if token:
        payload = Cache.Caching().verify_token(token)
        if payload['username'] == username:
            return template("dashboard", username=payload['username'], email=payload['email'], ListContent=ListContent)
        else:
            bottle.redirect("/error/401")
    else:
        bottle.redirect("/error/401")


@route('/logout', method='POST')
def logout():
    token = request.get_cookie("token")
    if token:
        response.set_cookie("token", token, max_age=0)
        bottle.redirect("/")
    else:
        bottle.redirect("/error/400")


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
