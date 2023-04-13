from Program.DOTests.HierarchyFromRatingsTest import *
from Program.Production.GfemScenarios import RegressionScenarios, SortedGfemData, GfemDataFrame
from Program.Production.AppGui import Application
from Program.GUI.my_app import MyApplication
from Program.GUI.data_model import DataModel
from edifice import App
import click
from pathlib import Path


@click.command()
@click.option('--path')
#path=r'C:\Users\User\Documents\production_prototype\src\program\data'

def main(path: str):
    #domain_model_full = domain_model(file_path=Path(path))


    scenarios = RegressionScenarios(sorted_data=SortedGfemData(
                                                prepared_data=GfemDataFrame(
                                                        file_path=path)
                                                                )
                                    )
    data_model = DataModel(scenarios=scenarios, path=path)
    data_model.initializtion()
   # app = Application(scenarios=scenarios, path=path)
    app = MyApplication(data_model=data_model, result_path=path)
  #  app.initialization()
    App(app).start()

if __name__ == '__main__':
    main()
