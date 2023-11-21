import pandas as pd


class DataFilterTypes:
    filter_keys = ('LVL', 'Money', 'Form', 'Gen', 'Dis', 'Cnt', 'Curs')
    empty_filter = {'LVL': []}
    # фильтры
    LVL_filters = ['Бакалавриат', 'Специалитет', 'Магистратура', 'Аспирантура', 'Ординатура', 'Докторантура']
    # столбцы таблицы
    col_names = {'LVL': 'LVL', 'Money': 'БД', 'Form': 'Форма обучения',
                 'Gen': 'Пол', 'Dis': 'inv', 'Cnt': 'IG', 'Cell_pr': 'Вид возмещения затрат', 'Spec_kv': 'Спец квота',
                 'Curs': 'Курс'}

    def get_empty_filter(self):
        for key in self.filter_keys:
            self.empty_filter[key] = []

    def set_empty_filter(self, filter: dict):
        for key in self.filter_keys:
            if key in filter:
                filter[key] = []


class DataTable:
    def __init__(self, src: str):
        self.__df = pd.read_excel(src)
        self.__df.drop_duplicates(subset='Зачетная книга', keep='first')
        self.__make_short_school_name()
        self.__all_zbooks = self.__df['Зачетная книга'].count()
        #TODO: спец квота

    def get_filtered_data(self, base_filter: dict, additional_filter: dict = {}, ret_type: str = 'val',
                          return_column: str | list | None = None, add_column: str = None):
        """
        Применить фильтры base_filter и additional_filter к таблице и вернуть значение.

        При ret_type со значением 'val' возвращает число.
        При ret_type со значением 'df' возвращает полную таблицу (DataFrame).
        При ret_type со значением 'df' и return_column со значением !None возвращает короткую таблицу (DataFrame).

        :param base_filter: первый фильтр.
        :param additional_filter: второй (необязательный) фильтр.
        :param ret_type: тип возвращаемого значения val | df.
        :param return_column: при непустом значении и tret_type со значением !None возвращает короткую таблицу (DataFrame).
        :return:

        """
        res_df = self.__df
        for current_filter in [base_filter, additional_filter]:     # Используя глобальный и дополнительный фильтры
            for key, value in current_filter.items():
                if value:
                    if type(value) == str:
                        res_df = res_df[res_df[DataFilterTypes.col_names[key]] == value]
                    elif type(value) == list:
                        res_df = res_df[res_df[DataFilterTypes.col_names[key]].isin(value)]

        if ret_type == 'val':
            return res_df['Зачетная книга'].count()
        else:
            if not return_column:
                return res_df
            else:
                if type(return_column) == str:
                    return pd.DataFrame({return_column: res_df[return_column], 'Количество студентов': res_df['Количество студентов']})
                else:
                    ret_dct = {col: res_df[col] for col in return_column}
                    ret_dct['Количество студентов'] = res_df['Количество студентов']
                    return pd.DataFrame(ret_dct)

    def __make_short_school_name(self):
        # удалить строки с гимназиями
        self.__df = self.__df[self.__df['Школа'].str.contains('Гимназия|колледж|Арсеньев|Камень') == False]     #TODO: из json
        self.__df = self.__df[self.__df['LVL'].str.contains('звена') == False]     #TODO: из json

        # переименовать школы в короткие формы по условию remap_dict
        #TODO: подгружать из внешнего json
        school_remap_dict = {'Восточный институт - Школа региональных и международных исследований': 'ВИ-ШРМИ',
                      'Инженерная школа': 'ПИ',
                      'Институт математики и компьютерных технологий (Школа)': 'ИМКТ',
                      'Институт Мирового океана (Школа)': 'ИМО',
                      'Институт наук о жизни и биомедицины (Школа)': 'ШМНЖ',
                      'Институт наукоемких технологий и передовых материалов (Школа)': 'ИНТПМ',
                      'Передовая инженерная школа «Институт биотехнологий, биоинженерии и пищевых систем»': 'ПИШ',
                      'Политехнический институт (Школа)': 'ПИ',
                      'Школа биомедицины': 'ШМНЖ',
                      'Школа естественных наук': 'ИНТПМ',
                      'Школа искусств и гуманитарных наук': 'ШИГН',
                      'Школа медицины': 'ШМНЖ',
                      'Школа медицины и наук о жизни': 'ШМНЖ',
                      'Школа педагогики': 'ШП',
                      'Школа экономики и менеджмента': 'ШЭМ',
                      'Юридическая школа': 'ЮШ'}

        BD_remap_dict = {
            'Б': 'Бюджет',
            'Д': 'Договор'
        }

        kurs_remap_dict = {
            'Первый': '1 Курс',
            'Второй': '2 Курс',
            'Третий': '3 Курс',
            'Четвертый': '4 Курс',
            'Пятый': '5 Курс',
            'Шестой': '6 Курс',
            'Седьмой': '7 Курс'
        }

        # переименовать
        self.__df = self.__df.replace({'Школа': school_remap_dict, 'БД': BD_remap_dict, 'Курс': kurs_remap_dict})

        # для подсчета
        self.__df['Количество студентов'] = [1 for _ in range(len(self.__df['Школа'].tolist()))]

        #спец квота
        kvot = self.__df['Льгота / Особая отметка'].tolist()

        spec_kv = []
        for kv in kvot:     #TODO: доработать точно

            if 'СВО' in str(kv):
                spec_kv.append('Да')
            elif 'военн' in str(kv):
                spec_kv.append('Да')
            elif 'катастр' in str(kv):
                spec_kv.append('Да')
            else:
                spec_kv.append('Нет')
        self.__df['Спец квота'] = spec_kv

    @property
    def all_z_books(self):
        return self.__all_zbooks
