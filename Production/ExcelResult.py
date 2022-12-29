import pandas as pd
import numpy as np

class ExcelResult:
    def __init__(self,
                 domain_model,
                 date_start,
                 vbd_index,
                 result=None):
        self.domain_model = domain_model
        self.date_start = date_start
        self.vbd_index = vbd_index
        self.result = result

    def dataframe(self):
        crude_base, crude_vbd, fcf_base, fcf_vbd = self._data()
        crude_base = np.array(crude_base)
        fcf_base = np.array(fcf_base)
        crude_vbd = np.array(crude_vbd)
        fcf_vbd = np.array(fcf_vbd)
        vbd_names = self.names('VBD.xlsx')
       # base_names = self.names('СВОД_скв._NEW_5лет.xlsx')




        dateline = pd.date_range(start=self.date_start, periods=366)
        data = [crude_base, fcf_base, crude_vbd, fcf_vbd]
        df = []

        for table in data:
            df.append(pd.DataFrame(table, columns=dateline))
        if self.result is not None:
            df.append(pd.DataFrame(self.result[self.vbd_index:]))
        #df[0].index = base_names
        #df[1].index = base_names
        df[2].index = vbd_names
        df[3].index = vbd_names
        return df

    def save(self):
        df = self.dataframe()
        df[0].to_excel('Production_results_base.xlsx')
        df[0].transpose().sum(axis=1).to_excel('Production_results_sum.xlsx')

        df[1].to_excel('Economic_results_base.xlsx')
        df[2].to_excel('Production_results_vbd.xlsx')
        df[2].transpose().sum(axis=1).to_excel('VBD_sum_results.xlsx')
        df[3].transpose().to_excel('Economic_results_vbd.xlsx')
        if df[4] is not None:
            df[4].to_excel('Shifts.xlsx')



    def _data(self):
       names = []

       l = len(self.domain_model[0])
       crude_base = []
       crude_vbd = []
       fcf_base = []
       fcf_vbd = []
       for i in range(self.vbd_index):
            names.append(self.domain_model[0][i].name)
            for key in self.domain_model[0][i].indicators:
                if key == 'Добыча нефти, тыс. т':
                    crude_base.append(self.domain_model[0][i].indicators[key][0:366])

                if key == 'FCF':
                    fcf_base.append(  self.domain_model[0][i].indicators[key][0:366])
       for i in range(self.vbd_index+1, l):
            names.append(self.domain_model[0][i].name)
            for key in self.domain_model[0][i].indicators:
                if key == 'Добыча нефти, тыс. т':
                    crude_vbd.append(self.domain_model[0][i].indicators[key][0:366])

                if key == 'FCF':
                    fcf_vbd.append( self.domain_model[0][i].indicators[key][0:366])


       return crude_base, crude_vbd, fcf_base, fcf_vbd


    def names(self, filename: str):
        df = pd.read_excel(filename).loc[1:]
        names = pd.DataFrame()
        names['Месторождение'] = df['Месторождение']
        names['Название ДНС'] = df['Название ДНС']
        names['Скважина'] = df['Скважина']
        names['Куст'] = df['Куст']
        return names

       # df = pd.DataFrame


