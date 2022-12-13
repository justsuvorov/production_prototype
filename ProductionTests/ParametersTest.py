from DOTests.WellDoFromSetOfWellsTest import main
from Production.ap_parameters import APParameters
from Production.CalculationMethods import *
from Production.Production import *
from Production.Optimizator import *
import datetime as dt


domain_model = main()

date_begin = dt.date(year=2022, month=12, day=1)
date_end = dt.date(year=2022, month=4, day=1)
time_step = 'month'
value = 0.65



parameters = APParameters(
    inKeys=['ObjectActivity'],
    outKeys=['Добыча нефти, тыс. т', 'FCF'],
    inValues=[[]]
)

parameters.from_domain_model(domain_model[0])
print(parameters)


program = ProductionOnValueBalancer(case=1,
                          domain_model=domain_model,
                          input_parameters=InputParameters(
                              date_begin = date_begin,
                              date_end=date_end,
                              time_step=time_step,
                              value=value
                          ),
                          optimizator=JayaOptimizator(kids_number=10,
                                                      parameters=parameters),
                          iterations_count=20,
                          )
program.result()



