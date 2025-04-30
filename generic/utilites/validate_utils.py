from requests import Response, JSONDecodeError
from pydantic import BaseModel


def validate_status_code(response: Response, status_code: int):
    """
    Проверка того, что полученный статус код ответа равен ожидаемому.
    :param response:
    :param status_code:
    :return:
    """
    assert response.status_code == status_code, \
        (
            f'Статус код ответа должен быть равен {status_code=}, а он равен '
            f'{response.status_code=}'
        )


def validate_request_json(json: str | BaseModel):
    if isinstance(json, dict):
        return json
    return json.model_dump(by_alias=True, exclude_none=True)


def validate_model(response: Response, obj_model):
    list_obj = []
    try:
        if type(response.json()) == list:
            for item in response.json():
                obj = obj_model(**item.json())
                list_obj.append(obj)
            return list_obj
        else:
            return obj_model(**response.json())
    except JSONDecodeError:
        return response


def validate_model_response(response: Response, obj_model, status_code: int):
    if response.status_code == status_code and response.status_code < 300:
        return validate_model(response=response, obj_model=obj_model)
    else:
        return response
