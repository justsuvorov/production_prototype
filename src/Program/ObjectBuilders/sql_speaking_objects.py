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


class MonitoringSQLSpeakingObject(SQLSpeakingObject):
    def __init__(self,
                 path: str, ):
        self.path = path
        self.db_name = self.path + '\monitoring.db'
        super().__init__(db_name=self.db_name)

        self.__monitoring_base_parser = MonitoringBaseParser(data_path=self.db_name)
        self.__monitoring_full_parser = MonitoringFullParser(data_path=self.db_name)
        self.__monitoring_activity_parser = MonitoringActivityParser(data_path=self.db_name)

    def black_list_from_db(self):
        return self.__monitoring_base_parser.data()

    def full_data_black_list_from_db(self):
        return self.__monitoring_full_parser.data()

    def activity_data_from_db(self):
        return self.__monitoring_activity_parser.data()

    def load_activity_data_to_db(self, data):
     #   ActivityLoaderDB(data=data, source_path=self.path).load_data()
        self.cursor.execute()
        self.connection.commit()

    def load_black_list_to_db(self, data: pd.DataFrame, gfem_base: SQLSpeakingObject):
     #   BlackListLoaderDB(data=data, source_path=self.path).load_data()
        new_data = data.loc[data['monitoring_id'] == 'New_id']
        new_data['Дата внесения'] = new_data['Дата внесения'].dt.strftime('%d/%m/%Y').astype(str)
        export_new_data = new_data.loc[:, ['id', 'Тип объекта', 'Скважина', 'Куст', 'Объект подготовки',
                                           'Месторождение', 'ДО', 'Дата внесения', 'Статус по рентабельности',
                                           'Статус по МЭР']]
        print(export_new_data.values.tolist())
        query = '''
            INSERT INTO monitoring_unprofit_obj (id_aro, obj_type, well_name, well_group_name, preparation_obj_name,
            field_name, company_name, date_creation, status, status_mer  ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.cursor.executemany(query, export_new_data.values.tolist())
        self.load_full_data_to_db(data=new_data, gfem_base=gfem_base)
        self.connection.commit()

#        old_data = data.loc[data['monitoring_id'] != 'New_id'].to


    #    self.connection.commit()

    def load_full_data_to_db(self, data: pd.DataFrame, gfem_base: GfemSQLSpeakingObject):
      #  AROFullLoaderDB(data=data, source_path=self.path).load_data()
        gfem_base.
        query1 = '''
                    SELECT id_parent, timeindex_dataframe, dobycha_nefti FROM 
        '''
        self.cursor.execute('')

        export_new_data = data.loc[:, ['id',
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
                                         'FCF за скользящий год; тыс. руб.',]]
        query = '''
            INSERT INTO monitoring_ecm_prod_full (object_id
                                                    date_aro
                                                    npv_max
                                                    fcf_first_month
                                                    oil_production_first_month
                                                    oil_production_full
                                                    fluid_extraction_full
                                                    fcf_full
                                                    oil_production_gap
                                                    fluid_extraction_gap
                                                    fcf_gap
                                                    calculation_horizon
                                                    oil_production_year
                                                    fluid_extraction_year
                                                    fcf_year
                                                ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, )
        '''
        self.cursor.executemany(query, export_new_data.values.tolist())
        self.connection.commit()

    def insert(self):
        if self.df is None:
            print('No data to insert')
        else:
            for raw in self.df.iterrows():
                self.cursor.execute('''INSERT OR IGNORE''')

    def delete_inactive(self):
        self.cursor.execute('''DELETE FROM monitoring_ecm_prod_full WHERE object_id NOT IN (SELECT id FROM monitoring_unprofit_obj)''')
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

        df = pd.read_sql_query('''SELECT * FROM mor_info WHERE id in (SELECT id_parent FROM mor_prod WHERE (date IN (SELECT max(date) FROM mor_prod)) AND (end_month_status = 'раб.' OR end_month_status = 'пьез' ))''', self.connection)


        return df

    def last_month_inactive_data(self):
        self.connection = sqlite3.connect(self.db_name)
        #    df = pd.read_sql_query('SELECT * FROM mor_prod WHERE date IN (SELECT max(date) FROM mor_prod)', self.connection)
        df = pd.read_sql_query(
            '''SELECT * FROM mor_info WHERE id in (SELECT id_parent FROM mor_prod WHERE (date IN (SELECT max(date) FROM mor_prod)) AND (end_month_status = 'ост.' OR  end_month_status = 'лик'))''',
            self.connection)
        # AND end_month_status = РАБ.

        return df
