from datetime import datetime
from uuid import uuid4


def get_random_string(length: int = 16):
    if type(length) != int or length < 0 or length > 32:
        raise ValueError("Длина - целое число от 0 до 32 включительно")
    date = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    return date + '_' + str(uuid4()).replace("-", "")[0:length]


def generate_user_name():
    return f'TestUserName_{get_random_string(length=12)}'


def generate_user_email():
    return f'TestUserName_{get_random_string(length=12)}' + '@email.com'


def generate_password():
    return get_random_string(16)
