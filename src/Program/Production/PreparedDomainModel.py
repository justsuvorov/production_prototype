from copy import deepcopy
import pandas as pd
from Program.Production.InputParameters import TimeParameters
import datetime as dt
import numpy as np
from Program.Production.CalculationMethods import SimpleOperations
from pathlib import Path


class PreparedDomainModel:
    """
    Класс подготовки доменной модели для балансировщика. Фильтрует объекты для выбранных ДО/месторождений,
    преобразует месячные показатели в суточные

    inputs:
    domain_model: доменная модель в виде словаря
    time_parameters: исходные параметры алгоритма балансировки (даты)
    find_gap: пареметр расчета ГЭП (если False, то импортируется из NGT)
    filter: фильтр выбранных ДО и месторождения для расчета в виде словаря
    path: путь к исходным данным

    :returns
    recalculate_indicators(): возвращает доменную модель с выбранными ДО и Месторождениями с суточными показателями
                Возвращает параметры дат для балансировки в виде индексов. (См. SimpleOperations)


    """
    def __init__(self,
                 domain_model: dict,
                 time_parameters: TimeParameters,
                 find_gap: bool = False,
                 filter: dict = {'company': 'All', 'field': 'All'},
                 path=None,
                 ):
        self.domain_model = domain_model
        self.time_parameters = time_parameters
        self.steps_count = None
        self.find_gap = find_gap
        self.path = path
        self.filter = filter

    def recalculate_indicators(self):
        domain_model = self.__copy_domain_model()
        wells = domain_model[0]
        clusters = domain_model[1]
        fields = domain_model[2]
        if self.find_gap:
            SimpleOperations(domain_model=wells,
                             indicator_name='FCF',
                             end_year_index=59,
                             ).wells_gap()
            print('ГЭП рассчитан')

        else:
            if self.path != None:
                filepath = Path(self.path)
                DATA = filepath / 'СВОД_Скв_NGT.xlsm'
                domain_model[0] = self.__export_gap(data=DATA, wells=wells)
                print('ГЭП импортирован')
            else:
                raise FileNotFoundError('Нет файла с GAP')
        wells, clusters, fields = self.__filter_objects(wells=wells, clusters=clusters, fields=fields)
        time_parameters = self._discretizate_parameters(domain_model=wells)
        prepared_domain_model = {}
        prepared_domain_model['Wells'] = wells
        prepared_domain_model['Clusters'] = clusters
        prepared_domain_model['Fields'] = fields

        return prepared_domain_model, time_parameters

    def __export_gap(self, data, wells):
        try:
            df = pd.read_excel(data)['GAP'].to_numpy()
        except:
            raise FileNotFoundError('Нет файла с GAP')
        i = 0
        for object in wells:
            if i < (len(df)):
                object.indicators['Gap index'] = df[i]
                i += 1
            else:
                object.indicators['Gap index'] = 60
        return wells

    def __copy_domain_model(self):
        return deepcopy(self.domain_model)
        
    def _discretizate_parameters(self, domain_model):
        time_step = self.time_parameters.time_step

        if time_step == 'Day':
            steps_count = 366
            date1 = (self.time_parameters.date_begin - self.time_parameters.date_start).days
            self._recalculate_indicators(step=30, domain_model=domain_model)
            if self.time_parameters.date_end is not None:
                date2 = (self.time_parameters.date_end - self.time_parameters.date_start).days

            else:
                date2 = self.steps_count
                print('date2 is the end of the period ')

        if time_step == 'Month':
            steps_count = 13
            a = ((self.time_parameters.date_begin.year - self.time_parameters.date_start.year) * 12) +\
                self.time_parameters.date_begin.month - self.time_parameters.date_start.month
            date1 = a
            if self.time_parameters.date_end is not None:
                b = ((self.time_parameters.date_end.year - self.time_parameters.date_start.year) * 12) + \
                    self.time_parameters.date_end.month - self.time_parameters.date_start.month
                date2 = b
            else:
                date2 = self.steps_count
                print('date2 is the end of the period ')

        if time_step == 'Week':
            steps_count = 55
            self._recalculate_indicators(step=3, domain_model=domain_model)

            def find_weeks(start_date, end_date):
                subtract_days = start_date.isocalendar()[2] - 1
                current_date = start_date + dt.timedelta(days=7 - subtract_days)
                weeks_between = []
                while current_date <= end_date:
                    weeks_between.append(
                        '{}{:02d}'.format(*current_date.isocalendar()[:2])
                    )
                    current_date += dt.timedelta(days=7)
                return weeks_between

            date1 = find_weeks(self.time_parameters.date_begin, self.time_parameters.date_start)
            if self.time_parameters.date_end is not None:
                date2 = find_weeks(self.time_parameters.date_end, self.time_parameters.date_start)
            else:
                date2 = self.steps_count
                print('date2 is the end of the period ')
        current_date = (self.time_parameters.current_date - self.time_parameters.date_start).days

        return {'date1': date1, 'date2': date2,  'steps_count': steps_count, 'current_date': current_date}

    def _recalculate_indicators(self, step: int, domain_model):
        step = 30.43
        for object in domain_model:
            try:
                for key in object.indicators:
                    if key != 'Gap index':
                        try:
                            l = (object.indicators[key].size - 1) * step + 1  # total length after interpolation
                            c = np.array(object.indicators[key]).astype(float)
                            c = c/step
                            new_arr = (c[1:]-c[:-1])*0.5
                            new_arr = np.insert(new_arr, -1, 0)
                            c = c - new_arr
                            a = np.interp(np.arange(l), np.arange(l, step=step), c)  # interpolate
                            object.indicators[key] = a
                        except:
                            print('Cannot recalculate indicators for well ', object.name)
            except:
                print()

    def __filter_objects(self, wells, clusters, fields):
        new_wells = []
        new_fields = []
        result_wells =[]
        result_clusters = []
        result_fields = []
        new_wells_list = []
        new_fields_list = []

        if self.filter['field'] != 'All':
            print('Расчет для ДО: ', self.filter['company'], ' Месторождение: ', self.filter['field'])

            for name in self.filter['field']:
                for field in fields:
                    if field.name[0] == name:
                        new_wells_list.append(field.link['Wells'])
                        new_fields_list.append(field)

            if not new_fields_list:
                print('В исходных данных нет выбранных месторождений!')

            for item in new_wells_list:
                new_wells.extend(item)
            for well in wells:
                if well in new_wells:
                    result_wells.append(well)
            for cluster in clusters:
                for well in result_wells:
                    if well in cluster.link['Wells'] and cluster not in result_clusters:
                        result_clusters.append(cluster)
            result_fields = new_fields_list


        else:
            result_wells = wells
            result_clusters = clusters
            result_fields = fields
        return result_wells, result_clusters, result_fields


class NRFPreparedDomainModel(PreparedDomainModel):
    def __init__(self,
                 domain_model: dict,
                 ):
        super().__init__(domain_model=domain_model,
                         time_parameters=TimeParameters(),
                         find_gap=False,
                         )
        self.domain_model = domain_model

    def full_domain_model(self):
        domain_model = self.__copy_domain_model()
        wells = domain_model[0]
        pads = domain_model[1]
        clusters = domain_model[2]
        fields = domain_model[3]


        if self.find_gap:
            SimpleOperations(domain_model=wells,
                             indicator_name='FCF',
                             end_year_index=59,
                             ).wells_gap()
            print('ГЭП рассчитан')

        else:
            if self.path != None:
                filepath = Path(self.path)
                DATA = filepath / 'СВОД_Скв_NGT.xlsm'
                domain_model[0] = self.__export_gap(data=DATA, wells=wells)
                print('ГЭП импортирован')
            else:
                raise FileNotFoundError('Нет файла с GAP')
        wells, clusters, fields = self.__filter_objects(wells=wells, clusters=clusters, fields=fields)
        time_parameters = self._discretizate_parameters(domain_model=wells)
        prepared_domain_model = {}
        prepared_domain_model['Wells'] = wells
        prepared_domain_model['Clusters'] = clusters
        prepared_domain_model['Fields'] = fields

        return prepared_domain_model