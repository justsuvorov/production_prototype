
from Program.ProductionTests import ScenarioViewerTest, OperationalProductionBalancerTest, CompensatoryProductionMalancerTest
import click

#@click.command()
#@click.option('--path')
"""
#path=r'C:\Users\User\Documents\production_prototype\src\program\data'
def main(path):
#    BalancerTest.main(path)
#    OperationalProductionBalancerTest.main(path)
#    CompensatoryProductionMalancerTest.main(path)
    ScenarioViewerTest.main(path)
if __name__ == '__main__':
    main(path)
"""
from Program.Production.GfemScenarios import RegressionScenarios, SortedGfemData, GfemDataFrame
from Program.Production.AppGui import Application
from edifice import App
path=r'C:\Users\User\Documents\production_prototype\src\program\data'
def main(file_path: str):

    scenarios = RegressionScenarios(sorted_data=SortedGfemData(
                                                prepared_data=GfemDataFrame(
                                                    file_path=file_path)
                                                                )
                                    )
    app = Application(scenarios=scenarios)
    app.initialization()
    App(app).start()

if __name__ == '__main__':
    main(path)
