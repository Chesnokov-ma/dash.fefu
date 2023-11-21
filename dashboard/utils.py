import json


def json_to_dict(file_name: str) -> dict:
    """Перевод из json в python.dict"""
    return json.load(open(file_name, 'r'))
