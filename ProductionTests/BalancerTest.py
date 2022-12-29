import pandas as pd

from DOTests.WellDoFromSetOfWellsTest import domain_model
from Production.GoalFunction import GoalFunction
from Production.ap_parameters import APParameters
from Production.CalculationMethods import *
from Production.Production import *
from Production.Optimizator import *
import datetime as dt
from pathlib import Path


""" Входные параметры из Excel"""


path = os.getcwd()
DATA = Path(path+'\оперативное планирование добычи. Ранж по добыче с учетом бригад.xlsm')
df = pd.read_excel(DATA, sheet_name='Исходные данные', index_col=0)
"""
date_start = dt.date(year=2022, month=11, day=1)
date_begin = dt.date(year=2022, month=12, day=1)
date_end = dt.date(year=2022, month=12, day=15)
time_lag_step = 0
max_objects_per_day = 5
value = 21.1
case = 3

"""
#
#date_end = None
time_step = 'Day'
value = df['Исходные данные'].loc['Требуемый показатель']
case = df['Исходные данные'].loc['СЦЕНАРИЙ']
date_start = pd.to_datetime(df['Исходные данные'].loc['Текущая дата']).date()
date_begin = pd.to_datetime(df['Исходные данные'].loc['Начало периода']).date()
date_end = pd.to_datetime(df['Исходные данные'].loc['Конец периода']).date()
time_lag_step = df['Исходные данные'].loc['Количество дней на включение']
max_objects_per_day = df['Исходные данные'].loc['Максимальное количество бригад']
days_per_object = df['Исходные данные'].loc['Количество дней на включение']

a = 500
b = 60000000
c = 1



domain_model = domain_model()
parameters = APParameters(
    inKeys=['ObjectActivity'],
    outKeys=['Добыча нефти, тыс. т', 'FCF'],
    inValues=[[]]
)
#parameters.from_domain_model(domain_model[0], last_index=13)



def main():
    parameters_of_algorithm = InputParameters(date_begin=date_begin,

                                              date_end=date_end,
                                              time_step=time_step,
                                              value=value,
                                              time_lag_step=time_lag_step,
                                              max_objects_per_day=max_objects_per_day,
                                              days_per_object=days_per_object

                                              )

    program = ProductionOnValueBalancer(case=case,
                                        domain_model=domain_model,
                                        input_parameters=parameters_of_algorithm,
                                        optimizator=JayaOptimizator(kids_number=6,
                                                                    parameters=parameters,
                                                                    goal_function=GoalFunction(parameters=parameters_of_algorithm,
                                                                                               a=a,
                                                                                               b=b,
                                                                                               c=c,
                                                                                               ),
                                                                    ),
                                        iterations_count=50,
                                        )
    program.result()


if __name__ == '__main__':
    main()
