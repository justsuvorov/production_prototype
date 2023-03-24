import pandas as pd
import numpy as np
from pathlib import Path
import enum
import pathlib

from edifice import Label,  Slider, TextInput, View, CheckBox, Component, StateManager, Window
from edifice.components.forms import FormDialog, Form
from edifice.components import plotting


from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score



from Program.ObjectBuilders.Parser import GfemParser

class GfemDataFrame:
    def __init__(self,
                 file_path: str,
                 ):
        self.file_path = file_path
        self.path = file_path + '\СВОД_Скв_формат из ГФЭМ.xlsm'
        self.parser = GfemParser(data_path=self.path)

    def result(self):
        return self._recalculate_indicators()

    def _data(self) -> pd.DataFrame:
        return self.parser.data()

    def _recalculate_indicators(self):
        data = self._data()
        companydict = CompanyDict(path=self.file_path)
        company_dict = companydict.load(scenario_program=True)
        prepared_data = pd.DataFrame()
        prepared_data['Месторождение'] = data['Месторождение']
        prepared_data['Скважина'] = data['Скважина']
        prepared_data['Куст'] = data['Куст']
        prepared_data['FCF первый месяц'] = data['FCF первый месяц:']/1000
        prepared_data['НДН за первый месяц; тыс. т'] = data['НДН за первый месяц; тыс. т']
        prepared_data['НДН за первый месяц; т./сут.'] =  prepared_data['НДН за первый месяц; тыс. т']/(365/12)*1000
        prepared_data['Уд.FCF на 1 тн. (за 1 мес.)'] = prepared_data['FCF первый месяц']/\
                                                       prepared_data['НДН за первый месяц; т./сут.']
        prepared_data['Доля СП по добыче'] = 1
        prepared_data['Доля СП по FCF'] = 1
        prepared_data['ДО'] = 'ГПН'
        for index, row in prepared_data.iterrows():
            row['ДО'] = company_dict[row['Месторождение']]
            prepared_data.at[index,'ДО'] = company_dict[row['Месторождение']]
            prepared_data.at[index,'Доля СП по добыче'] = companydict.joint_venture_crude_part[row['ДО']]
            prepared_data.at[index,'Доля СП по FCF'] = companydict.joint_venture_fcf_part[row['ДО']]

           # row['НДН за первый месяц; т./сут.'] =

        prepared_data['НДН за первый месяц; тыс. т. с долей СП'] = prepared_data['НДН за первый месяц; тыс. т'] * prepared_data['Доля СП по добыче']
        prepared_data['FCF первый месяц c долей СП'] = prepared_data['FCF первый месяц'] * prepared_data['Доля СП по FCF']
        prepared_data['НДН за первый месяц; т./сут. с долей СП'] = prepared_data['НДН за первый месяц; тыс. т. с долей СП'] / (365 / 12) * 1000

        prepared_data['Уд.FCF с СП на 1 тн. (за 1 мес.)'] = prepared_data['FCF первый месяц c долей СП']/prepared_data['НДН за первый месяц; т./сут. с долей СП']
        return prepared_data


class SortedGfemData:

    def __init__(self,
                 prepared_data: GfemDataFrame,
                 ):
        self.prepared_data = prepared_data
        self.company_names = None

    def _data(self):
        return self.prepared_data.result()

    def result(self):
        dataframe = self._data()
        company_names = dataframe['ДО'].unique()
        self.company_names = company_names
        result_data = []
        result_jv = []
        result_data.append(dataframe.sort_values(by='Уд.FCF на 1 тн. (за 1 мес.)'))
        result_jv.append(dataframe.sort_values(by='Уд.FCF с СП на 1 тн. (за 1 мес.)'))
        for name in company_names:
            result = dataframe.loc[dataframe['ДО'] == name]
            result_data.append(result.sort_values(by='Уд.FCF на 1 тн. (за 1 мес.)'))
            result_jv.append(result.sort_values(by='Уд.FCF с СП на 1 тн. (за 1 мес.)'))

        return {'Без учета СП': result_data, 'C учетом СП': result_jv}


class RegressionScenarios:

    def __init__(self,
                 sorted_data: SortedGfemData):
        self.sorted_data = sorted_data
        self.company_names = None
        self.dataframe = []
    def _data(self):
        data = self.sorted_data.result()
        self.company_names = self.sorted_data.company_names

        return data

    def scenarios(self):
        data = self.data_for_regression()
        full_scenarios = {}
        jv_scenarios = {}
        full_scenarios['ГПН'] = self._prepare_scenario(data=data[0][0].to_numpy())
        jv_scenarios['ГПН'] = self._prepare_scenario(data=data[1][0].to_numpy())
        for i in range(len(self.company_names)):
            full_scenarios[self.company_names[i]] = self._prepare_scenario(data=data[0][i+1].to_numpy())
            jv_scenarios[self.company_names[i]] = self._prepare_scenario(data=data[1][i + 1].to_numpy())

        return [full_scenarios, jv_scenarios]

    def _prepare_scenario(self, data):
        data1 = np.copy(data)
        x_initial = data1.T[0]
        y_initial = data1.T[1]
        x = np.cumsum(x_initial)
        x = x[:, np.newaxis]
        y = np.cumsum(y_initial)
        X_train, X_test, Y_train, Y_test = train_test_split(x, y,
                                                            test_size=0.2,
                                                            random_state=1)
        poly = PolynomialFeatures(4)
        poly_model = make_pipeline(poly, LinearRegression())
        poly_model.fit(X_train, Y_train)

        return [poly_model, x.min(), x.max()]

    def data_for_regression(self):
        data = self._data()
        full_data = data['Без учета СП']
        self.dataframe.append(full_data[0])
        jv_data = data['C учетом СП']
        self.dataframe.append(jv_data[0])
        result_full = []
        result_jv = []
        for dataframe in full_data:
            result_full.append(dataframe[['НДН за первый месяц; т./сут.', 'FCF первый месяц']])

        for dataframe in jv_data:
            result_jv.append(dataframe[['НДН за первый месяц; т./сут. с долей СП', 'FCF первый месяц c долей СП']])

        return [result_full, result_jv]


class Application(Component):

    def __init__(self,
                 scenarios: RegressionScenarios,

                 ):

        self.scenarios = scenarios
        super().__init__()

        self.base_crude = False
        self.condence = False
        self.joint_venture = False
        self.label_width = 150

        self.state = StateManager({
                                    "File": pathlib.Path(""),
                                    })

        self.min_value_full = {}
        self.max_value_full = {}

        self.min_value_jv = {}
        self.max_value_jv = {}

        self.min_value = {}
        self.max_value = {}

        self.vostok_value = 0.0
        self.megion_value = 0.0
        self.messoyaha_value = 0.0
        self.nng_value = 0.0
        self.orenburg_value = 0.0
        self.hantos_value = 0.0
        self.yamal_value = 0.0

        self.do_value = [self.vostok_value,
                         self.megion_value,
                         self.messoyaha_value,
                         self.nng_value,
                         self.orenburg_value,
                         self.hantos_value,
                         self.yamal_value]

        self.sum_value = self.vostok_value + self.megion_value + self.messoyaha_value + self.nng_value + self.orenburg_value + self.hantos_value + self.yamal_value

        self.fcf_value_full = {}
        self.fcf_value_jv = {}
        self.fcf_full = 0
        self.fcf_jv = 0
        self.fcf_value = {}

        self.company_min = 0
        self.company_max = 0
        self.company_value = 0

        self.company_fcf = 0

        self.data = None

        self.company_names = []
        self.dataframe_list = None

    def initialization(self):
        data = self.scenarios.scenarios()
        self.data = data
        self.company_names = self.scenarios.company_names.copy()

        self.min_full = 0#data[0]['ГПН'][1]
        self.max_full = data[0]['ГПН'][2]
        self.fcf_full = data[0]['ГПН'][0].predict(np.array(self.min_full).reshape(-1, 1))

        self.min_jv = 0#data[1]['ГПН'][1]
        self.max_jv = data[1]['ГПН'][2]
        self.fcf_jv = data[0]['ГПН'][0].predict(np.array(self.min_jv).reshape(-1, 1))

        for name in self.company_names:
            self.min_value_full[name] = 0#data[0][name][1]
            self.max_value_full[name] = data[0][name][2]
            self.fcf_value_full[name] = np.array([0])#data[0][name][0].predict(np.array(self.min_value_full[name]).reshape(-1,1))
        for name in self.company_names:
            self.min_value_jv[name] = 0#data[1][name][1]
            self.max_value_jv[name] = data[1][name][2]
            self.fcf_value_jv[name] = np.array([0])#data[1][name][0].predict(np.array(self.min_value_jv[name]).reshape(-1,1))
        self._choose_scenario()
        self.dataframe = self.scenarios.dataframe
        print(self.dataframe_list[0].head())

    def _choose_scenario(self):
        self.joint_venture = not self.joint_venture
        if self.joint_venture:
            self.min_value = self.min_value_jv
            self.max_value = self.max_value_jv
            self.company_min = self.min_jv
            self.company_max = self.max_jv
            self.company_value = self.company_min
            self.fcf_value = self.fcf_value_jv

            self.vostok_value = self.min_value_jv[self.company_names[0]]
            self.megion_value = self.min_value_jv[self.company_names[1]]
            self.nng_value = self.min_value_jv[self.company_names[2]]
            self.hantos_value = self.min_value_jv[self.company_names[3]]
            self.orenburg_value = self.min_value_jv[self.company_names[4]]
            self.messoyaha_value = self.min_value_jv[self.company_names[5]]
            self.yamal_value = self.min_value_jv[self.company_names[6]]

        if not self.joint_venture:
            self.min_value = self.min_value_full
            self.max_value = self.max_value_full
            self.company_min = self.min_full
            self.company_max = self.max_full
            self.company_value = self.company_min

            self.fcf_value = self.fcf_value_full
            self.vostok_value = self.min_value_full[self.company_names[0]]
            self.megion_value = self.min_value_full[self.company_names[1]]
            self.nng_value = self.min_value_full[self.company_names[2]]
            self.hantos_value = self.min_value_full[self.company_names[3]]
            self.orenburg_value = self.min_value_full[self.company_names[4]]
            self.messoyaha_value = self.min_value_full[self.company_names[5]]
            self.yamal_value = self.min_value_full[self.company_names[6]]

    def plot(self, ax):
        x = np.linspace(0, self.company_max, 200)

        if self.joint_venture: j = 0
        else: j = 1
        y = self.data[j]['ГПН'][0].predict(x[:,np.newaxis])
        ax.plot(x, y)

    def _update_fcf(self):

        if self.joint_venture: j = 0
        else: j = 1
        self.company_fcf = self.data[j]['ГПН'][0].predict(np.array(self.company_value).reshape(-1, 1))
        if self.vostok_value == 0:
            self.fcf_value[self.company_names[0]] = np.array([0])
        else:
            self.fcf_value[self.company_names[0]] = self.data[j][self.company_names[0]][0].predict(np.array(self.vostok_value).reshape(-1, 1))
        if self.megion_value == 0:
            self.fcf_value[self.company_names[1]]= np.array([0])
        else:
            self.fcf_value[self.company_names[1]] = self.data[j][self.company_names[1]][0].predict(np.array(self.megion_value).reshape(-1, 1))
        self.fcf_value[self.company_names[2]] = self.data[j][self.company_names[2]][0].predict(np.array(self.messoyaha_value).reshape(-1, 1))
        self.fcf_value[self.company_names[3]] = self.data[j][self.company_names[3]][0].predict(np.array(self.nng_value).reshape(-1, 1))
        self.fcf_value[self.company_names[4]] = self.data[j][self.company_names[4]][0].predict(np.array(self.orenburg_value).reshape(-1, 1))
        self.fcf_value[self.company_names[5]] = self.data[j][self.company_names[5]][0].predict(np.array(self.hantos_value).reshape(-1, 1))
        self.fcf_value[self.company_names[6]] = self.data[j][self.company_names[6]][0].predict(np.array(self.yamal_value).reshape(-1, 1))

    def _find_solution(self):

        pass

    def render(self):
        self.sum_value = self.vostok_value + self.megion_value + self.messoyaha_value + self.nng_value + self.orenburg_value + self.hantos_value + self.yamal_value
        self.sum_fcf = sum(self.fcf_value.values())
        self._update_fcf()
        return Window(title='Просмотрщик сценариев')(View(layout="column", style={"margin": 15, "font-weight": 1})(View(layout="row")(
                                            View(layout="column")(
                                                CheckBox(text='Базовая добыча',),
                                                CheckBox(text='ГТМ'),
                                                CheckBox(text='Конденсат'),
                                                CheckBox(text='Учет доли СП', checked=self.joint_venture, on_change=lambda value: self._choose_scenario()),
                                                                ),
                                           # Image(src=r'C:\Users\User\Downloads\Desktop\image.JPG', style={"width": self.label_width*5,  "margin": 10}, scale_to_fit=False)
                                            plotting.Figure(lambda ax: self.plot(ax))),


                                    View(layout="row", )(
                                        Label('ГПН', style={"width": self.label_width, }, ),
                                        Slider(value=self.company_value, min_value=self.company_min,
                                               max_value=self.company_max, on_click=lambda value: self._find_solution(),
                                               on_change=lambda value: self.set_state(company_value=value)),
                                        Label(round(self.company_value, 1),
                                              style={"width": self.label_width / 2, "margin": 5, "align": "center"}),
                                        Label(self.company_fcf.round()[0],
                                              style={"width": self.label_width / 2, "margin": 5, "align": "center"})

            ),


                                        View(layout="row",)(
                                            Label(self.company_names[0], style={"width": self.label_width,  }, ),
                                            Slider(value=self.vostok_value, min_value=self.min_value[self.company_names[0]], max_value=self.max_value[self.company_names[0]], on_change=lambda value: self.set_state(vostok_value=value)),
                                            Label(round(self.vostok_value, 1), style={"width": self.label_width/2, "margin": 5, "align": "center"}),
                                            Label(self.fcf_value[self.company_names[0]].round()[0], style={"width": self.label_width / 2, "margin": 5, "align": "center"})


                                                            ),
                                        View(layout="row", )(
                                            Label(self.company_names[1], style={"width": self.label_width}),
                                            Slider(value=self.megion_value,min_value=self.min_value[self.company_names[1]], max_value=self.max_value[self.company_names[1]], on_change=lambda value: self.set_state(megion_value=value)),
                                            Label(round(self.megion_value, 1), style={"width": self.label_width / 2, "margin": 5,
                                                                         "align": "center"}),
                                            Label(self.fcf_value[self.company_names[1]].round()[0],
                                                  style={"width": self.label_width / 2, "margin": 5, "align": "center"})


                                        ),
                                        View(layout="row")(
                                            Label(self.company_names[2], style={"width": self.label_width}),
                                            Slider(value=self.messoyaha_value, min_value=self.min_value[self.company_names[2]],
                                                   max_value=self.max_value[self.company_names[5]],
                                                   on_change=lambda value: self.set_state(messoyaha_value=value)),
                                            Label(round(self.messoyaha_value, 1), style={"width": self.label_width / 2, "margin": 5,
                                                                                         "align": "center"}),
                                            Label(self.fcf_value[self.company_names[2]].round()[0],
                                                  style={"width": self.label_width / 2, "margin": 5, "align": "center"})
                                        ),

                                        View(layout="row", )(
                                            Label(self.company_names[3], style={"width": self.label_width}),
                                            Slider(value=self.nng_value, min_value=self.min_value[self.company_names[3]], max_value=self.max_value[self.company_names[3]], on_change=lambda value: self.set_state(nng_value=value)),
                                            Label(round(self.nng_value, 1), style={"width": self.label_width / 2, "margin": 5,
                                                                         "align": "center"}),
                                            Label(self.fcf_value[self.company_names[3]].round()[0],
                                                  style={"width": self.label_width / 2, "margin": 5, "align": "center"})
                                        ),

                                        View(layout="row")(
                                            Label(self.company_names[4], style={"width": self.label_width}),
                                            Slider(self.orenburg_value, min_value=self.min_value[self.company_names[4]], max_value=self.max_value[self.company_names[4]], on_change=lambda value: self.set_state(orenburg_value=value)),
                                            Label(round(self.orenburg_value, 1), style={"width": self.label_width / 2, "margin": 5,
                                                                         "align": "center"}),
                                            Label(self.fcf_value[self.company_names[4]].round()[0],
                                                  style={"width": self.label_width / 2, "margin": 5, "align": "center"})
                                        ),
                                        View(layout="row")(
                                            Label(self.company_names[5], style={"width": self.label_width}),
                                            Slider(value=self.hantos_value, min_value=self.min_value[self.company_names[5]],
                                                   max_value=self.max_value[self.company_names[5]],
                                                   on_change=lambda value: self.set_state(hantos_value=value)),
                                            Label(round(self.hantos_value, 1), style={"width": self.label_width / 2, "margin": 5,
                                                                                      "align": "center"}),
                                            Label(self.fcf_value[self.company_names[5]].round()[0],
                                                  style={"width": self.label_width / 2, "margin": 5, "align": "center"})
                                        ),

                                        View(layout="row")(
                                            Label(self.company_names[6], style={"width": self.label_width}),
                                            Slider(value=self.yamal_value, min_value=self.min_value[self.company_names[6]], max_value=self.max_value[self.company_names[6]],
                                                   on_change=lambda value: self.set_state(yamal_value=value)),
                                            Label(round(self.yamal_value, 1), style={"width": self.label_width / 2, "margin": 5,
                                                                              "align": "center"}),
                                            Label(self.fcf_value[self.company_names[6]].round()[0],
                                                  style={"width": self.label_width / 2, "margin": 5, "align": "center"})
                                        ),
                                        View(layout="row")(
                                            Label('Сумма', style={"width": self.label_width}),

                                            Label(round(self.sum_value, 1), style={"width": self.label_width / 2, "margin": 5,
                                                                                     "align": "right"}),
                                            Label(self.sum_fcf.round()[0],
                                                  style={"width": self.label_width / 2, "margin": 5, "align": "right"})
                                        ),

                                        View(layout="row")(
                                            Label("Загрузить объекты в Excel", style={"width": self.label_width}),
                                            Form(self.state,),

            ),

        )
    )


class SolutionBalancer:

    def __init__(self,
                 dataframe_list: list,
                 crude_value: float):



class CompanyDict:
    def __init__(self,
                 path
                 ):
        self.path = Path(path)
        self.joint_venture_crude_part = {}
        self.joint_venture_fcf_part = {}

    def load(self, scenario_program: bool = False):
        if not scenario_program:
            DATA = self.path / 'Балансировка компенсационных мероприятий для НРФ.xlsm'
        else:
            DATA = self.path / 'Словарь ДО.xlsx'
        df = pd.read_excel(DATA, sheet_name='Словарь ДО')


        df1 = df['Список ДО']
        df2 = df['Месторождение']
        if scenario_program:
            dataframe = pd.read_excel(DATA, sheet_name='Доли СП')
            df3 = dataframe['ДО']
            df4 = dataframe['По добыче']
            df5 = dataframe['По FCF']

            self.joint_venture_crude_part = dict(zip(list(df3), list(df4)))
            self.joint_venture_fcf_part = dict(zip(list(df3), list(df5)))
        company_dict = dict(zip(list(df2), list(df1)))
        return company_dict
