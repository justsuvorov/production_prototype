from DOTests.WellDoFromSetOfWellsTest import main
from Production.GoalFunction import GoalFunction
from Production.ap_parameters import APParameters
from Production.CalculationMethods import *
from Production.Production import *
from Production.Optimizator import *
import datetime as dt


domain_model = main()

date_start = dt.date(year=2022, month=11, day=1)
date_begin = dt.date(year=2023, month=8, day=1)
date_end = dt.date(year=2023, month=10, day=1)
#date_end = None
time_step = 'Month'
time_lag_step = 0
max_objects_per_day = 5
value = 480

parameters = APParameters(
    inKeys=['ObjectActivity'],
    outKeys=['Добыча нефти, тыс. т', 'FCF'],
    inValues=[[]]
)
#parameters.from_domain_model(domain_model[0], last_index=13)

program = ProductionOnValueBalancer(case=1,
                                    domain_model=domain_model,
                                    input_parameters=InputParameters(date_begin=date_begin,
                                                                     date_end=date_end,
                                                                     time_step=time_step,
                                                                     value=value,
                                                                     time_lag_step=time_lag_step,
                                                                     max_objects_per_day=max_objects_per_day
                                                                     ),
                                    optimizator=JayaOptimizator(kids_number=7,
                                                                parameters=parameters,
                                                                goal_function=GoalFunction(parameters=InputParameters(date_begin=date_begin,
                                                                                                                      date_end=date_end,
                                                                                                                      time_step=time_step,
                                                                                                                      value=value,
                                                                                                                      time_lag_step=time_lag_step,
                                                                                                                      max_objects_per_day=max_objects_per_day
                                                                                                                      ),
                                                                                           ),

                                                                ),
                                    iterations_count=30,
                                    )
program.result()



