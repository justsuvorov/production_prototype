
from Program.ProductionTests import OperationalProductionBalancerTest
import click

#@click.command()
#@click.option('--path')

path=r'C:\Users\User\Documents\production_prototype\src\program\data'
def main(path):
#    BalancerTest.main(path)
    OperationalProductionBalancerTest.main(path)
if __name__ == '__main__':
    main(path)