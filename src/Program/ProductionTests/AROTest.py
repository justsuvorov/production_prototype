from Program.Production.GfemScenarios import GfemDataFrameAro
from Program.ObjectBuilders.Parser import *


path=r'C:\Users\User\Documents\production_prototype\src\program\data'
def main(file_path: str):
    filtered = {'Company': 'All', 'Field': 'All'}

    data = GfemDataFrameAro(file_path=file_path, filter=filtered, db_export=True)
    data.black_list()





if __name__ == '__main__':
    main(path)
