from Program.Production.GfemScenarios import AroMonitoring
from Program.ObjectBuilders.Parser import *
from Program.GUI.my_app import MyApplication, MonitoringApp
from Program.GUI.data_model import DataModel, DataModelFull, DataModelMonitoring
from edifice import App

path=r'C:\Users\User\Documents\production_prototype\src\program\data'


def main(file_path: str):
    filtered = {'Company': 'All', 'Field': 'All'}

    monitoring_module = AroMonitoring(file_path=file_path, filter=filtered, )
  #  monitoring_module.black_list(excel_export=True)
  #  monitoring_module.aro_full_info_black_list(excel_export=True)
  #  monitoring_module.export_company_form()

    app = MonitoringApp(data_model=DataModelMonitoring(monitoring_module=monitoring_module),
                        result_path=file_path)
    App(app).start()


if __name__ == '__main__':
    main(path)
