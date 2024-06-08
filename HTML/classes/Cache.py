from . import SQL_connect
import jwt
import random
import string
from datetime import datetime, timedelta

class Caching:

    def get_basic_info(self, session, rdb):
        rdb.incr('visitors')
        visitor = rdb.get('visitors')
        last_visit = session['visit']
        session['visit'] = datetime.now().isoformat()
        with open("dump", "a") as file:
            file.write('\nYou are visitor %s, your last visit was on %s' % (visitor, last_visit))
            file.close()

    def generate_token(self, username):
        info = SQL_connect.Mysql().get_user_info(username)
        expiration_time = datetime.now() + timedelta(hours=1)
        salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        payload = {
            "username": info[0][1],
            "email": info[0][3],
            "exp": expiration_time,
            "salt": salt
        }
        secret_key = "SECRET_KEY" + salt
        return jwt.encode(payload, secret_key, algorithm="HS256")

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            salt = payload.get('salt', '')
            secret_key = "SECRET_KEY" + salt
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token expired
        except jwt.InvalidTokenError:
            return None  # Invalid token
