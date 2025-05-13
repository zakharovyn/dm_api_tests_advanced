import random
from datetime import datetime
from string import ascii_letters, digits
from uuid import uuid4


def get_random_string(length: int = 16):
    if type(length) != int or length < 0 or length > 32:
        raise ValueError("Длина - целое число от 0 до 32 включительно")
    date = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    return date + '_' + str(uuid4()).replace("-", "")[0:length] + '!'


def generate_user_name():
    return f'TestName_{get_random_string(length=8)}'


def generate_user_email():
    return f'Test_{get_random_string(length=8)}' + '@email.com'


def generate_password():
    return get_random_string(12)


def random_string(begin: int = 1, end: int = 30):
    symbols = ascii_letters + digits
    string = ''
    for _ in range(random.randint(begin, end)):
        string += random.choice(symbols)
    return string
