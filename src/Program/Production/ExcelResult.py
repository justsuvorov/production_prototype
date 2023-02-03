import pandas as pd
import numpy as np
from Program.constants import DATA_DIR
from pathlib import Path
from Program.Production import Production
from Program.Production.InputParameters import TimeParameters


class ExcelResult:
    def __init__(self,
                 domain_model,
                 production: Production,
                 dates: TimeParameters,
                 results: str = 'Only sum'

                ):
        self.domain_model = domain_model
        self.production = production
        self.results = results
        self.dates = dates

        self.date_start = None
        self.vbd_index = None


    def dataframe(self):
        crude_base, crude_vbd, fcf_base, fcf_vbd = self._data()
        crude_base = np.array(crude_base)
        fcf_base = np.array(fcf_base)
        crude_vbd = np.array(crude_vbd)
        fcf_vbd = np.array(fcf_vbd)
        vbd_names = self.names('VBD.xlsx')
       # base_names = self.names('СВОД_скв._NEW_5лет.xlsx')
        dateline = pd.date_range(start=self.dates.date_start, periods=366)
        data = [crude_base, fcf_base, crude_vbd, fcf_vbd]
        df = []
        for table in data:
            df.append(pd.DataFrame(table, columns=dateline))
        if self.production.result_dates is not None:
            res = np.array(self.production.result_dates[self.vbd_index:])
            res = res - self.production.shift
            np.where(res != 357, res, 366)
            np.where(res>0, res, 0)
            for x in res:
                if x < 0: x = 0
            df.append(pd.DataFrame(res))
        #df[0].index = base_names
        #df[1].index = base_names
        df[2].index = vbd_names
        df[3].index = vbd_names
        return df

    def save(self, path = None):
        if path is not None:
            path = path
        else:
            path = DATA_DIR
        df = self.dataframe()
        if self.results == 'Only sum':
            df[0].sum(axis=0).to_excel(DATA_DIR / 'Production_results_sum.xlsx')
            df[2].transpose().sum(axis=1).to_excel(path / 'VBD_sum_results.xlsx')
        if self.results == 'Full':
            df[0].to_excel(DATA_DIR/'Production_results_base.xlsx')
            df[0].sum(axis=0).to_excel(DATA_DIR/'Production_results_sum.xlsx')
            df[1].to_excel(DATA_DIR/'Economic_results_base.xlsx')
            df[2].to_excel(DATA_DIR/'Production_results_vbd.xlsx')
            df[2].transpose().sum(axis=1).to_excel(path/'VBD_sum_results.xlsx')
            df[3].transpose().to_excel(DATA_DIR/'Economic_results_vbd.xlsx')
        if df[4] is not None:
            df[4].to_excel(path/'Shifts.xlsx')



    def _data(self):
       names = []
       self.vbd_index = self.production.vbd_index
       self.date_start = self.production.date_start
       l = len(self.domain_model)
       crude_base = []
       crude_vbd = []
       fcf_base = []
       fcf_vbd = []
       for i in range(self.vbd_index):
            names.append(self.domain_model[i].name)
            for key in self.domain_model[i].indicators:

                if key == 'Добыча нефти, тыс. т':
                    crude_base.append(self.domain_model[i].indicators[key][0:366])

                if key == 'FCF':
                    fcf_base.append(  self.domain_model[i].indicators[key][0:366])
       for i in range(self.vbd_index+1, l):
            names.append(self.domain_model[i].name)
            for key in self.domain_model[i].indicators:
                if key == 'Добыча нефти, тыс. т':
                    crude_vbd.append(self.domain_model[i].indicators[key][0:366])

                if key == 'FCF':
                    fcf_vbd.append(self.domain_model[i].indicators[key][0:366])

       return crude_base, crude_vbd, fcf_base, fcf_vbd


    def names(self, filename: str):
        df = pd.read_excel(DATA_DIR/filename).loc[1:]
        names = pd.DataFrame()
        names['Месторождение'] = df['Месторождение']
        names['Название ДНС'] = df['Название ДНС']
        names['Скважина'] = df['Скважина']
        names['Куст'] = df['Куст']
        return names

       # df = pd.DataFrame

class ExcelResultPotential:
    def __init__(self,
                 domain_model,
                 production: Production,
                 dates: TimeParameters,
                 results: str = 'Only sum'
                 ):

        self.domain_model = domain_model
        self.production = production
        self.results = results
        self.dates = dates

        self.date_start = None
        self.vbd_index = None


    def dataframe(self):
        crude_base, crude_vbd, fcf_base, fcf_vbd = self._data()
      #  crude_base = np.array(crude_base)
   #     fcf_base = np.array(fcf_base)
        crude_vbd = np.array(crude_vbd)
        fcf_vbd = np.array(fcf_vbd)
        vbd_names = self.names('VBD.xlsx')
       # base_names = self.names('СВОД_скв._NEW_5лет.xlsx')
        dateline = pd.date_range(start=self.dates.date_start, periods=366)
        data = [crude_base, fcf_base, crude_vbd, fcf_vbd]
        df = []
        for table in data:
            df.append(pd.DataFrame(table, columns=dateline))
        if self.production.result_dates is not None:
            res = np.array(self.production.result_dates[self.vbd_index:])
            res = res - self.production.shift
            np.where(res != 357, res, 366)
            np.where(res>0, res, 0)
            for x in res:
                if x < 0: x = 0
            df.append(pd.DataFrame(res))
        #df[0].index = base_names
        #df[1].index = base_names
        df[2].index = vbd_names
        df[3].index = vbd_names
        return df

    def save(self, path=None):
        if path is not None:
            path = path
        else:
            path = DATA_DIR
        df = self.dataframe()
        if self.results == 'Only sum':
            df[0].sum(axis=0).to_excel(path / 'Production_results_sum.xlsx')
            df[2].transpose().sum(axis=1).to_excel(path / 'VBD_sum_results.xlsx')
            df[1].transpose().sum(axis=1).to_excel(path/ 'Economic_results_base_sum.xlsx')
            df[3].transpose().sum(axis=1).to_excel(path / 'Economic_results_vbd.xlsx')
        if self.results == 'Full':
            df[0].to_excel(path/'Production_results_base.xlsx')
            df[0].sum(axis=0).to_excel(path/'Production_results_sum.xlsx')
            df[1].to_excel(path/'Economic_results_base.xlsx')
            df[2].to_excel(path/'Production_results_vbd.xlsx')
            df[2].transpose().sum(axis=1).to_excel(path/'VBD_sum_results.xlsx')
            df[3].transpose().to_excel(path/'Economic_results_vbd.xlsx')
        if df[4] is not None:
            df[4].to_excel(path/'Shifts.xlsx')



    def _data(self):
       names = []
       self.vbd_index = self.production.vbd_index

       self.date_start = self.production.date_start
       l = len(self.domain_model)
       crude_base = []
       crude_vbd = []
       fcf_base = []
       fcf_vbd = []
       for i in range(self.vbd_index):
            names.append(self.domain_model[i].name)
            for key in self.domain_model[i].indicators:

                if key == 'Добыча нефти, тыс. т':
                    crude_base.append(self.domain_model[i].indicators[key][0:366])

                if key == 'FCF':
                    fcf_base.append(  self.domain_model[i].indicators[key][0:366])
       for i in range(self.vbd_index+1, l):
            names.append(self.domain_model[i].name)
            for key in self.domain_model[i].indicators:
                if key == 'Добыча нефти, тыс. т':
                    crude_vbd.append(self.domain_model[i].indicators[key][0:366])

                if key == 'FCF':
                    fcf_vbd.append(self.domain_model[i].indicators[key][0:366])

       return crude_base, crude_vbd, fcf_base, fcf_vbd


    def names(self, filename: str):
        df = pd.read_excel(DATA_DIR/filename).loc[1:]
        names = pd.DataFrame()
        names['Месторождение'] = df['Месторождение']
        names['Название ДНС'] = df['Название ДНС']
        names['Скважина'] = df['Скважина']
        names['Куст'] = df['Куст']
        return names
