import sys


class Config:
    def __init__(self, data_dict: dict):
        """
        Получить данные из файла конфигурации.
        Выдать исключение при отсутствии важной информации.
        """

        # <-- Обязательная часть -->
        # Остановка программы при отсутствии данных

        # <-- Необязательная часть -->
        # При отсутствии данных программа продолжит работу
        if 'external_stylesheets' in data_dict:
            self.__external_stylesheets = data_dict['external_stylesheets']


    @property
    def external_stylesheets(self):
        return self.__external_stylesheets