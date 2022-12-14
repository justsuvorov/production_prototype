from DOTests.WellDoFromSetOfWellsTest import main
from Production.ap_parameters import APParameters
from Production.CalculationMethods import *
from Production.Production import *
from Production.Optimizator import *
import datetime as dt


domain_model = main()

date_start = dt.date(year=2022, month=11, day=1)
date_begin = dt.date(year=2023, month=1, day=1)
date_end = dt.date(year=2023, month=3, day=1)
date_end = None
time_step = 'Day'
time_lag_step = 5
max_objects_per_day = 5
value = 20

parameters = APParameters(
    inKeys=['ObjectActivity'],
    outKeys=['Добыча нефти, тыс. т', 'FCF'],
    inValues=[[]]
)
parameters.from_domain_model(domain_model[0], last_index=13)

program = ProductionOnValueBalancer(case=1,
                                    domain_model=domain_model,
                                    input_parameters=InputParameters(date_begin=date_begin,
                                                                     date_end=date_end,
                                                                     time_step=time_step,
                                                                     value=value
                                                                     ),
                                    optimizator=JayaOptimizator(kids_number=7,
                                                                parameters=parameters,
                                                                ),
                                    iterations_count=30,
                                    )
program.result()



