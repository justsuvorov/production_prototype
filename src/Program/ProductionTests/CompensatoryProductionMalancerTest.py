from Program.DOTests.WellDoFromSetOfWellsTest import *
from Program.Production.GoalFunction import GoalFunction
from Program.Production.GuiInputInterface import ExcelInterface
from Program.Production.Optimizator import GreedyOptimizer
from Program.Production.Production import OperationalProductionBalancer, CompensatoryProductionBalancer
from Program.Production.ap_parameters import APParameters
from Program.Production.ExcelResult import ExcelResult, ExcelResultPotential, QlikExcelResult
from pathlib import Path
from Program.Production.PreparedDomainModel import PreparedDomainModel
import pickle

def main(file_path: str):
    filepath = Path(file_path)

    """ Входные параметры из Excel"""
    gui = ExcelInterface(filepath=filepath)
    all_companies_option, all_fields_option = gui.calculation_parameters()
    time_parameters = gui.time_parameters()
    find_gap = gui.find_gap()
    imported_domain_model = domain_model(file_path=filepath)
    qlik_result = QlikExcelResult(
                                  dates=time_parameters)
    for company_index in range(gui.company_iterations()):
        for field_index in range(gui.field_iterations(company_index=company_index)):
            filter = gui.chosen_objects(company_index=company_index, field_index=field_index)
            parameters_of_algorithm = gui.parameter_of_algorithm(company_index=company_index, field_index=field_index)

            parameters_of_optimization = APParameters(inKeys=['ObjectActivity'],
                                                      outKeys=['Добыча нефти, тыс. т', 'FCF'],
                                                      inValues=[[]]
                                                      )
            domain_model_wells = PreparedDomainModel(domain_model=imported_domain_model,
                                                     time_parameters=time_parameters,
                                                     find_gap=find_gap,
                                                     path=file_path,
                                                     filter=filter
                                                     )

            try:
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

                if all_companies_option:
                    folder = str(file_path) + '\\' + str(gui.companies_names[company_index]) + '\\'
                    a = folder
                    Path(folder).mkdir(parents=True, exist_ok=True)
                    filepath = Path(folder)

                if all_fields_option:
                    if not all_companies_option:
                        a = str(file_path) + '\\' + str(gui.companies_names[company_index]) + '\\'
                    folder = a + '\\' + str(gui.fields_names[field_index]) + '\\'
                    Path(folder).mkdir(parents=True, exist_ok=True)
                    filepath = Path(folder)

                domain_model_with_results = program.result(path=filepath, qlik_result=qlik_result)

                ExcelResultPotential(
                                    domain_model=domain_model_with_results['Wells'],
                                    production=program,
                                    results='Only sum',
                                    dates=time_parameters,
                                    ).save(path=filepath)

                qlik_result.load_data_from_domain_model(domain_model=domain_model_with_results,
                                )
                qlik_result.load_data_from_domain_model(domain_model=domain_model_with_results,
                                                        cut_index=program.vbd_index,
                                                        nrf=True)

            except:
                print('Невозможно произвести расчет для ', filter['company'], filter['field'])

    qlik_result.save(path=Path(file_path))
if __name__ == '__main__':
    main()
