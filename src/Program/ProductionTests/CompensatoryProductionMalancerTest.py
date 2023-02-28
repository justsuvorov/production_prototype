from Program.DOTests.WellDoFromSetOfWellsTest import *
from Program.Production.GoalFunction import GoalFunction
from Program.Production.GuiInputInterface import ExcelInterface
from Program.Production.Optimizator import GreedyOptimizer
from Program.Production.Production import OperationalProductionBalancer, CompensatoryProductionBalancer
from Program.Production.ap_parameters import APParameters
from Program.Production.ExcelResult import ExcelResult, ExcelResultPotential
from pathlib import Path
from Program.Production.PreparedDomainModel import PreparedDomainModel

def main(file_path: str):
    filepath = Path(file_path)

    """ Входные параметры из Excel"""
    gui = ExcelInterface(filepath=filepath)
    time_parameters = gui.time_parameters()
    parameters_of_algorithm = gui.parameter_of_algorithm()
    find_gap = gui.find_gap()
    imported_domain_model = domain_model(file_path=filepath)
    for iteration_index in range(gui.iterations()):

        filter = gui.chosen_objects(iteration_index=iteration_index)
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

     #   try:
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
        if len(gui.companies_names) > 1:
            a = str(file_path) + '\\' + str(gui.companies_names[iteration_index]) + '\\'
            Path(a).mkdir(parents=True, exist_ok=True)
            result_path = Path(a)
        else:
            result_path = filepath
        domain_model_with_results = program.result(path=result_path)

        ExcelResultPotential(
                            domain_model=domain_model_with_results['Wells'],
                            production=program,
                            results='Only sum',
                            dates=time_parameters,
                            ).save(path=result_path)
       # except:
      #      print('Невозможно произвести расчет для ', filter['company'])

if __name__ == '__main__':
    main()
