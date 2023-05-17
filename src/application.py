from Program.DOTests.HierarchyFromRatingsTest import *
from Program.Production.GfemScenarios import RegressionScenarios, SortedGfemData, GfemDataFrame, PortuDataFrame
from Program.Production.AppGui import Application
from Program.GUI.my_app import MyApplication
from Program.GUI.data_model import DataModel, DataModelFull
from edifice import App
import click
from pathlib import Path

from Program.Production.GfemScenarios import AroMonitoring
from Program.ObjectBuilders.Parser import *
from Program.GUI.my_app import MonitoringApp
from Program.GUI.data_model import DataModel, DataModelFull, DataModelMonitoring


#@click.command()
#@click.option('--path')
path=r'C:\Users\User\Documents\production_prototype\src\program\data'

def main(path: str):
    """
    #domain_model_full = domain_model(file_path=Path(path))


 #   scenarios = RegressionScenarios(sorted_data=SortedGfemData(
                                                prepared_data=GfemDataFrame(
                                                        file_path=path)
                                                                )
                                    )
   # data_model = DataModel(scenarios=scenarios, path=path)
  #  data_model = DataModelFull(scenarios=scenarios, path=path, portu_results=PortuDataFrame(file_path=path))
  #  data_model.initializtion()
 #   data_model.full_initializtion()
   # app = Application(scenarios=scenarios, path=path)
 #   app = MyApplication(data_model=data_model, result_path=path)
  #  app.initialization()
    """

    filtered = {'Company': 'All', 'Field': 'All'}

    monitoring_module = AroMonitoring(file_path=path, filter=filtered, )
    #  monitoring_module.black_list(excel_export=True)
    #  monitoring_module.aro_full_info_black_list(excel_export=True)
    #  monitoring_module.export_company_form()

    app = MonitoringApp(data_model=DataModelMonitoring(monitoring_module=monitoring_module),
                        result_path=path)
    App(app).start()


if __name__ == '__main__':
    main(path)