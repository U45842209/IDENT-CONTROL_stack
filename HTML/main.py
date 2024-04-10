import bottle
from bottle import route, run, template, SimpleTemplate, request
import json


bottle.TEMPLATE_PATH.append(f"./templates/")
print(f"Templates path : {bottle.TEMPLATE_PATH}")


@route('/hello/<name>')
def hello_test(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@route('/template/<name>')
def template_test(name='World'):
    return template('hello_template', name=name)

@route('/')
def index_login():
    return template('index')


@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if username==username and password=="password":
        return template("<p>You have logged in successfuly, {{username}}, {{password}}</p>", username=username, password=password)
    else:
        return http_error(401)


@route('/register', method='POST')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if username == username and password == "password":
        return template("<p>You have logged in successfuly, {{username}}, {{password}}</p>", username=username, password=password)
    else:
        return http_error(401)


@route('/error/<error_code:int>')
def http_error(error_code):
    # Load and parse the JSON file
    with open("error_codes.json") as f:
        http_errors = json.load(f)

    # Initialize error_description with a default value
    error_description = "Unknown Error"

    # Find the error code in the JSON data
    for category, codes in http_errors.items():
        if str(error_code) in codes:
            error_description = codes[str(error_code)]
            break

    # Return the error template with the error code and description
    return template("errors", error_code=error_code, error_description=error_description)


run(host='localhost', port=8080)
