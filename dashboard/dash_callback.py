from dash import Input, ctx, Output, dcc
from debug_str import debug_str

"""
Обработка нажатия на все интерактивные элементы на странице
При добавлении новых элементов: Output должен находиться перед Input
Так как любой фильтр влияет на всю страницу, более чем 1 функция callback не имеет смысла

Пояснение:
    Output -> (id элемента, возвращаемое свойство элемента)
    Input -> (id элемента, принимаемое свойство элемента)
    
Примечание:
# Разделение callback на кнопки и фильтры: https://stackoverflow.com/questions/62102453/how-to-define-callbacks-in-separate-files-plotly-dash
# clientside_callback: https://dash.plotly.com/clientside-callbacks
"""

# Последняя нажатая кнопка выбора уровня подготовки
# сохраняется в глобальном пространстве
last_btn_clicked = -1

# Активные кнопки выбора уровня подготовки
active_lvl_buttons = set()

# Были ли сброшены фильтры
remove_filters_pressed = False


def get_callback(app, main_layout, dash_graph, global_filter, data_filter_types, data_table):
    @app.callback(
        # Текст из панели с направлениями подготовки
        Output('lvl-text', 'children'),

        # Данные (цифры) из панели
        Output('val-table-0', 'children'),
        Output('val-table-1', 'children'),
        Output('val-table-2', 'children'),
        Output('val-table-3', 'children'),
        Output('val-table-4', 'children'),
        Output('val-table-5', 'children'),
        Output('val-table-6', 'children'),
        Output('val-table-7', 'children'),

        # Графики
        Output('school-graph', 'figure'),
        Output('bd-gph', 'figure'),
        Output('gn-gph', 'figure'),
        Output('ig-gph', 'figure'),
        Output('kr-gph', 'figure'),

        # Фильтры
        Output('filters-0', 'value'),
        Output('filters-1', 'value'),
        Output('filters-2', 'value'),
        Output('filters-3', 'value'),
        Output('filters-4', 'value'),
        Output('filters-5', 'value'),

        # Кнопки (подсветка активных)
        Output('btn-1', 'className'),
        Output('btn-2', 'className'),
        Output('btn-3', 'className'),
        Output('btn-4', 'className'),
        Output('btn-5', 'className'),
        Output('btn-6', 'className'),

        # Кнопки (n_clicks - количество нажатия на кнопки)
        Input('btn-0', 'n_clicks'),
        Input('btn-1', 'n_clicks'),
        Input('btn-2', 'n_clicks'),
        Input('btn-3', 'n_clicks'),
        Input('btn-4', 'n_clicks'),
        Input('btn-5', 'n_clicks'),
        Input('btn-6', 'n_clicks'),
        Input('btn-df', 'n_clicks'),

        # Фильтры (radio_button)
        Input('filters-0', 'value'),
        Input('filters-1', 'value'),
        Input('filters-2', 'value'),
        Input('filters-3', 'value'),
        Input('filters-4', 'value'),
        Input('filters-5', 'value'),

        prevent_initial_call=True
    )
    def callback_click(bn0, bn1, bn2, bn3, bn4, bn5, bn6, bndf,
                       v0, v1, v2, v3, v4, v5):
        """Обработка нажатий на кнопки или фильтры"""

        global last_btn_clicked
        global remove_filters_pressed

        remove_filters_pressed = False
        btn_default_class = 'btn-preset'

        # Обработка нажатия на кнопки (выбор направления подготовки)
        # ctx.triggered_id - контекст
        # ====================================================================================================================================
        all_lvls_pressed = False
        if 'btn' in ctx.triggered_id:
            ids = [f'btn-{i}' for i in range(7)]
            for i in range(len(ids)):
                if ids[i] == ctx.triggered_id:

                    # Нажатие на кнопку
                    if i == 0:
                        global_filter['LVL'] = {}
                        active_lvl_buttons.clear()
                        all_lvls_pressed = True
                    else:
                        if not all_lvls_pressed:
                            active_lvl_buttons.remove(i) if i in active_lvl_buttons else active_lvl_buttons.add(i)

                    last_btn_clicked = i

                    # Повторное нажатие на кнопку - отмена выбора
                    # else:
                    #     global_filter['LVL'] = []
                    #     last_btn_clicked = -1

            lvl_lst = []
            for i in range(len(ids)):
                if i > 0:
                    if i in active_lvl_buttons:
                        lvl_lst.append(data_filter_types.LVL_filters[i - 1])

            if len(lvl_lst) < 6:
                global_filter['LVL'] = lvl_lst
            else:
                global_filter['LVL'] = {}

            # Сбросить все фильтры
            if ctx.triggered_id == 'btn-df':
                # print('All filters were deleted')
                data_filter_types.set_empty_filter(global_filter)
                active_lvl_buttons.clear()
                remove_filters_pressed = True

        # Обработка активации фильтров
        # ====================================================================================================================================
        if 'filters' in ctx.triggered_id and not remove_filters_pressed:
            last_btn_clicked = -1

            # 1. Курс
            global_filter['Curs'] = [elem for elem in v0[1:]]

            # 2. Основа обучения
            if len(v1) == 3 or len(v1) == 1:
                global_filter['Money'] = []
            elif len(v1) == 2 and 'Бюджет' in v1:
                global_filter['Money'] = ['Бюджет']
            elif len(v1) == 2 and 'Договор' in v1:
                global_filter['Money'] = ['Договор']

            # 3. Форма обучения
            if len(v2) == 3 or len(v2) == 1:
                global_filter['Form'] = []
            elif len(v2) == 2 and 'Очная' in v2:
                global_filter['Form'] = ['Очная']
            elif len(v2) == 2 and 'Заочная' in v2:
                global_filter['Form'] = ['Заочная']

            # 4. Пол
            if len(v3) == 3 or len(v3) == 1:
                global_filter['Gen'] = []
            elif len(v3) == 2 and 'Мужчины' in v3:
                global_filter['Gen'] = ['Мужской']
            elif len(v3) == 2 and 'Женщины' in v3:
                global_filter['Gen'] = ['Женский']

            # 5. Инвалидность
            if len(v4) == 3 or len(v4) == 1:
                global_filter['Dis'] = []
            elif len(v4) == 2 and 'Да' in v4:
                global_filter['Dis'] = ['Да']
            elif len(v4) == 2 and 'Нет' in v4:
                global_filter['Dis'] = ['Нет']

            # 6. Гражданство
            if len(v5) == 3 or len(v5) == 1:
                global_filter['Cnt'] = []
            elif len(v5) == 2 and 'Иностранный гражданин' in v5:
                global_filter['Cnt'] = ['ИГ']
            elif len(v5) == 2 and 'Российская Федерация' in v5:
                global_filter['Cnt'] = ['РФ']

        #TODO: if debug is true
        # debug_str({'global filter': global_filter, 'Context': ctx.triggered_id,
        #            'del fiters': remove_filters_pressed, 'set': active_lvl_buttons})

        ret_0, ret_1, ret_2, ret_3, ret_4, ret_5, ret_6, ret_7 = [main_layout.make_val_table(global_filter, i) for i in
                                                                  range(8)]

        # Возврат значений
        # ====================================================================================================================================

        return ' + '.join(global_filter['LVL']) if len(global_filter['LVL']) else 'Все уровни подготовки', \
               ret_0, ret_1, ret_2, ret_3, ret_4, ret_5, ret_6, ret_7, \
               dash_graph.make_school_hist(), \
               dash_graph.make_circle('БД', '<b>Соотношение студентов на<br>бюджетной и договорной основе</b>',
                                      ['Бюджет', 'Договор'],
                                      {'Бюджет': '#6667ab', 'Договор': '#8bc28c'}), \
               dash_graph.make_circle('Пол', '<b>Соотношение студентов по полу</b>',
                                      ['Мужской', 'Женский'],
                                      {'Мужской': '#6667ab', 'Женский': '#8bc28c'}), \
               dash_graph.make_circle('IG', '<b>Соотношение студентов РФ<br>и иностранных граждан</b>',
                                      ['РФ', 'ИГ'],
                                      {'РФ': '#6667ab', 'ИГ': '#8bc28c'}), \
               dash_graph.make_kurs_circle('Курс', '<b>Распределение студентов <br>по курсам</b>'), \
               [None] if remove_filters_pressed else v0, \
               [None] if remove_filters_pressed else v1, \
               [None] if remove_filters_pressed else v2, \
               [None] if remove_filters_pressed else v3, \
               [None] if remove_filters_pressed else v4, \
               [None] if remove_filters_pressed else v5, \
               f'{btn_default_class} activated' if 1 in active_lvl_buttons else btn_default_class, \
               f'{btn_default_class} activated' if 2 in active_lvl_buttons else btn_default_class, \
               f'{btn_default_class} activated' if 3 in active_lvl_buttons else btn_default_class, \
               f'{btn_default_class} activated' if 4 in active_lvl_buttons else btn_default_class, \
               f'{btn_default_class} activated' if 5 in active_lvl_buttons else btn_default_class, \
               f'{btn_default_class} activated' if 6 in active_lvl_buttons else btn_default_class


    # @app.callback(
    #     Output('download-df', 'data'),
    #     Input('btn-export', 'n_clicks'),
    #     prevent_initial_call=True
    # )
    # def export_click(btn_exp):
    #     return dcc.send_data_frame(data_table.get_filtered_data(global_filter, {}, 'df').to_excel, 'export.xlsx', sheet_name="Sheet_name_1")
