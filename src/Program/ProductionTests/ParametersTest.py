from Program.DOTests.WellDoFromSetOfWellsTest import main
from Program.Production.GoalFunction import GoalFunction
from Program.Production.ap_parameters import APParameters
import datetime as dt


domain_model = main()

date_start = dt.date(year=2022, month=11, day=1)
date_begin = dt.date(year=2022, month=12, day=1)
date_end = dt.date(year=2022, month=12, day=15)
#date_end = None
time_step = 'Day'
time_lag_step = 0
max_objects_per_day = 5
value = 21.1
case = 3

a = 500
b = 60000000
c = 1

parameters = APParameters(
    inKeys=['ObjectActivity'],
    outKeys=['Добыча нефти, тыс. т', 'FCF'],
    inValues=[[]]
)
#parameters.from_domain_model(domain_model[0], last_index=13)

parameters_of_algorithm = InputParameters(date_begin=date_begin,
                                          date_end=date_end,
                                          time_step=time_step,
                                          value=value,
                                          time_lag_step=time_lag_step,
                                          max_objects_per_day=max_objects_per_day,

                                          )

program = ProductionOnValueBalancer(case=case,
                                    domain_model=domain_model,
                                    input_parameters=parameters_of_algorithm,
                                    optimizator=JayaOptimizator(kids_number=1,
                                                                parameters=parameters,
                                                                goal_function=GoalFunction(parameters=parameters_of_algorithm,
                                                                                           a=a,
                                                                                           b=b,
                                                                                           c=c,
                                                                                           ),
                                                                ),
                                    iterations_count=1,
                                    )
program.result()



