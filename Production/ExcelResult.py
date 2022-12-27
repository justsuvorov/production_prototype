import pandas as pd
import numpy as np

class ExcelResult:
    def __init__(self,
                 domain_model,
                 result=None):
        self.domain_model = domain_model

    def dataframe(self):
        names, crude, fcf = self._data()
        crude = np.array(crude)
        fcf = np.array(fcf)
        data = [crude.T, fcf.T]
        df = pd.DataFrame(crude).to_excel('1.xlsx')
        df2 = pd.DataFrame(fcf).to_excel('2.xlsx')






    def _data(self):
       names = []

       l = len(self.domain_model[0])
       crude = []
       fcf = []
       for i in range(l):
            names.append(self.domain_model[0][i].name)
            for key in self.domain_model[0][i].indicators:
                if key == 'Добыча нефти, тыс. т':
                    crude.append(self.domain_model[0][i].indicators[key][0:366])

                if key == 'FCF':
                    fcf.append(  self.domain_model[0][i].indicators[key][0:366])

       return names, crude, fcf




       # df = pd.DataFrame


