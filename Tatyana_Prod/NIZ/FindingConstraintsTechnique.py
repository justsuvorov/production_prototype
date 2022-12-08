import numpy as np
import pandas as pd
from typing import Optional
import math
from sklearn.linear_model import LinearRegression

from constants import MERNames


class OIZ():
    """Класс, характеризующий ОИЗ скважины
    Принимает на вход:
            :param well:  скважинa
            :param min_reserves: минимальное значение ОИЗ
            :param year_min: минимальное время работы скважины (лет)
            :param year_max: максимальное время раоты скважины (лет)
            """

    def __init__(self, state: pd.DataFrame,
                 min_reserves: Optional[float]=2000,
                 year_min: Optional[int] = 5,
                 year_max: Optional[int] = 20):

        self.df_well = state

        if min_reserves is not None:
            self.min_reserves = min_reserves
        if year_min is not None:
            self.year_min = year_min
        if year_max is not None:
            self.year_max = year_max


    #получить значение, работала ли скважина в один из трех последних месяцев факта
    def calculate_oiz(self):

        name_well = self.df_well.index[0]
        well_error=0

        df_result = self.calculate_reserves_statistics(self.df_well, name_well)[0]
        if df_result.empty:
            df_result = self.calculate_reserves_statistics(self.df_well, name_well, marker=1)[0]
            if df_result.empty:
                well_error=name_well

        if well_error==name_well:
            self.df_well['qnak'] = self.df_well[MERNames.OIL_PRODUCTION].cumsum()
            cumulative_op = self.df_well['qnak'].values[-1]
            if len(self.df_well['qnak']) > 1:
                #  Добыча нефти за предпоследний месяц
                Q_next_to_last = float(self.df_well[MERNames.OIL_PRODUCTION][-2:-1])
            else:
                Q_next_to_last = 0
            Q_last = self.df_well[MERNames.OIL_PRODUCTION].values[-1]

            New_OIZ = cumulative_op * 0.5 + self.min_reserves
            work_time = New_OIZ / (Q_last * 12)
            if work_time > self.year_max:
                New_OIZ = (Q_last + Q_next_to_last) * self.year_max * 6
            elif work_time < self.year_min:
                New_OIZ = (Q_last + Q_next_to_last) * self.year_min * 6
            if New_OIZ < self.min_reserves:
                New_OIZ = self.min_reserves
            New_NIZ=int(New_OIZ + cumulative_op)

            #df_result = pd.DataFrame()
            df_result = pd.DataFrame(data={'ОИЗ Right': [New_OIZ], 'ОИЗ Left': [New_OIZ/2], \
                                           'НИЗ': [New_NIZ], 'Накопленная добыча,т': [cumulative_op]})

        df_result = self.count_int_oiz(df_result)
        df_result['ОИЗ Right'] = df_result['ОИЗ Right'] / 1000
        df_result['ОИЗ Left'] = df_result['ОИЗ Left'] / 1000
        return df_result



    def calculate_reserves_statistics(self, df_well, name_well, marker=0):
        """
        Расчет остаточных извлекаемых запасов для скважины на основе истории работы
        :param df_well: МЭР
        :param name_well: идентификатор скважины
        :param marker: отметка 0 расчет по всем точкам истории, 1 для последних трех
        :return: df_well_result: DataFrame[columns= {'Скважина';
                                            "НИЗ";
                                            "ОИЗ";
                                            'Метод';
                                            'Добыча за посл мес, т';
                                            'Добыча за предпосл мес, т';
                                            'Накопленная добыча,т';
                                            'Korelation';
                                            'Sigma';
                                            'Время работы, прогноз,лет';
                                            'Время работы, прошло, лет';
                                            'Координата Х';
                                            'Координата Y'}],
                 error: ошибка, из-за которой не были рассчитаны ОИЗ
        """
        error = ""

        #  Подготовка осей
        df_well['qnak'] = df_well[MERNames.OIL_PRODUCTION].cumsum()
        df_well['qnak_liq'] = df_well[MERNames.LIQUID_PRODUCTION].cumsum()
        df_well['qnak_water'] = df_well['qnak_liq'] - df_well['qnak']
        df_well['y'] = df_well['qnak_liq'] / df_well['qnak']
        df_well['log_Ql'] = np.log(df_well['qnak_water']).replace(-np.inf, 0)
        df_well['log_Qw'] = np.log(df_well['qnak'])
        df_well['log_Qn'] = np.log(df_well['qnak_liq'])
        df_well['Год'] = df_well[MERNames.DATE].map(lambda x: x.year)

        Q_next_to_last = 0
        if marker == 0:
            if len(df_well['qnak']) > 1:
                #  Добыча нефти за предпоследний месяц
                Q_next_to_last = float(df_well[MERNames.OIL_PRODUCTION][-2:-1])
            else:
                error = "одна точка"
        else:
            if len(df_well['qnak']) > 2:
                df_well = df_well.tail(3)
                Q_last = float(df_well[MERNames.OIL_PRODUCTION][-1:])
                Q_next_to_last = float(df_well[MERNames.OIL_PRODUCTION][-2:-1])
                if (Q_last / Q_next_to_last) < 0.25:
                    df_well = df_well[:-1]

        cumulative_op = df_well['qnak'].values[-1]
        #  Сколько лет работала скважина
        work_time = int(df_well['Год'].tail(1)) - int(df_well['Год'].head(1))

        """Статистические методы"""
        reserves1, residual_reserves1, Korelation1, Determination1 = self.Linear_model(df_well, "Nazarov_Sipachev")
        reserves2, residual_reserves2, Korelation2, Determination2 = self.Linear_model(df_well, "Sipachev_Pasevich")
        reserves3, residual_reserves3, Korelation3, Determination3 = self.Linear_model(df_well, "FNI")
        reserves4, residual_reserves4, Korelation4, Determination4 = self.Linear_model(df_well, "Maksimov")
        reserves5, residual_reserves5, Korelation5, Determination5 = self.Linear_model(df_well, "Sazonov")

        #  Формирование итогового DataFrame
        df_well_result = pd.DataFrame()
        df_well_result['НИЗ'] = [reserves1, reserves2, reserves3, reserves4, reserves5]
        df_well_result['ОИЗ Right'] = [residual_reserves1, residual_reserves2, residual_reserves3, residual_reserves4,
                                 residual_reserves5]
        df_well_result['ОИЗ Left'] = None
        df_well_result['Метод'] = ['Назаров_Сипачев', 'Сипачев_Пасевич', 'ФНИ', 'Максимов', 'Сазонов']
        df_well_result['Добыча за посл мес, т'] = df_well[MERNames.OIL_PRODUCTION].values[-1]
        df_well_result['Добыча за предпосл мес, т'] = Q_next_to_last
        df_well_result['Накопленная добыча,т'] = cumulative_op
        df_well_result['Скважина'] = name_well
        df_well_result['Korelation'] = [Korelation1, Korelation2, Korelation3, Korelation4, Korelation5]
        df_well_result['Время работы, прогноз,лет'] = df_well_result['ОИЗ Right'] / (
                    df_well_result['Добыча за посл мес, т'] * 12)
        df_well_result['Время работы, прошло, лет'] = work_time
        df_well_result = df_well_result.loc[df_well_result['ОИЗ Right'] > 0]
        if df_well_result.empty:
            error = "residual_reserves < 0"

        df_up = df_well_result.loc[df_well_result['Korelation'] > 0.7]
        df_down = df_well_result.loc[df_well_result['Korelation'] < (-0.7)]
        df_well_result = pd.concat([df_up, df_down]).reset_index()
        if df_well_result.empty:
            error = "Korelation <0.7 & >-0.7"

        df_well_result = df_well_result.loc[df_well_result['Время работы, прогноз,лет'] < 50]
        if df_well_result.empty:
            error = "work_time > 50"

        df_well_result = df_well_result.sort_values('ОИЗ Right').reset_index(drop=True)

        #найти левую границу интервала, в котором будет найден ОИЗ
        if not df_well_result.empty:
            df_well_result['ОИЗ Left'] = df_well_result.loc[0, 'ОИЗ Right']
        df_well_result = df_well_result.tail(1)

        if not df_well_result.empty:
            if marker == 0:
                df_well_result['Метка'] = 'Расчет по всем точкам'
            else:
                df_well_result['Метка'] = 'Расчет по последним 3м точкам'

        return df_well_result, error


    def count_int_oiz(self, model: pd.DataFrame):
        model = model.reset_index(drop=True)
        try:
            model.loc[0, 'Метод']
            #случай, когда данные настолько плохие, что статистическими методами считать нелогично
        except:
            return model
        if model.loc[0,'ОИЗ Left'] == model.loc[0,'ОИЗ Right'] or model.loc[0,'ОИЗ Left'] is None:
            WC_last = 1 - self.df_well[MERNames.OIL_PRODUCTION][-1] / self.df_well[MERNames.LIQUID_PRODUCTION][-1]
            RF = WC_last/(1-WC_last)
            niz = model.loc[0, 'Накопленная добыча,т'] / RF
            oiz = niz - model.loc[0, 'Накопленная добыча,т']
            #проверка на адекват
            if (oiz/ (model.loc[0, 'Добыча за посл мес, т'] * 12)) > 75:
                oiz = 75 * 12 * model.loc[0,'Добыча за посл мес, т']
            if oiz < model.loc[0, 'ОИЗ Right']:
                model.loc[0, 'ОИЗ Left'] = oiz
            else:
                model.loc[0, 'ОИЗ Left'] = model.loc[0, 'ОИЗ Right']
                model.loc[0, 'ОИЗ Right'] = oiz
        #elif model.loc[0, 'ОИЗ Right'] - model.loc[0, 'ОИЗ Left'] > 10:
            #return model
        model = model.loc[:, ['ОИЗ Right', 'ОИЗ Left', 'НИЗ', 'Накопленная добыча,т', 'Время работы, прогноз,лет']]
        return model


    #модели ХВ
    def Linear_model(self, df, param):
        if param == "Nazarov_Sipachev":  # Назаров_Сипачев
            x = df['qnak_water'].values.reshape((-1, 1))
            y = df['y']
        elif param == "Sipachev_Pasevich":
            x = df['qnak_liq'].values.reshape((-1, 1))
            y = df['y']
        elif param == "FNI":
            x = df['qnak'].values.reshape((-1, 1))
            y = df['y']
        elif param == "Maksimov":
            x = df['qnak'].values.reshape((-1, 1))
            y = df['log_Qw']
        elif param == "Sazonov":
            x = df['qnak'].values.reshape((-1, 1))
            y = df['log_Ql']

        model = LinearRegression().fit(x, y)
        a = model.intercept_
        b = model.coef_
        b = float(b)
        b = math.fabs(b)
        Qo = df['qnak'].values[-1]
        if b != 0:
            if param == "Nazarov_Sipachev":
                q_izv = (1 / b) * (1 - ((a - 1) * (1 - 0.99) / 0.99) ** 0.5)
            elif param == "Sipachev_Pasevich":
                q_izv = (1 / b) - ((0.01 * a) / (b ** 2)) ** 0.5
            elif param == "FNI":
                q_izv = 1 / (2 * b * (1 - 0.99)) - a / 2 * b
            elif param == "Maksimov":
                q_izv = (1 / b) * math.log(0.99 / ((1 - 0.99) * b * math.exp(a)))
            elif param == "Sazonov":
                try:
                    q_izv = (1 / b) * math.log(0.99 / ((1 - 0.99) * b * math.exp(a)))
                except ZeroDivisionError:
                    q_izv = 0
            OIZ = q_izv - Qo
        else:
            q_izv = 0
            OIZ = 0
        # k = np.corrcoef(df['qnak_water'], df['y'])
        Korelation = math.fabs(np.corrcoef(df['qnak_water'], df['y'])[1, 0])
        Determination = model.score(x, y)

        return q_izv, OIZ, Korelation, Determination