from dash import html, dcc
from dashboard.dash_data_table import DataTable
from dashboard.dash_graph import DashGraph


class MainLayout:
    def __init__(self, dataTableRef: DataTable, dashGraphRef: DashGraph):
        self.__tableRef = dataTableRef
        self.__dash_graph = dashGraphRef

        self.__layout = html.Div([
            html.Div(className='wrapper main',
                     children=[
                         html.Div(className='column-text', children=[               # колонка 1
                             html.Div(className='sum-value', children=[
                                 html.Div(className='date-label small', children='Обновление данных: 20.11.2023'),
                                 html.Div(className='max-stud max-stud-value bold main__heading', children=str(self.__tableRef.all_z_books)),
                                 html.Div(className='max-stud-text italic small gray page-text',
                                          children='Всего обучающихся')
                             ]),
                             html.Div(className='filtered-value page-text', children=[
                                 html.Div(className='lvl-text', id='lvl-text', children='Все уровни подготовки'),
                                 html.Div(className='filtered-tables', children=[
                                     html.Div(className='add-flex-col name-table', children=self.__make_name_table()),
                                     html.Div(className='add-flex-col val-table', children=self.__make_val_table(10)),
                                     html.Div(className='add-flex-col stud-table', children=self.__make_stud_table(10)),
                                 ]),
                             ]),
                         ]),
                         html.Div(className='column-graph page-text', children=[              # колонка 2
                             html.Div(className='button-panel', children=self.__make_lvl_buttons()
                                      ),
                             html.Div(className='school-panel', children=dcc.Graph(figure=self.__dash_graph.make_school_hist(),
                                                                                   className='school-graph', id='school-graph',
                                                                                   config={'displayModeBar': False})),
                             html.Div(className='graph-panel', children=[
                                 dcc.Graph(figure=self.__dash_graph.make_kurs_circle('Курс', '<b>Распределение студентов <br>по курсам</b>'),
                                           className='circle-graph-main', id='kr-gph', config={'displayModeBar': False}),

                                 dcc.Graph(figure=self.__dash_graph.make_circle('БД', '<b>Соотношение студентов на<br>бюджетной и договорной основе</b>',
                                                                                ['Бюджет', 'Договор'],
                                                                                {'Бюджет': '#6667ab', 'Договор': '#8bc28c'}), #royalblue darkblue
                                           className='circle-graph', id='bd-gph', config={'displayModeBar': False}),

                                 dcc.Graph(figure=self.__dash_graph.make_circle('Пол', '<b>Соотношение студентов по полу</b>',
                                                                                ['Мужской', 'Женский'],
                                                                                {'Мужской': '#6667ab', 'Женский': '#8bc28c'}),
                                           className='circle-graph', id='gn-gph', config={'displayModeBar': False}),

                                 dcc.Graph(figure=self.__dash_graph.make_circle('IG', '<b>Соотношение студентов РФ<br>и иностранных граждан</b>',
                                                                                ['РФ', 'ИГ'],
                                                                                {'РФ': '#6667ab', 'ИГ': '#8bc28c'}),
                                           className='circle-graph', id='ig-gph', config={'displayModeBar': False}),
                             ]),
                         ]),
                         html.Div(className='column-filter page-text', children=[             # колонка 3
                             html.Div(className='filters', children=self.__make_filters()),
                             html.Button('Очистить все фильтры', className='btn-df btn-preset-1', id='btn-df', n_clicks=0),
                             html.Button('Экспорт в excel', className='btn-exp btn-preset', id='btn-export', n_clicks=0),
                             dcc.Download(id='download-df')
                         ]),
                     ]),
        ])

    #TODO: считывание из json
    def __make_name_table(self):
        names = ['Всего', 'Бюджет', 'Договор', 'Очная форма', 'Заочная форма', 'Женщины', 'Мужчины', 'Иностранцы', 'Целевая квота', 'Спец. квота']

        arr = [html.Div(className=f'filtered-panel bold oblique', children=f'{names[i]}') for i in range(len(names))]
            # .append(html.Div(className=f'filtered-panel bold oblique', children='Спец. квота', title='Военные действия, техногенные катастрофы'))

        return arr

    #TODO: запросы к БД
    def __make_val_table(self, num):
        return [html.Div(className='filtered-panel', id=f'val-table-{i}',
                         children=html.Div(children=str(self.make_val_table({}, i)))) for i in range(num)]

    def __make_stud_table(self, num):
        return [html.Div(className='filtered-panel oblique', children=f'чел.') for _ in range(num)]

    #TODO: из json
    def __make_lvl_buttons(self):
        names = ['Всего', 'Бакалавриат', 'Специалитет', 'Магистратура', 'Аспирантура', 'Ординатура', 'Докторантура']
        return [html.Button(f'{names[i]}', className='lvl-btn btn-preset', id=f'btn-{i}', n_clicks=0) for i in range(len(names))]

    #TODO: из json
    def __make_filters(self):
        names = {'Курс': ['1 Курс', '2 Курс', '3 Курс', '4 Курс', '5 Курс', '6 Курс', '7 Курс'],
                 'Основа обучения': ['Бюджет', 'Договор'],
                 'Форма обучения': ['Очная', 'Заочная'],
                 'Пол': ['Женщины', 'Мужчины'],
                 'Инвалидность': ['Да', 'Нет'],
                 'Гражданство': ['Российская Федерация', 'Иностранные граждане']}

        ret_list = []
        ind = 0
        for key in names:
            ret_list.append(html.Div(className='f-txt bold', children=key))
            ret_list.append(dcc.Checklist(options=names[key], value=[None], inline=False, id=f'filters-{ind}', className='radio-filters'))
            ind += 1

        return ret_list

    def make_val_table(self, global_filter, ind: int):
        """Левая часть дашборда"""
        if ind == 0:
            return self.__tableRef.get_filtered_data(global_filter)
        elif ind == 1:
            return self.__tableRef.get_filtered_data(global_filter, {"Money": "Бюджет"})
        elif ind == 2:
            return self.__tableRef.get_filtered_data(global_filter, {"Money": "Договор"})
        elif ind == 3:
            return self.__tableRef.get_filtered_data(global_filter, {"Form": "Очная"})
        elif ind == 4:
            return self.__tableRef.get_filtered_data(global_filter, {"Form": "Заочная"})
        elif ind == 5:
            return self.__tableRef.get_filtered_data(global_filter, {"Gen": "Женский"})
        elif ind == 6:
            return self.__tableRef.get_filtered_data(global_filter, {"Gen": "Мужской"})
        elif ind == 7:
            return self.__tableRef.get_filtered_data(global_filter, {"Cnt": "ИГ"})
        elif ind == 8:
            return self.__tableRef.get_filtered_data(global_filter, {"Cell_pr": "Целевой прием"})
        elif ind == 9:
            return self.__tableRef.get_filtered_data(global_filter, {"Spec_kv": "Да"})

    @property
    def layout(self):
        return self.__layout
