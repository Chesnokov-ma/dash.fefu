from dash import Dash, clientside_callback
from dashboard.dashboard_layout import MainLayout
from dashboard.dash_data_table import DataFilterTypes, DataTable
from dashboard.dash_graph import DashGraph
from dashboard.dash_config import Config
from dashboard.dash_callback import get_callback
from dashboard.utils import *
import dash_auth


"""
========================================================================================
Веб-приложение. Структура:
* Дашборд по контингенту студентов ДВФУ (доступ: все группы)

Примечания:
* /assets должен располагаться в директории с app.py
========================================================================================
"""

# Получение данных из файла конфигурации ../data/config.json
# Остановка программы при отсутствии файла конфигурации или необходимых данных
config = Config(json_to_dict('./data/config.json'))

# Веб-приложение и сервер для запуска через gunicorn
app = Dash(__name__, title='Контингент ДВФУ', external_stylesheets=config.external_stylesheets,
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}])
server = app.server

# Авторизация на сайте по логину и паролю
# auth = dash_auth.BasicAuth(
#     app,
#     {'test': 'qwerty23', 'admin': 'test9'}
# )

# Получение и таблицы с данными в excel-формате
kont_table = DataTable('./data/data.xlsx')

# Глобальный фильтр - это единый фильтр для всей страницы
# Он применяется для всех изменяемых элементов
# кроме общего числа студентов
data_filter_types = DataFilterTypes()
global_filter = data_filter_types.empty_filter

# Класс для построения графиков
dash_graph = DashGraph(kont_table, global_filter)

# Главная страница с дашбордом по контингенту студентов ДВФУ
main_layout = MainLayout(kont_table, dash_graph)
app.layout = main_layout.layout

# Добавить callback для дашборда по контингенту
get_callback(app, main_layout, dash_graph, global_filter, data_filter_types, kont_table)

#

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
    # app.run(debug=True)

