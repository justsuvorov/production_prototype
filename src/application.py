from Program.Production.GfemScenarios import RegressionScenarios, SortedGfemData, GfemDataFrame
from Program.Production.AppGui import Application
from edifice import App
import click


#@click.command()
#@click.option('--path')
path=r'C:\Users\User\Documents\production_prototype\src\program\data'

def main(path: str):

    scenarios = RegressionScenarios(sorted_data=SortedGfemData(
                                                prepared_data=GfemDataFrame(
                                                        file_path=path)
                                                                )
                                    )
    app = Application(scenarios=scenarios, path=path)
    app.initialization()
    App(app).start()

if __name__ == '__main__':
    main(path)
