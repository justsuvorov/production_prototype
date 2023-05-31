import pandas as pd
import sqlite3
from Program.ObjectBuilders.Parser import *
from Program.ObjectBuilders.loaders import *


class SQLSpeakingObject:
    def __init__(self,
                 db_name: str,
                 ):
        self.db_name = db_name
        self.cursor = None
        self.connection = None

        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print('Connected to ', db_name)
        #  connection.close()
        except:
            print('Unable to connect to db', self.db_name)

    def check_connection(self):
        try:
            self.connection.cursor()
        except:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print('Connected to ', self.db_name)


class GfemSQLSpeakingObject(SQLSpeakingObject):
    def __init__(self,
                 path: str,
                 add_data_from_excel: bool = False
                 ):
        self.path = path
        self.db_name = self.path + '\gfem_results.db'
        super().__init__(db_name=self.db_name)
        self.__gfem_base_parser = GfemDataBaseParser(data_path=self.db_name,
                                                     add_data_from_excel=add_data_from_excel,
                                                     file_path=self.path)

    def data(self):
        return self.__gfem_base_parser.data()

    def transfer_month_table(self):
        self.__gfem_base_parser.transfer_month_table(path=self.path)

    def transfer_data_month_table(self, id_parent: pd.DataFrame, mdb: str, ):
        if id_parent.shape[0]:
            self.cursor.execute('ATTACH "' + mdb + '" AS m')
            for id in id_parent:
                self.cursor.execute('''
                INSERT OR IGNORE INTO m.monitoring_ecm_prod_monthly SELECT * FROM arf_prod_ecm WHERE id_parent = (?)              
                ''', (id,))
            self.connection.commit()

    def get_crude_first_month(self):
        data = pd.read_sql_query(
            '''SELECT id_parent, timeindex_dataframe, dobycha_nefti FROM arf_prod_ecm GROUP BY id_parent HAVING timeindex_dataframe = MIN(timeindex_dataframe)''',
            con=self.connection)
        return data

    def new_month_table(self, id: pd.DataFrame):

        data = pd.read_sql_query(
            'SELECT * FROM arf_prod_ecm WHERE id_parent in "' + id.values.tolist() + '"',
            con=self.connection)
        return data


class MonitoringSQLSpeakingObject(SQLSpeakingObject):
    def __init__(self,
                 path: str, ):
        self.path = path
        self.db_name = self.path + '\monitoring.db'
        super().__init__(db_name=self.db_name)

        self.__monitoring_base_parser = MonitoringBaseParser(data_path=self.db_name)
        self.__monitoring_full_parser = MonitoringFullParser(data_path=self.db_name)
        self.__monitoring_activity_parser = MonitoringActivityParser(data_path=self.db_name)

    def load_black_list_to_db(self, data: pd.DataFrame, gfem_base: GfemSQLSpeakingObject):
        #   BlackListLoaderDB(data=data, source_path=self.path).load_data()
        new_data = data.loc[data['monitoring_id'] == 'New_id']  # новый скважины в черный список
        self.__load_new_data_to_db(new_data=new_data, gfem_base=gfem_base)
        old_data = data.loc[data['monitoring_id'] != 'New_id']
        self.__update_old_data_to_db(old_data=old_data, gfem_base=gfem_base)
        print('Operations is completed')

    def black_list_from_db(self):
        return self.__monitoring_base_parser.data()

    def full_data_black_list_from_db(self):
        return self.__monitoring_full_parser.data()

    def activity_data_from_db(self):
        return self.__monitoring_activity_parser.data()

    def load_activity_data_to_db(self, data):
        sqlite3.connect(self.db_name)
        ActivityLoaderDB(data=data, source_path=self.path).load_data()

    def __load_new_data_to_db(self, new_data: pd.DataFrame, gfem_base: GfemSQLSpeakingObject):
        if new_data.shape[0] > 0:
            new_data['Дата внесения'] = new_data['Дата внесения'].dt.strftime('%d/%m/%Y').astype(str)
            export_new_data = new_data.loc[:, ['id', 'Тип объекта', 'Скважина', 'Куст', 'Объект подготовки',
                                               'Месторождение', 'ДО', 'Дата внесения', 'Статус по рентабельности',
                                               'Статус по МЭР']]
            query = '''
                        INSERT INTO monitoring_unprofit_obj (id_aro, obj_type, well_name, well_group_name, preparation_obj_name,
                        field_name, company_name, date_creation, status, status_mer  ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''

            try:
                self.cursor.executemany(query, export_new_data.values.tolist())
                self.connection.commit()
                new_data_id = self.__prepare_new_data_id(new_data=new_data, gfem_base=gfem_base)

                export_new_data = new_data_id.loc[:, ['id_main',
                                                      'date',
                                                      'NPV_MAX',
                                                      'FCF первый месяц:',
                                                      'НДН за первый месяц',
                                                      'НДН за весь период; тыс. т',
                                                      'НДЖ за весь период; тыс. т',
                                                      'FCF за весь период; тыс. руб.',
                                                      'НДН до ГЭП; тыс. т',
                                                      'НДЖ до ГЭП; тыс. т',
                                                      'FCF до ГЭП; тыс. руб.',
                                                      'Период расчета; мес.',
                                                      'НДН за скользящий год; тыс. т',
                                                      'НДЖ за скользящий год; тыс. т',
                                                      'FCF за скользящий год; тыс. руб.', ]]
                query = '''
                           INSERT INTO monitoring_ecm_prod_full (object_id,
                                                                   date_aro,
                                                                   npv_max,
                                                                   fcf_first_month,
                                                                   oil_production_first_month,
                                                                   oil_production_full,
                                                                   fluid_extraction_full,
                                                                   fcf_full,
                                                                   oil_production_gap,
                                                                   fluid_extraction_gap,
                                                                   fcf_gap,
                                                                   calculation_horizon,
                                                                   oil_production_year,
                                                                   fluid_extraction_year,
                                                                   fcf_year
                                                               ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       '''
                self.cursor.executemany(query, export_new_data.values.tolist())
                self.connection.commit()
                gfem_base.transfer_data_month_table(id_parent=new_data_id['id'], mdb=self.db_name)
                self.connection.commit()
                print('Добавлены новые объекты в черный список: ', new_data.shape[0])

            except sqlite3.Error:
               print('Ошибка добавления новых объектов')
        else:
            print('Нет новых объектов')

    def __update_old_data_to_db(self, old_data: pd.DataFrame, gfem_base: GfemSQLSpeakingObject):
        if old_data.shape[0] > 0:
            self.__update_id_aro_in_black_list(new_id_aro=old_data['id'],
                                               id=old_data['monitoring_id'],
                                               status=old_data['Статус по рентабельности'])
            data_for_full_table = self.__prepare_old_data_for_full_table(old_data=old_data,
                                                                         gfem_base=gfem_base)
            self.__insert_new_data_to_full_table(data=data_for_full_table)
            self.__delete_old_month_data(id_aro_old=old_data['old_id_aro'])
            self.cursor.close()
            try:
                gfem_base.transfer_data_month_table(id_parent=old_data['id'], mdb=self.db_name)
            except:
                print('Экспорт таблицы помесячного прогноза не выполнен, повторите снова')
            self.check_connection()
            print('Обновлено данных для скважин: ', old_data.shape[0])

    def __insert_new_data_to_full_table(self, data: pd.DataFrame, ):
        query = '''
                INSERT OR IGNORE INTO monitoring_ecm_prod_full (object_id,
                                                                   date_aro,
                                                                   npv_max,
                                                                   fcf_first_month,
                                                                   oil_production_first_month,
                                                                   oil_production_full,
                                                                   fluid_extraction_full,
                                                                   fcf_full,
                                                                   oil_production_gap,
                                                                   fluid_extraction_gap,
                                                                   fcf_gap,
                                                                   calculation_horizon,
                                                                   oil_production_year,
                                                                   fluid_extraction_year,
                                                                   fcf_year
                                                               ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
        try:
            self.cursor.executemany(query, data.values.tolist())
            self.connection.commit()
        except sqlite3.Error:
            print('Ошибка обновления старых объектов. Rollback')
            self.connection.rollback()

    def __update_id_aro_in_black_list(self, new_id_aro: pd.DataFrame, id: pd.DataFrame, status: pd.DataFrame):
        new_id_aro = new_id_aro.values.tolist()
        status = status.values.tolist()
        query = '''
            UPDATE monitoring_unprofit_obj SET id_aro = (?), status = (?) WHERE id = (?)
    
                    '''
        j = 0
        self.check_connection()
        for i in id:
            self.cursor.execute(query, (new_id_aro[j], status[j], i,))
            j += 1
        self.connection.commit()

    def __prepare_old_data_for_full_table(self, old_data: pd.DataFrame, gfem_base: GfemSQLSpeakingObject):
        add_data = gfem_base.get_crude_first_month()
        add_data.columns = ['id', 'date', 'НДН за первый месяц']
        add_data = add_data.loc[add_data['id'].isin(old_data['id'])]
        add_data = add_data.set_index('id')
        old_data = old_data.set_index('id')
        old_data = old_data.join(add_data)
        old_data = old_data.reset_index()
        prepared_data = old_data.loc[:, ['monitoring_id',
                                         'date',
                                         'NPV_MAX',
                                         'FCF первый месяц:',
                                         'НДН за первый месяц',
                                         'НДН за весь период; тыс. т',
                                         'НДЖ за весь период; тыс. т',
                                         'FCF за весь период; тыс. руб.',
                                         'НДН до ГЭП; тыс. т',
                                         'НДЖ до ГЭП; тыс. т',
                                         'FCF до ГЭП; тыс. руб.',
                                         'Период расчета; мес.',
                                         'НДН за скользящий год; тыс. т',
                                         'НДЖ за скользящий год; тыс. т',
                                         'FCF за скользящий год; тыс. руб.', ]]
        return prepared_data

    def __prepare_new_data_id(self, new_data: pd.DataFrame, gfem_base: GfemSQLSpeakingObject):
        black_list = self.black_list_from_db().sort_values(by='id_aro')
        add_data = gfem_base.get_crude_first_month()
        add_data.columns = ['id', 'date', 'НДН за первый месяц']
        add_data = add_data.loc[add_data['id'].isin(new_data['id'])]
        add_data = add_data.set_index('id')
        new_data = new_data.set_index('id')
        new_data = new_data.join(add_data)
        new_data = new_data.reset_index()
        new_data = new_data.sort_values(by='id')
        black_list = black_list.loc[:, 'id'].reset_index()
        new_data['id_main'] = black_list.loc[:, 'id']
        return new_data

    def load_full_data_to_db(self, new_data: pd.DataFrame, old_data: pd.DataFrame, gfem_base: GfemSQLSpeakingObject):
        #  AROFullLoaderDB(data=data, source_path=self.path).load_data()
        new_data = self.__prepare_new_data_id(new_data=new_data, gfem_base=gfem_base)
        #      old_data =
        export_new_data = new_data.loc[:, ['id_main',
                                           'date',
                                           'NPV_MAX',
                                           'FCF первый месяц:',
                                           'НДН за первый месяц',
                                           'НДН за весь период; тыс. т',
                                           'НДЖ за весь период; тыс. т',
                                           'FCF за весь период; тыс. руб.',
                                           'НДН до ГЭП; тыс. т',
                                           'НДЖ до ГЭП; тыс. т',
                                           'FCF до ГЭП; тыс. руб.',
                                           'Период расчета; мес.',
                                           'НДН за скользящий год; тыс. т',
                                           'НДЖ за скользящий год; тыс. т',
                                           'FCF за скользящий год; тыс. руб.', ]]
        query = '''
            INSERT INTO monitoring_ecm_prod_full (object_id,
                                                    date_aro,
                                                    npv_max,
                                                    fcf_first_month,
                                                    oil_production_first_month,
                                                    oil_production_full,
                                                    fluid_extraction_full,
                                                    fcf_full,
                                                    oil_production_gap,
                                                    fluid_extraction_gap,
                                                    fcf_gap,
                                                    calculation_horizon,
                                                    oil_production_year,
                                                    fluid_extraction_year,
                                                    fcf_year
                                                ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        self.cursor.executemany(query, export_new_data.values.tolist())

    #    self.transfer_month_table(data=black_list['id_aro'], gfem_base=gfem_base)

    def __delete_old_month_data(self, id_aro_old: pd.DataFrame):
        id_aro_old = id_aro_old.values.tolist()
        query = '''
                   DELETE FROM monitoring_ecm_prod_monthly WHERE id_object = (?)
                '''
        for id in id_aro_old:
            self.connection.execute(query, (id,))
        self.connection.commit()

    def write_mer_status(self, id: pd.DataFrame, status_mer: pd.DataFrame):
        id_ = id.values.tolist()
        status_mer = status_mer.values.tolist()
        query = '''
                    UPDATE monitoring_unprofit_obj SET status_mer = (?) WHERE id = (?)

                            '''
        j = 0

        self.check_connection()
        for i in id_:
            self.cursor.execute(query, (status_mer[j], i,))
            j += 1
        self.connection.commit()

    def insert(self):
        if self.df is None:
            print('No data to insert')
        else:
            for raw in self.df.iterrows():
                self.cursor.execute('''INSERT OR IGNORE''')

    def delete_inactive(self):
        self.cursor.execute(
            '''DELETE FROM monitoring_ecm_prod_full WHERE object_id NOT IN (SELECT id FROM monitoring_unprofit_obj)''')
        self.cursor.execute(
            '''DELETE FROM monitoring_ecm_prod_monthly WHERE object_id NOT IN (SELECT id FROM monitoring_unprofit_obj)''')
        self.connection.commit()


class SQLMorDBSpeakingObject(SQLSpeakingObject):
    def __init__(self,
                 path: str,
                 ):
        self.path = path
        self.db_name = self.path + '\mor_db.db'
        super().__init__(db_name=self.db_name)

    def last_month_active_data(self):
        self.connection = sqlite3.connect(self.db_name)

        df = pd.read_sql_query(
            '''SELECT * FROM mor_info WHERE id in (SELECT id_parent FROM mor_prod WHERE (date IN (SELECT max(date) FROM mor_prod)) AND (end_month_status = 'раб.' OR end_month_status = 'пьез' ))''',
            self.connection)

        return df

    def last_month_inactive_data(self):
        self.connection = sqlite3.connect(self.db_name)
        #    df = pd.read_sql_query('SELECT * FROM mor_prod WHERE date IN (SELECT max(date) FROM mor_prod)', self.connection)
        df = pd.read_sql_query(
            '''SELECT * FROM mor_info WHERE id in (SELECT id_parent FROM mor_prod WHERE (date IN (SELECT max(date) FROM mor_prod)) AND (end_month_status = 'ост.' OR  end_month_status = 'лик'))''',
            self.connection)
        # AND end_month_status = РАБ.

        return df