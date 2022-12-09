from ObjectBuilders.Parser import SetOfWellsParser
from pathlib import Path
from ObjectBuilders.FormatReader import SetOfWellsFormatReader
from ObjectBuilders.Builders import *


DATA_DIR = Path(r'C:\Users\User\Documents\production_prototype\Input\TestData')

filePath = DATA_DIR/'СВОД_скв._NEW_5лет.xlsx'

def main():
    domainModel = DomainModelBuilder(parser=SetOfWellsParser(data_path=filePath),
                                     format_reader=SetOfWellsFormatReader(),
                                     )
    domain_model = domainModel.build_object()
    return domain_model



if __name__ == '__main__':
    main()