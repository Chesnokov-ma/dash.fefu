import plotly.express as px
from dashboard.dash_data_table import DataTable

"""


Примечания:
 * color_discrete_sequence в histogram списком, если не определен category_orders для color
 * color_discrete_sequence в histogram словарем, если определен category_orders для color
 * color_discrete_sequence в pie всегда словарем

"""


class DashGraph:
    def __init__(self, tableReference: DataTable, global_filter: dict):
        self.__tableRef = tableReference
        self.__global_filter = global_filter
        self.__current_df = None

    def make_school_hist(self):
        return px.histogram(
            self.__tableRef.get_filtered_data(self.__global_filter, ret_type='df', return_column=['Школа', 'LVL']),
            y='Школа', text_auto=True, color='LVL', histfunc='count',
            title='<b>Распределение студентов по школам</b>', category_orders={
                'LVL': ['Бакалавриат', 'Специалитет', 'Магистратура', 'Аспирантура', 'Ординатура', 'Докторантура']},
                color_discrete_map={
                    'Бакалавриат': '#6667ab', 'Специалитет': '#f18aad',
                    'Магистратура': '#ea6759', 'Аспирантура': '#f88f58',
                    'Ординатура': '#f3c65f', 'Докторантура': '#8bc28c'
            }).\
            update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'},
                           yaxis={'categoryorder': 'total ascending'}, xaxis_title_text='Количество студентов',
                           yaxis_title_text=None, title_x=0.5, font=dict(family="Roboto", size=14), title_font_size=16,
                           dragmode=False, legend={'orientation': 'h', 'traceorder': 'normal'}, legend_title=None). \
            update_layout(uniformtext_minsize=12, uniformtext_mode='hide'). \
            update_xaxes(visible=False). \
            update_traces(textposition='inside', showlegend=True). \
            update_traces(hovertemplate='><b>Школа:</b> %{y}<br>Студентов: %{x}<br>')

    def make_circle(self, column: str, title: str, labels: list, colors: dict = None):
            self.__current_df = self.__tableRef.get_filtered_data(self.__global_filter, ret_type='df', return_column=column)
            return px.pie(self.__current_df, values='Количество студентов', color=column,
                          names=column, title=title, labels=labels,
                          color_discrete_map=colors). \
                update_layout(title_x=0.5, font=dict(family="Roboto", size=14), title_font_size=16). \
                update_traces(textposition='outside', textinfo='percent+label', showlegend=False). \
                update_layout(uniformtext_minsize=12, uniformtext_mode='hide'). \
                update_traces(hovertemplate='%{label}<br>Студентов: %{value}<br>(%{percent})')

    def make_kurs_circle(self, column: str, title: str):
        self.__current_df = self.__tableRef.get_filtered_data(self.__global_filter, ret_type='df', return_column=column)
        return px.pie(self.__current_df, values='Количество студентов', color=column,
                      names=column, title=title, hole=.3,
                      color_discrete_map={'1 Курс': '#6667ab', '2 Курс': '#f18aad', '3 Курс': '#ea6759',
                                          '4 Курс': '#f88f58', '5 Курс': '#f3c65f', '6 Курс': '#8bc28c',
                                          '7 Курс': '#00132d'}). \
            update_layout(title_x=0.5, font=dict(family="Roboto", size=14), title_font_size=16). \
            update_traces(textposition='inside', textinfo='label', showlegend=False). \
            update_layout(uniformtext_minsize=10, uniformtext_mode='hide'). \
            update_traces(hovertemplate='%{label}<br>Студентов: %{value}<br>(%{percent})', marker={'line': {'color': '#000000',
                                                                                     'width': .1}})
