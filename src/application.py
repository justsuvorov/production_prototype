import datetime

from Program.DOTests.HierarchyFromRatingsTest import *
from Program.Production.GfemScenarios import RegressionScenarios, SortedGfemData, GfemDataFrame, PortuDataFrame
from Program.Production.AppGui import Application
from Program.GUI.my_app_gemba import OperBalancerApplication
from Program.GUI.data_model_gemba import DataModel
from edifice import App
import click
from pathlib import Path
from Program.AROMonitoring.aro_monitoring import AroMonitoring
from Program.GUI.data_model_monitoring import DataModelMonitoring
from Program.Production.GfemScenarios import *
from Program.ObjectBuilders.Parser import *
from Program.GUI.my_app import MonitoringApp, BalancerViewerApplication
from Program.GUI.data_model_vbd import DataModelVbd
from Program.GUI.data_model_full import DataModelFull
from Program.GUI.data_model import ModelProxy

#@click.command()
#@click.option('--path')
path = r'C:\Users\User\Documents\production_prototype\src\program\data'

def main(path: str):

    #domain_model_full = domain_model(file_path=Path(path))
    scenarios = RegressionScenarios(sorted_data=SortedGfemData(
                                            prepared_data=GfemDataFrame(
                                                    file_path=path)
                                                                )
                                    )
    """
    data_model_full = DataModelFull(scenarios=scenarios, path=path, five_year_format=True)
    data_model_full.initialization()
    data_model_vbd = DataModelVbd(scenarios=scenarios, path=path, five_year_format=True)
    data_model_vbd.initialization()
    """
    data_model_gemba = DataModel(scenarios=scenarios, path=path, five_year_format=True, vbd=True)
    data_model_gemba.initializtion()
  #  vbd_data_model = DataModel(scenarios=vbd_scenarios, path=path, five_year_format=True, vbd=True)
  #  full_oper_balaner_model = FullOperModel(data_model=data_model, vbd_data_model=vbd_data_model)
   # full_oper_balaner_model.initialization()

 #   data_model.full_initializtion()
   # app = Application(scenarios=scenarios, path=path)
    #app = MyApplication(data_model=data_model, result_path=path)
 #   app = OperBalancerApplication(model_proxy=ModelProxy(modelA=data_model_full, modelB=data_model_vbd), result_path=path)
    app = OperBalancerApplication(model_proxy=data_model_gemba,
                                  result_path=path)
 #   app = BalancerViewerApplication(data_model=data_model, result_path=path)

 #   app.initialization()
    App(app).start()


    #Просмотрщик для балансировки


    """
    
    gap = 1
    filtered = {'Company': 'All', 'Field': 'All'}
    monitoring_module = AroMonitoring(file_path=path, filter=filtered, gap=gap) #,date=date)
    app = MonitoringApp(data_model=DataModelMonitoring(monitoring_module=monitoring_module),
                        result_path=path)

    App(app).start()
    """
if __name__ == '__main__':
    main(path)
