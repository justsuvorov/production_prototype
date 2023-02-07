import pandas as pd
from Program.DOTests.WellDoFromSetOfWellsTest import *
from Program.Production.GoalFunction import GoalFunction
from Program.Production.InputParameters import InputParameters
from Program.Production.Optimizator import JayaOptimizator, GreedyOptimizer
from Program.Production.Production import ProductionOnValueBalancer
from Program.Production.ap_parameters import APParameters
from Program.Production.CalculationMethods import SimpleOperations


""" Входные параметры из Excel"""

"""


DATA = DATA_DIR / 'оперативное планирование добычи. Ранж по добыче с учетом бригад.xlsm'
df = pd.read_excel(DATA, sheet_name='Исходные данные', index_col=0)

date_start = dt.date(year=2022, month=11, day=1)
date_begin = dt.date(year=2022, month=12, day=1)
date_end = dt.date(year=2022, month=12, day=15)
time_lag_step = 0
max_objects_per_day = 5
value = 21.1
case = 3


#
# date_end = None
time_step = 'Day'
value = df['Исходные данные'].loc['Требуемый показатель']
case = df['Исходные данные'].loc['СЦЕНАРИЙ']
date_start = pd.to_datetime(df['Исходные данные'].loc['Текущая дата']).date()
date_begin = pd.to_datetime(df['Исходные данные'].loc['Начало периода']).date()
date_end = pd.to_datetime(df['Исходные данные'].loc['Конец периода']).date()
time_lag_step = df['Исходные данные'].loc['Количество дней на включение']
max_objects_per_day = df['Исходные данные'].loc['Максимальное количество бригад']
days_per_object = df['Исходные данные'].loc['Количество дней на включение']
economics = df['Исходные данные'].loc['Учет экономики']
if economics: b = 1
else: b = 0
a = 500
b = b * 60000000
c = 1

domain_model = domain_model()
parameters = APParameters(
    inKeys=['ObjectActivity'],
    outKeys=['Добыча нефти, тыс. т', 'FCF'],
    inValues=[[]]
)
"""

# parameters.from_domain_model(domain_model[0], last_index=13)
from pathlib import Path


def main(file_path: str):
    filepath = Path(file_path)
    DATA = filepath / 'Оперативное планирование добычи.xlsm'
    df = pd.read_excel(DATA, sheet_name='Исходные данные', index_col=0)

    # date_end = None
    time_step = 'Day'
    value = df['Исходные данные'].loc['Требуемый показатель']
    case = df['Исходные данные'].loc['СЦЕНАРИЙ']
    date_start = pd.to_datetime(df['Исходные данные'].loc['Текущая дата']).date()
    date_begin = pd.to_datetime(df['Исходные данные'].loc['Начало периода']).date()
    date_end = pd.to_datetime(df['Исходные данные'].loc['Конец периода']).date()
    time_lag_step = df['Исходные данные'].loc['Количество дней на включение']
    max_objects_per_day = df['Исходные данные'].loc['Максимальное количество бригад']
    days_per_object = df['Исходные данные'].loc['Количество дней на включение']
    economics = df['Исходные данные'].loc['Учет экономики']
    if economics:
        b = 1
    else:
        b = 0
    a = 500
    b = b * 60000000
    c = 3

    domain_model_main = domain_model(file_path=filepath)
    parameters = APParameters(
        inKeys=['ObjectActivity'],
        outKeys=['Добыча нефти, тыс. т', 'FCF'],
        inValues=[[]]
    )
    domain_model_main = SimpleOperations(
                                        domain_model=domain_model_main,
                                        end_year_index=59,
                                        indicator_name='FCF'
                                        ).wells_gap()


    
    parameters_of_algorithm = InputParameters(date_begin=date_begin,
                                              date_end=date_end,
                                              time_step=time_step,
                                              value=value,
                                              time_lag_step=time_lag_step,
                                              max_objects_per_day=max_objects_per_day,
                                              days_per_object=days_per_object,
                                              current_date=date_start,
                                              )

    program = ProductionOnValueBalancer(case=case,
                                        domain_model=domain_model_main,
                                        input_parameters=parameters_of_algorithm,
                                        optimizator=GreedyOptimizer(
                                                                    constraints=parameters_of_algorithm,
                                                                    parameters=parameters,
                                                                    goal_function=GoalFunction(
                                                                        parameters=parameters_of_algorithm,
                                                                        a=a,
                                                                    ),
                                                                    ),
                                        iterations_count=200,
                                        )
    program.result(path=filepath)
    """

    program = ProductionOnValueBalancer(case=case,
                                        domain_model=domain_model_main,
                                        input_parameters=parameters_of_algorithm,
                                        optimizator=JayaOptimizator(kids_number=2,
                                                                    parameters=parameters,
                                                                    goal_function=GoalFunction(
                                                                        parameters=parameters_of_algorithm,
                                                                        a=a,
                                                                        b=b,
                                                                        c=c,
                                                                    ),
                                                                    ),
                                        iterations_count=2,
                                        )
    program.result(path=filepath)


"""




if __name__ == '__main__':
    main()
