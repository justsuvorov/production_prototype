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
from Program.Production.CalculationMethods import SimpleOperations
import pickle


def main(file_path: str):
    filepath = Path(file_path)

    """ Входные параметры из Excel"""

    DATA = filepath / 'оперативное планирование добычи. Ранж по добыче с учетом бригад.xlsm'
    df = pd.read_excel(DATA, sheet_name='Исходные данные', index_col=0)
    time_step = 'Day'
    date_start = pd.to_datetime(df['Исходные данные'].loc['Текущая дата']).date()
    time_lag_step = df['Исходные данные'].loc['Количество дней на включение']
    max_objects_per_day = df['Исходные данные'].loc['Максимальное количество бригад']
    days_per_object = df['Исходные данные'].loc['Количество дней на включение']
    max_nrf_objects = df['Исходные данные'].loc['Максимальное количество выводимых объектов']

    time_parameters = TimeParameters(
                                     time_step=time_step,
                                     current_date=date_start
                                     )

    value = 9140.95
    domain_model_wells = PreparedDomainModel(domain_model=domain_model(file_path=filepath),
                                             time_parameters=time_parameters,
                                             find_gap=True,
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
        max_nrf_objects=max_nrf_objects
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
