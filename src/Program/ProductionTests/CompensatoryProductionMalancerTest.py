import pandas as pd
from Program.DOTests.WellDoFromSetOfWellsTest import *
from Program.Production.GoalFunction import GoalFunction
from Program.Production.InputParameters import TimeParameters, ParametersOfAlgorithm
from Program.Production.Optimizator import GreedyOptimizer
from Program.Production.Production import OperationalProductionBalancer, CompensatoryProductionBalancer
from Program.Production.ap_parameters import APParameters
from Program.Production.ExcelResult import ExcelResult, ExcelResultPotential
from pathlib import Path
from Program.Production.PreparedDomainModel import PreparedDomainModel

import pickle


def main(file_path: str):
    filepath = Path(file_path)

    """ Входные параметры из Excel"""

    DATA = filepath / 'Балансировка компенсационных мероприятий для НРФ.xlsm'
    if os.path.exists(filepath/'СВОД_Скв_NGT.xlsm'):
        find_gap = False
    else:
        find_gap = True
    df = pd.read_excel(DATA, sheet_name='Исходные данные', index_col=0)
    time_step = 'Day'
    date_start = pd.to_datetime(df['Исходные данные'].loc['Текущая дата']).date()
    date_begin = pd.to_datetime(df['Исходные данные'].loc['Начало периода']).date()
    date_end = pd.to_datetime(df['Исходные данные'].loc['Конец периода']).date()

    time_lag_step = df['Исходные данные'].loc['Количество дней на включение']
    max_objects_per_day = df['Исходные данные'].loc['Максимальное количество бригад']
    days_per_object = df['Исходные данные'].loc['Количество дней на включение']
    #max_nrf_objects_per_day = df['Исходные данные'].loc['Максимальное количество выводимых объектов']
    #pump_extraction_value = df['Исходные данные'].loc['Стоимость подъема насоса']
    compensation = df['Исходные данные'].loc['Полная компенсация накопленной добычи']


    time_parameters = TimeParameters(
                                     date_end=date_end,
                                     date_begin=date_begin,
                                     time_step=time_step,
                                     current_date=date_start,
                                     )

    value = 9140.95
    domain_model_wells = PreparedDomainModel(domain_model=domain_model(file_path=filepath),
                                             time_parameters=time_parameters,
                                             find_gap=find_gap,
                                             path=file_path,
                                             )

    """
    with open('data.pickle', 'rb') as f:
        domain_model_wells = pickle.load(f)
    """
    parameters_of_algorithm = ParametersOfAlgorithm(
        value=value,
        time_lag_step=time_lag_step,
        max_objects_per_day=max_objects_per_day,
        days_per_object=days_per_object,
       # max_nrf_objects_per_day=max_nrf_objects_per_day,
       # pump_extraction_value=pump_extraction_value,
        compensation=compensation,
    )

    parameters_of_optimization = APParameters(
        inKeys=['ObjectActivity'],
        outKeys=['Добыча нефти, тыс. т', 'FCF'],
        inValues=[[]]
    )

    program = CompensatoryProductionBalancer(
                                        prepared_domain_model=domain_model_wells,
                                        input_parameters=parameters_of_algorithm,
                                        optimizator=GreedyOptimizer(
                                            constraints=parameters_of_algorithm,
                                            parameters=parameters_of_optimization,
                                            goal_function=GoalFunction(
                                                parameters=parameters_of_algorithm,
                                            ),
                                        ),
                                        iterations_count=200,
                                        )

    domain_model_with_results = program.result(path=filepath)

    ExcelResultPotential(domain_model=domain_model_with_results,
                production=program,
                results='Only sum',
                dates=time_parameters,
                # file_path = file_path
                ).save(path=filepath)


if __name__ == '__main__':
    main()
