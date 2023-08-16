from datetime import datetime

import pandas as pd
import numpy as np
from pathlib import Path
from Program.ObjectBuilders.sql_speaking_objects import *
from Program.AROMonitoring.connector import *

class AroMonitoring:

    def __init__(self,
                 file_path: str,
                 filter: dict = {'Company': 'All', 'Field': 'All'},
                 date: datetime = datetime.today().replace(day=1)
                 ):
        self.add_data_from_excel = True
        self.file_path = file_path
        self.filter = filter
        self.date = date

        self.__monitoring_base = MonitoringSQLSpeakingObject(path=self.file_path)
        self.__gfem_base = GfemSQLSpeakingObject(path=self.file_path,
                                                 add_data_from_excel=self.add_data_from_excel)
        self.__mor_db_base = SQLMorDBSpeakingObject(path=self.file_path)

    def _data(self) -> pd.DataFrame:
        gfem_data = self.__gfem_base.data()
        return gfem_data

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
            raise print('Aro Monitoring||Ошибка выбора ДО-Месторождения. Фильтры сброшены')
        prepared_data = prepared_data.drop(columns=['GAP'])

        return prepared_data

    def __prepare_df(self, df: pd.DataFrame, new_data: bool = False):
        df['Скважина'].replace(to_replace=[None], value='-', inplace=True)
        df['Куст'].replace(to_replace=[None], value='-', inplace=True)
        df['Объект подготовки'].replace(to_replace=[None], value='-', inplace=True)
        df['temp_id'] = df.loc[:,'Скважина'] + df.loc[:, 'Куст'] + df.loc[:, 'Объект подготовки'] + df.loc[:,'Месторождение']
       # df['Статус по МЭР'] = ''

        if new_data:

            df['Дата внесения'] = self.date
    #       df['Статус по рентабельности'] = 'Нерентабельная'
        return df

    def __prepare_new_data_for_export(self, df: pd.DataFrame):
        pd.set_option('mode.chained_assignment', None)
        df['Статус по МЭР'] = ''
        df['monitoring_id'] = 'New_id'
        pd.reset_option("mode.chained_assignment")
        return df

    def __prepare_old_data_for_export(self, df: pd.DataFrame, db_black_list_data: pd.DataFrame):
        df = df.sort_values(by='temp_id')

        db_black_list_data = db_black_list_data.loc[db_black_list_data['temp_id'].isin(df['temp_id'])]
        db_black_list_data = db_black_list_data.sort_values(by='temp_id')
        df['Статус по МЭР'] = db_black_list_data['Статус по МЭР'].values
        df['monitoring_id'] = db_black_list_data['id'].values
        df['old_id_aro'] = db_black_list_data['id_aro'].values
        df = df.sort_values(by='monitoring_id')
        return df

    def black_list(self, excel_export: bool = False):
        if self.__check_base(db=self.__gfem_base):
            self.__monitoring_base.check_connection()
            self.__gfem_base.check_connection()
            db_black_list_data = self.__prepare_df(self.__monitoring_base.black_list_from_db()) #черный список из базы
            data = self.__prepare_df(df=self._recalculate_indicators(), new_data=True)  #результаты АРО
            black_list_delete = db_black_list_data.loc[~db_black_list_data['temp_id'].isin(data['temp_id'])]
            black_list_new = self.__prepare_new_data_for_export(
                df=data.loc[~data['temp_id'].isin(db_black_list_data['temp_id'])]
                                                                )  #новые объекты
            black_list_old = self.__prepare_old_data_for_export(
                db_black_list_data=db_black_list_data,
                df=data.loc[data['temp_id'].isin(db_black_list_data['temp_id'])]
                                                                )
            black_list = pd.concat([black_list_old, black_list_new], ignore_index=False)
            self.__export_black_list(data=black_list, excel_export=excel_export)
            self.__monitoring_base.check_connection()
            self.__check_status_and_transfer_to_archive(data=black_list_delete)
            self.__monitoring_base.connection.close()

            self.__gfem_base.connection.close()
        else:
            print('ARO Monitoring || База ГФЭМ содержит неактуальыне даынне. Мэппинг непроизведен')

    def __check_status_and_transfer_to_archive(self, data: pd.DataFrame):
        df_gfem = self.__prepare_df(df=self.__gfem_base.names())
        if self.filter['Company'] != 'All':
            df_gfem = df_gfem.loc[df_gfem['ДО'] == self.filter['Company']]
            data = data.loc[data['ДО'] == self.filter['Company']]
        gfem_data = data.loc[data['temp_id'].isin(df_gfem['temp_id'])]
        gfem_data['Статус по рентабельности'] = 'Выведен в рентабельную зону'
        stopped_data = data.loc[~data['temp_id'].isin(df_gfem['temp_id'])]
        stopped_data['Статус по рентабельности'] = 'Остановлен'
        self.__monitoring_base.delete_from_base(gfem_id=gfem_data['id'],
                                                stopped_id=stopped_data['id']
                                                )

    def __export_black_list(self, data: pd.DataFrame, excel_export: bool):
        if excel_export:
            BlackListLoaderExcel(data=data, source_path=self.file_path).load_data()
        self.__monitoring_base.load_black_list_to_db(data=data, gfem_base=self.__gfem_base)
        print('Loading completed')

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
        prepared_data['Дата направления мероприятия'] = pd.to_datetime('today', format='%d/%m/%Y')
        prepared_data = prepared_data.drop(columns=['Дата внесения', 'id_aro'])
        prepared_data.to_excel(self.file_path + '\Форма для ДО.xlsx')
        print('Company ford is exported')

    def load_company_form_to_db(self, data: pd.DataFrame):

        db_activity_data = self.__monitoring_base.activity_data_from_db()
        filtered_data = data[['id', 'ID Мероприятия (автозаполнение)', 'Комментарии к мероприятию',
                                'Дата выполнения мероприятия (План)', 'Дата выполнения мероприятия (Факт)',
                                'Отвественный (название должности)', 'Статус. В работе/остановлена',
                                'Наличие отказа. Да/Нет', 'Дата направления мероприятия']]

        filtered_data.columns = ['object_id', 'activity_id', 'activity_comment', 'date_planning', 'date_fact',
                                'responsible_person', 'obj_status', 'failure', 'date_creation']
     #   filtered_data = filtered_data.fillna(' ')
   #     filtered_data['date_creation'] = filtered_data['date_creation'].astype('str')
      # a = db_activity_data.loc[~db_activity_data['object_id'].isin(filtered_data['object_id'])]
      # export_data = pd.concat([a, filtered_data])
        export_data = filtered_data
        self.__monitoring_base.load_activity_data_to_db(data=export_data)
        print('Company form is loaded')

    def map_status_from_mor_db(self):
        if self.__check_base(db=self.__mor_db_base):
            pd.set_option('mode.chained_assignment', None)

            df_active = self.__mor_db_base.last_month_active_data()
            print('ARO Monitoring || МЭР. Действующие скважины ',df_active.shape[0])
            df_inactive = self.__mor_db_base.last_month_inactive_data()
            print('ARO Monitoring || МЭР. Остановленные скважины ', df_inactive.shape[0])
            black_list = self.__monitoring_base.black_list_from_db()
            black_list['temp_id'] = black_list['Скважина'] + black_list['Месторождение']
            df_inactive['temp_id'] = df_inactive['well_number'] + df_inactive['field']
            df_active['temp_id'] = df_active['well_number'] + df_active['field']
            black_list_on = black_list.loc[black_list['temp_id'].isin(df_active['temp_id'])]
            black_list_on['Статус по МЭР'] = 'Раб.'
            black_list_off = black_list.loc[black_list['temp_id'].isin(df_inactive['temp_id'])]
            black_list_off['Статус по МЭР'] = 'Ост.'
            black_list = pd.concat([black_list_on, black_list_off])
            export_list = black_list.drop(columns='temp_id')
            self.__monitoring_base.write_mer_status(id=export_list['id'], status_mer=export_list['Статус по МЭР'])
        #    self.__monitoring_base.load_black_list_to_db(data=export_list)
         #   self.__monitoring_base.delete_inactive()

            pd.reset_option("mode.chained_assignment")
            print('ARO Monitoring || МЭР. Мэппинг произведен')
        else:
            print('ARO Monitoring || МЭР. База МЭР содержит неактуальные данные. Мэппинг не произведен')

    def __check_base(self, db: SQLSpeakingObject) -> bool:
        if isinstance(db, GfemSQLSpeakingObject):
            self.data = GfemDBConnection(db=db).check_last_date()
            return GfemDBConnection(db=db).check_status()
        elif isinstance(db, SQLMorDBSpeakingObject):
            return MorDBConnection(db=db).check_status()
        else:
            return False

    def upload_data_for_dashboard(self):

       self.__monitoring_base.check_connection()
       archive = sqlite3.connect(self.file_path + '\monitoring_archive.db')

       black_list = self.__monitoring_base.black_list_from_db()
       black_list_archive = pd.read_sql_query('SELECT * FROM monitoring_obj_archive', archive)
       series_names = ['id', 'id_aro', 'Тип объекта', 'Скважина', 'Куст', 'ДНС', 'Месторождение', 'ДО',
                       'Дата внесения', 'Статус', 'Статус по МЭР', 'Дата попадания в архив']
       series_names2 = ['id', 'id_aro', 'Тип объекта', 'Скважина', 'Куст', 'ДНС', 'Месторождение', 'ДО',
                       'Дата внесения', 'Статус', 'Статус по МЭР']
       black_list_archive = black_list_archive.set_axis(series_names, axis=1, )
       black_list = black_list.set_axis(series_names2, axis=1, )
       black_list = pd.concat([black_list,black_list_archive])

       economics_and_crude = self.__monitoring_base.full_data_black_list_from_db()
       economics_and_crude_archive = pd.read_sql_query('SELECT * FROM monitoring_ecm_prod_full_arc', archive)
       economics_and_crude = pd.concat([economics_and_crude, economics_and_crude_archive])
       series_names_2 = [
                       'id', 'дата АРО', 'NPV',
                       'FCF, тыс. руб.', 'Добыча нефти, тыс. т.','Добыча нефти за весь период; тыс. т',
                       'НДЖ за весь период; тыс. т', 'FCF за весь период; тыс. руб.',
                       'НДН до ГЭП; тыс. т', 'НДЖ до ГЭП; тыс. т', 'FCF до ГЭП; тыс. руб.',
                       'Период расчета; мес.', 'НДН за скользящий год; тыс. т', 'НДЖ за скользящий год; тыс. т',
                       'FCF за скользящий год; тыс. руб.',
                       'Добыча жидкости за первый месяц, тыс.т.']
       economics_and_crude = economics_and_crude.set_axis(series_names_2, axis=1)
       economics_and_crude['Добыча нефти, тыс. т.'] = economics_and_crude['Добыча нефти, тыс. т.'].round(5)
       economics_and_crude['Добыча жидкости за первый месяц, тыс.т.'] = economics_and_crude['Добыча жидкости за первый месяц, тыс.т.'].round(5)

       activity_list = self.__monitoring_base.activity_data_from_db()
       activity_list['Статус'] = np.where(activity_list['date_fact'], 'Выполнено', 'Не выполнено')
       activity_list['Статус'] = np.where(activity_list['activity_id'] == 3, 'Выполнено', 'Не выполнено')
       activity_list_archive = pd.read_sql_query('SELECT * FROM activity_unprofit_archive', archive)
       activity_list_archive['Статус'] = 'Выполнено'
       activity_list = pd.concat([activity_list, activity_list_archive])

       activity_list['date_creation'] = pd.to_datetime(activity_list['date_creation'], format='mixed', errors='ignore')
       activity_list['date_planning'] = pd.to_datetime(activity_list['date_planning'], format='mixed',errors='ignore')
       activity_list['date_fact'] = pd.to_datetime(activity_list['date_fact'],  format='mixed', errors='coerce')


       predict_list = pd.read_sql_query('SELECT * FROM monitoring_ecm_prod_monthly', sqlite3.connect(self.file_path+'\monitoring.db'))
       predict_list = predict_list.loc[:, ['id_object', 'timeindex_dataframe', 'dobycha_nefti', 'dobycha_gaza', 'neft_tovarnaya', 'opex', 'dobycha_zhidkosti', 'fcf']]

       predict_list_names = ['id_object', 'timeindex_dataframe', 'Добыча нефти, тыс.т.', 'Добыча газа', 'Нефть товарная', 'OPEX', 'Добыча жидкости, тыс.т.', 'FCF, тыс. руб.']
       predict_list  = predict_list.set_axis(predict_list_names, axis=1, )

       activities = {'activity_id': [1, 2, 3, 4 , 5, 6, 7], 'activity': ['Остановлена с ГТМ',
'Остановлена без ГТМ',
'Отбор проб',
'Мероприятия по ППД',
'Инфраструктурные ограничения',
'ВНР, неустановившийся режим',
'Прочие ограничения'
]}

       with pd.ExcelWriter(self.file_path+'\qlik_results.xlsx') as writer:
           black_list.to_excel(writer, sheet_name='BlackList', index=False)
           economics_and_crude.to_excel(writer, sheet_name='Экономика и добыча', index=False)
           activity_list.to_excel(writer, sheet_name='Мероприятия', index=False)
           predict_list.to_excel(writer, sheet_name='Прогноз', index=False)
           pd.DataFrame(data=activities).to_excel(writer, sheet_name='Список мероприятий', index=False)

       print('Данные выгружены')



