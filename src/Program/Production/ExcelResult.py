import abc

import pandas as pd
import numpy as np
from Program.constants import DATA_DIR
from pathlib import Path
from Program.Production import Production
from Program.Production.InputParameters import TimeParameters
from Program.Production.GuiInputInterface import *
from shutil import copy
from abc import ABC
from math import floor
from pathlib import Path


class CompanyDict:
    def __init__(self,
                 path
                 ):
        self.path = Path(path)
        self.joint_venture_crude_part = {}
        self.joint_venture_fcf_part = {}

    def load(self, scenario_program: bool = False):
        if not scenario_program:
            DATA = self.path / 'Балансировка компенсационных мероприятий для НРФ.xlsm'
        else:
            DATA = self.path / 'Словарь ДО.xlsx'
        df = pd.read_excel(DATA, sheet_name='Словарь ДО')


        df1 = df['Список ДО']
        df2 = df['Месторождение']
        if scenario_program:
            dataframe = pd.read_excel(DATA, sheet_name='Доли СП')
            df3 = dataframe['ДО']
            df4 = dataframe['По добыче']
            df5 = dataframe['По FCF']

            self.joint_venture_crude_part = dict(zip(list(df3), list(df4)))
            self.joint_venture_fcf_part = dict(zip(list(df3), list(df5)))
        company_dict = dict(zip(list(df2), list(df1)))
        return company_dict


class ResultExport(ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def save(self):
        pass


class ExcelResult(ResultExport):
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
            np.where(res > 0, res, 0)
            for x in res:
                if x < 0: x = 0
            df.append(pd.DataFrame(res))
        # df[0].index = base_names
        # df[1].index = base_names
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
            df[1].transpose().sum(axis=1).to_excel(path / 'Economic_results_base_sum.xlsx')
            df[3].transpose().sum(axis=1).to_excel(path / 'Economic_results_vbd.xlsx')
        if self.results == 'Full':
            df[0].to_excel(path / 'Production_results_base.xlsx')
            df[0].sum(axis=0).to_excel(path / 'Production_results_sum.xlsx')
            df[1].to_excel(path / 'Economic_results_base.xlsx')
            df[2].to_excel(path / 'Production_results_vbd.xlsx')
            df[2].transpose().sum(axis=1).to_excel(path / 'VBD_sum_results.xlsx')
            df[3].transpose().to_excel(path / 'Economic_results_vbd.xlsx')
        if df[4] is not None:
            df[4].to_excel(path / 'Shifts.xlsx')

    def _data(self):
        names = []
        self.vbd_index = self.production.vbd_index
        self.date_start = self.production.date_start
        l = len(self.domain_model)
        crude_base = []
        crude_vbd = []
        fcf_base = []
        fcf_vbd = []
        liquid_base = []
        liquid_vbd = []
        for i in range(self.vbd_index):
            names.append(self.domain_model[i].name)
            for key in self.domain_model[i].indicators:
                if key == 'Добыча нефти, тыс. т':
                    crude_base.append(self.domain_model[i].indicators[key][0:366])

                if key == 'Добыча жидкости, тыс. т':
                    liquid_base.append(self.domain_model[i].indicators[key][0:366])
                if key == 'FCF':
                    fcf_base.append(self.domain_model[i].indicators[key][0:366])
        for i in range(self.vbd_index, l):
            names.append(self.domain_model[i].name)
            for key in self.domain_model[i].indicators:
                if key == 'Добыча нефти, тыс. т':
                    crude_vbd.append(self.domain_model[i].indicators[key][0:366])
                if key == 'Добыча жидкости, тыс. т':
                    liquid_vbd.append(self.domain_model[i].indicators[key][0:366])
                if key == 'FCF':
                    fcf_vbd.append(self.domain_model[i].indicators[key][0:366])

        return crude_base, crude_vbd, fcf_base, fcf_vbd, liquid_base, liquid_vbd

    def names(self, filename: str):
        df = pd.read_excel(DATA_DIR / filename).loc[1:]
        names = pd.DataFrame()
        names['Месторождение'] = df['Месторождение']
        names['Название ДНС'] = df['Название ДНС']
        names['Скважина'] = df['Скважина']
        names['Куст'] = df['Куст']
        return names

    # df = pd.DataFrame


class ExcelResultPotential(ExcelResult):
    def __init__(self,
                 domain_model,
                 production: Production,
                 dates: TimeParameters,
                 results: str = 'Only sum',

                 ):

        super().__init__(
            domain_model=domain_model,
            production=production,
            dates=dates,
            results=results
        )

    def dataframe(self):
        crude_base, crude_vbd, fcf_base, fcf_vbd, liquid_base, liquid_vbd = self._data()
        crude_vbd = np.array(crude_vbd)
        fcf_vbd = np.array(fcf_vbd)
        dateline = pd.date_range(start=self.dates.date_start, periods=366)
        data = [crude_base, crude_vbd, fcf_base, fcf_vbd, liquid_base, liquid_vbd]
        df = []

        for table in data:
            try:
                df.append(pd.DataFrame(table, columns=dateline))
            except ValueError:
                df.append(pd.DataFrame(np.zeros_like(crude_base), columns=dateline))

                print('Отсутствуют скважины ВБД')
        if self.production.result_dates is not None:
            res = np.array(self.production.result_dates[self.vbd_index:])
            res = res - self.production.shift
            np.where(res != 357, res, 366)
            np.where(res > 0, res, 0)
            for x in res:
                if x < 0: x = 0
            df.append(pd.DataFrame(res))
        # df[2].index = vbd_names
        # df[3].index = vbd_names
        return df

    def save(self, path=None):
        if path is not None:
            path = path
        else:
            path = DATA_DIR
        """
        if not os.path.isfile(path / 'Балансировка компенсационных мероприятий для НРФ.xlsm'):
            home_path = os.path.split(path)[0]
            try:
                copy(str(home_path) + '//' + 'Балансировка компенсационных мероприятий для НРФ.xlsm',
                     str(path) + '//' + 'Балансировка компенсационных мероприятий для НРФ.xlsm')
            except FileNotFoundError:
                home_path = os.path.split(home_path)[0]
                copy(str(home_path) + '//' + 'Балансировка компенсационных мероприятий для НРФ.xlsm',
                     str(path) + '//' + 'Балансировка компенсационных мероприятий для НРФ.xlsm')
        """
        print('Exporting results...')
        df = self.dataframe()
        with pd.ExcelWriter(path / 'Results.xlsx') as writer:

            df[0].sum(axis=0).to_excel(writer, sheet_name='Production_results_sum')
            df[1].transpose().sum(axis=1).to_excel(writer, sheet_name='VBD_sum_results')
            df[2].transpose().sum(axis=1).to_excel(writer, sheet_name='Economic_results_base_sum')
            df[3].transpose().sum(axis=1).to_excel(writer, sheet_name='Economic_results_vbd')
            df[4].transpose().sum(axis=1).to_excel(writer, sheet_name='Liquid_results_base')
            df[5].transpose().sum(axis=1).to_excel(writer, sheet_name='Liquid_results_vbd')
            if self.results == 'Full':
                df[0].to_excel(writer, sheet_name='Production_results_base')
                df[2].to_excel(writer, sheet_name='Economic_results_base')
                df[1].to_excel(writer, sheet_name='Production_results_vbd')
                df[3].transpose().to_excel(writer, sheet_name='Economic_results_vbd')
            if df[6] is not None:
                df[6].to_excel(writer, sheet_name='Shifts')
        print('Program completed')

    @staticmethod
    def save_initial_results(domain_model, path, vbd_index: int):
        crude_base = []
        fcf_base = []
        liquid_base = []
        wells = domain_model['Wells']
        if vbd_index == 0 and len(wells) > 1:
            vbd_index = 1
        for i in range(vbd_index):
            for key in wells[i].indicators:
                if key == 'Добыча нефти, тыс. т':
                    crude_base.append(wells[i].indicators[key][0:366])
                if key == 'FCF':
                    fcf_base.append(wells[i].indicators[key][0:366])
                if key == 'Добыча жидкости, тыс. т':
                    liquid_base.append(wells[i].indicators[key][0:366])
        df = []
        data = [crude_base, fcf_base, liquid_base]
        for table in data:
            df.append(pd.DataFrame(table))
        with pd.ExcelWriter(path / 'initial_results.xlsx') as writer:
            df[0].sum(axis=0).to_excel(writer, sheet_name='Production_results_sum')
            df[1].transpose().sum(axis=1).to_excel(writer, sheet_name='Economic_results_base_sum')
            df[2].sum(axis=0).to_excel(writer, sheet_name='Liquid_results_sum')


class QlikExcelResult(ResultExport):

    def __init__(self,
                 dates: TimeParameters,
                 initial_domain_model: dict = None,
                 domain_model_with_results: dict = None,
                 production: Production = None,
                 export: bool = True,
                 ):
        self.initial_domain_model = initial_domain_model
        self.domain_model_with_results = domain_model_with_results
        self.production = production
        self.dates = dates
        self.data = []
        self.initial_data = []
        self.nrf = []
        self.crude_key = 'Добыча нефти, тыс. т'
        self.fcf_key = 'FCF'
        self.liquid_key = 'Добыча жидкости, тыс. т'
        self.wells = []
        self.export = export

        self.dateline = pd.date_range(start=self.dates.date_start, periods=365)
        self.dateline_export = pd.date_range(start=self.dates.date_start, periods=12, freq='M')

    def load_vbd_wells(self, wells: list, vbd_index: int, dates: list):
        try:
            for i in range(vbd_index, len(wells)):
                if dates[i] < 365:
                    well = wells[i]
                    gap_index = floor(dates[i] / 30.3)
                    self.load_nrf_well(well=well, gap_index=gap_index, type='ВБД')
        except:
            pass

    def load_nrf_well(self, well, gap_index: int, type: str = 'НРФ'):
        well_info = {}
        well_info['Месторождение'] = well.link['Fields'][0].name[0]
        well_info['Имя скважины'] = well.name[0]
        well_info['ДНС'] = well.link['Clusters'][0].name[0]
        well_info['ГЭП'] = gap_index
        well_info['Тип'] = type
        # well_info['ДО'] =
        self.wells.append(well_info)

    def load_data_from_domain_model(self, domain_model: dict, cut_index: int = None, initial_calc: bool = False,
                                    nrf: bool = False):

        domain_model_temp = domain_model.copy()

        if (cut_index is not None) and (initial_calc or nrf):
            wells = domain_model_temp['Wells'][0:cut_index]

        else:
            wells = domain_model_temp['Wells']

        for field in domain_model_temp['Fields']:
            well_sum = {}
            for well in field.link['Wells']:
                if well in wells:
                    df_crude = pd.Series(data=well.indicators[self.crude_key][0:365], index=self.dateline)
                    df_crude_result = df_crude.groupby([lambda x: x.year, lambda x: x.month]).sum()

                    df_fcf = pd.Series(well.indicators[self.fcf_key][0:365], index=self.dateline)
                    df_fcf_result = df_fcf.groupby([lambda x: x.year, lambda x: x.month]).sum()

                    df_liquid = pd.Series(well.indicators[self.liquid_key][0:365], index=self.dateline)
                    df_liquid_result = df_liquid.groupby([lambda x: x.year, lambda x: x.month]).sum()

                    well_sum[well.name[0]] = np.array([df_crude_result, df_fcf_result, df_liquid_result])

            b = np.array(list(well_sum.values()))
            if initial_calc:
                self.initial_data.append({field.name[0]: np.sum(b, axis=0)})
            elif nrf:
                self.nrf.append({field.name[0]: np.sum(b, axis=0)})
            else:
                self.data.append({field.name[0]: np.sum(b, axis=0)})

    # return self.data

    def save(self, path):
        if self.export:
            company_dict = CompanyDict(path=path).load()
            data = self.result(company_dict=company_dict)
            df = pd.DataFrame(self.wells)
            with pd.ExcelWriter(path / 'qlik_results.xlsx') as writer:
                data.to_excel(writer, sheet_name='Сводная таблица', index=False)
                df.to_excel(writer, sheet_name='Таблица скважин', index=False)

    def result(self, company_dict=None):

        list_of_dict = []
        for j in range(len(self.data)):
            indicators = np.array(list(self.data[j].values()))[0]
            indicators_init = np.array(list(self.initial_data[j].values()))[0]
            indicators_nrf = np.array(list(self.nrf[j].values()))[0]

            for i in range(12):

                new_dict = {}
                new_dict['Месторождение'] = list(self.data[j].keys())[0]
                try:
                    new_dict['ДО'] = company_dict[new_dict['Месторождение']]
                except:
                    print('Qlik Result || Месторождения ', new_dict['Месторождение'], 'нет в списке ДО')
                    new_dict['ДО'] = ''
                new_dict['Дата'] = self.dateline_export[i]

                try:
                    new_dict['Накопленная добычи нефти, исходный профиль, тыс.т.'] = indicators_init[0][i]
                    new_dict['Накопленная добычи нефти с учетом отключения НРФ, тыс.т.'] = indicators_nrf[0][i]
                    new_dict['Накопленная добычи нефти с учетом балансировки, тыс.т.'] = indicators[0][i]
                    new_dict['Накопленный FCF, исходный профиль, тыс.руб.'] = indicators_init[1][i]
                    new_dict['Накопленный FCF с учетом отключения НРФ, тыс.руб.'] = indicators_nrf[1][i]
                    new_dict['Накопленный FCF с учетом балансировки, тыс.руб.'] = indicators[1][i]
                    new_dict['Накопленная добычи жидкости, исходный профиль, тыс.т.'] = indicators_init[2][i]
                    new_dict['Накопленная добычи жидкости с учетом отключения НРФ, тыс.т.'] = indicators_nrf[2][i]
                    new_dict['Накопленная добычи жидкости с учетом балансировки, тыс.т.'] = indicators[2][i]
                except:
                    print('Qlick Result || error', new_dict['Месторождение'])

                list_of_dict.append(new_dict)
        for well in self.wells:
            well['ДО'] = company_dict[well['Месторождение']]
        df = pd.DataFrame(list_of_dict)
        return df
