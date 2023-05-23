import pandas as pd
import numpy as np
from pathlib import Path
from Program.ObjectBuilders.sql_speaking_objects import  *


class AroMonitoring:

    def __init__(self,
                 file_path: str,
                 filter: dict = {'Company': 'All', 'Field': 'All'},
                 ):
        self.add_data_from_excel = True
        self.file_path = file_path
        self.filter = filter
        self.black_list_names = ['id', 'Тип объекта', 'Скважина', 'Куст', 'Объект подготовки','Месторождение', 'ДО', 'Дата внесения', 'Статус по рентабельности']
        self.__monitoring_base = MonitoringSQLSpeakingObject(path=self.file_path)
        self.__gfem_base = GfemSQLSpeakingObject(path=self.file_path,
                                                 add_data_from_excel=self.add_data_from_excel)
        self.__mor_db_base = SQLMorDBSpeakingObject(path=self.file_path)

    def _data(self) -> pd.DataFrame:
        return self.__gfem_base.data()

    def _recalculate_indicators(self):
        data = self._data()
        print('Aro Monitoring||Gfem data is read')
        prepared_data = data
        prepared_data.loc[prepared_data['Тип объекта'].str[0] == 'W', 'Тип объекта'] = 'Скважина'
        prepared_data.loc[prepared_data['Тип объекта'] == 'GROUP_ECONOMIC', 'Тип объекта'] = 'Куст'
        prepared_data.loc[prepared_data['Тип объекта'] == 'PREPARATION_OBJECT_ECONOMIC', 'Тип объекта'] = 'Объект подготовки'
        prepared_data = prepared_data.loc[~prepared_data['Тип объекта'].isin(['GROUP_OPEX','PREPARATION_OBJECT_OPEX'])]
        try:
            if self.filter['Company'] != 'All':
                prepared_data = prepared_data.loc[prepared_data['ДО'] == self.filter['Company']]
                print('Выбрано ДО: ', self.filter['Company'])
            if self.filter['Field'] != 'All':
                prepared_data = prepared_data.loc[prepared_data['Месторождение'] == self.filter['Field']]
                print('Выбрано месторождение: ', self.filter['Field'])
        except:
            print('Aro Monitoring||Ошибка выбора ДО-Месторождения. Фильтры сброшены')
        prepared_data = prepared_data.drop(columns=['GAP'])

        return prepared_data

    def __prepare_df(self, df: pd.DataFrame, new_data: bool = False):
        df['Скважина'].replace(to_replace=[None], value='-', inplace=True)
        df['Куст'].replace(to_replace=[None], value='-', inplace=True)
        df['Объект подготовки'].replace(to_replace=[None], value='-', inplace=True)
        df['temp_id'] = df.loc[:, 'Скважина'] + df.loc[:,'Скважина'] + df.loc[:, 'Объект подготовки'] + df.loc[:,'Месторождение']
        if new_data:
            df['Дата внесения'] = pd.to_datetime("today")
    #        df['Статус по рентабельности'] = 'Нерентабельная'
        return df

    def black_list(self, excel_export: bool = False):
        db_black_list_data = self.__monitoring_base.black_list_from_db()
        db_black_list_data = self.__prepare_df(df=db_black_list_data)

        db_export_list = self.__monitoring_base.full_data_black_list_from_db()


        data = self._recalculate_indicators()
        data = self.__prepare_df(df=data, new_data=True)

        black_list = data.loc[:, :]
        black_list['temp_id'] = data['Скважина'] + data['Скважина'] + data['Объект подготовки'] + data['Месторождение']
        black_list = black_list.loc[~black_list['temp_id'].isin(db_black_list_data['temp_id'])]



        export_list = black_list.drop(columns=self.black_list_names[1:-2])
        black_list = black_list.loc[:, self.black_list_names]
        black_list = pd.concat([db_black_list_data, black_list])
        export_list = pd.concat([db_export_list, export_list])

        self.__export_black_list(data=black_list, excel_export=excel_export)
        self.__export_full_list(data=export_list, excel_export=excel_export)

    def aro_full_info_black_list(self, path: str=None, excel_export: bool = False):
        if path is None:
            path = self.file_path
        data = self._recalculate_indicators()

        export_list = data.drop(columns=self.black_list_names[1:-2])
        export_list = export_list.drop(columns='Лицензионный участок')
        self.__export_full_list(data=export_list, excel_export=excel_export)

    def __export_black_list(self, data: pd.DataFrame, excel_export: bool):
        if excel_export:
            BlackListLoaderExcel(data=data, source_path=self.file_path).load_data()
        self.__monitoring_base.load_black_list_to_db(data=data)

    def __export_full_list(self, data: pd.DataFrame, excel_export: bool):
        if excel_export:
            data.to_excel(self.file_path + '/Full_list.xlsx')
        data =data.drop(
            columns=['Лицензионный участок', 'temp_id', 'Дата внесения', 'Статус по рентабельности',])
        self.__monitoring_base.load_full_data_to_db(data=data)
        self.__gfem_base.transfer_month_table()

    def export_company_form(self):
        prepared_data = self.__monitoring_base.black_list_from_db()
        if self.filter['Company'] != 'All':
            prepared_data = prepared_data.loc[prepared_data['ДО'] == self.filter['Company']]
        if self.filter['Field'] != 'All':
            prepared_data = prepared_data.loc[prepared_data['Месторождение'] == self.filter['Field']]
        prepared_data['Мероприятие'] = ''
        prepared_data['Комментарии к мероприятию'] = ''
        prepared_data['Дата выполнения мероприятия (План)'] = ''
        prepared_data['Дата выполнения мероприятия (Факт)'] = ''
        prepared_data['Отвественный(название должности)'] = ''
        prepared_data['Статус. В работе/остановлена'] = ''
        prepared_data['Наличие отказа. Да/Нет'] = ''
        prepared_data.drop(columns=['Дата внесения', 'id'])
        prepared_data.to_excel(self.file_path + '\Форма для ДО.xlsx')

    def load_company_form_to_db(self, data: pd.DataFrame):

        db_activity_data = self.__monitoring_base.activity_data_from_db()
        print(db_activity_data)
       # db_activity_data
       # data = data.loc[~data['id'].isin(db_activity_data['object_id'].isin(data['id']))]

        filtered_data = data[['id', 'Мероприятие', 'Комментарии к мероприятию',
                                'Дата выполнения мероприятия (План)', 'Дата выполнения мероприятия (Факт)',
                                'Отвественный (название должности)', 'Статус. В работе/остановлена',
                                'Наличие отказа. Да/Нет', ]]

        filtered_data.columns = ['object_id', 'activity_id', 'activity_comment', 'date_planning', 'date_fact',
                               'responsible_person', 'obj_status', 'date_creation']

        a = db_activity_data.loc[~db_activity_data['object_id'].isin(filtered_data['object_id'])]

        export_data = pd.concat([a, filtered_data])
        self.__monitoring_base.load_activity_data_to_db(data=export_data)

    def map_status_from_mor_db(self):
        df_active = self.__mor_db_base.last_month_active_data()
        print('ARO Monitoring || МЭР. Действующие скважины ',df_active.shape[0])
        df_inactive = self.__mor_db_base.last_month_inactive_data()
        print('ARO Monitoring || МЭР. Остановленные скважины ', df_inactive.shape[0])

        black_list = self.__monitoring_base.black_list_from_db()
        black_list['temp_id'] = black_list['Скважина'] + black_list['Месторождение']
        df_inactive['temp_id'] = df_inactive['well_number'] + df_inactive['field']
        black_list = black_list.loc[~black_list['temp_id'].isin(df_inactive['temp_id'])]
        export_list = black_list.drop(columns='temp_id')
        self.__monitoring_base.load_black_list_to_db(data=export_list)
        self.__monitoring_base.delete_inactive()

        print('ARO Monitoring || МЭР. Мэппинг произведен')








