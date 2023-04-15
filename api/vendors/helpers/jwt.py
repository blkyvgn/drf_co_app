from django.conf import settings
from api.vendors.helpers.token import get_random_string
from datetime import (
    datetime,
    timedelta,
)
from django.utils.timezone import (
    timedelta,
    now,
)
import jwt


def get_access_token(payload):
    return jwt.encode(
        {'exp': datetime.now() + timedelta(minutes=15), **payload},
        settings.SECRET_KEY,
        algorithm='HS256'
    )

def get_refresh_token():
    return jwt.encode(
        {'exp': datetime.now() + timedelta(days=365), 'data':get_random_string(15)},
        settings.SECRET_KEY,
        algorithm='HS256'
    )

def verify_token(token):
    decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
    except Exception:
        return None

    exp = decoded_data['exp']
    if datetime.now().timestamp() > exp:
        return None 

    return decoded_data

def validate_request(headers):
    authorization = headers.get('Authorization', None)
    if not authorization:
        # raise Exception('Token is not exist')
        return None
    # token = headers['Authorization'][7:]
    token = headers['Authorization'].split(' ')[1]
    decoded_data = verify_token(token)

    if not decoded_data:
        # raise Exception('Token not valid of as expired')
        return None

    return decoded_data