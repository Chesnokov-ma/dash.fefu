class DashBoard:
    def __init__(self):
        from .dashboard_layout import MainLayout
        from .dash_data_table import DataFilterTypes, DataTable
        from .dash_graph import DashGraph
        from .dash_config import Config
        from .utils import json_to_dict
        from .dash_callback import get_callback
