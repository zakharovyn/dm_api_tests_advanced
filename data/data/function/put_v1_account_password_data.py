from datetime import datetime


class PutV1AccountPasswordData:
    """Класс данных для теста PutV1AccountPassword"""
    __date = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    new_password = str(f'NewPassWord{__date}')