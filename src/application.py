
from Program.GUI.my_app_gemba import OperBalancerApplication
from Program.GUI.data_model_gemba import DataModel
from edifice import App
import click
from Program.Production.GfemScenarios import *


@click.command()
@click.option('--path')
#path = r'C:\Users\User\Documents\production_prototype\src\program\data'

def main(path: str):

    scenarios = RegressionScenarios(sorted_data=SortedGfemData(
                                            prepared_data=GfemDataFrame(
                                                    file_path=path)
                                                                )
                                    )

    data_model_gemba = DataModel(scenarios=scenarios, path=path, five_year_format=True, vbd=True)
    data_model_gemba.initializtion()
    app = OperBalancerApplication(model_proxy=data_model_gemba,
                                  result_path=path)
    App(app).start()
    """

   #Мониторинг

    gap = 0
    filtered = {'Company': 'All', 'Field': 'All'}
    monitoring_module = AroMonitoring(file_path=path, filter=filtered, gap=gap) #,date=date)
    app = MonitoringApp(data_model=DataModelMonitoring(monitoring_module=monitoring_module),
                        result_path=path)
    App(app).start()
    """
if __name__ == '__main__':
    main()
