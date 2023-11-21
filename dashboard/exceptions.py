# class ConfigDataNotFoundException(Exception):
#     def __init__(self, key: str = None):
#         self.__key = key
#
#     def __str__(self):
#         if self.__key:
#             return f'Required key "{self.__key}" not found in data.json.'
#         else:
#             return f'Required key not found in data.json.'