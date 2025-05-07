from generic.utilites.rand_utils import generate_password


class PutV1AccountPasswordData:
    """Класс данных для теста PutV1AccountPassword"""
    new_password = generate_password()
