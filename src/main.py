
from Program.ProductionTests import ScenarioViewerTest, OperationalProductionBalancerTest, CompensatoryProductionMalancerTest
import click

#@click.command()
#@click.option('--path')

path=r'C:\Users\User\Documents\production_prototype\src\program\data'
def main(path):
#    BalancerTest.main(path)
#    OperationalProductionBalancerTest.main(path)
#    CompensatoryProductionMalancerTest.main(path)
    ScenarioViewerTest.main(path)
if __name__ == '__main__':
    main(path)
