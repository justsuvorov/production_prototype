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
        ActivityLoaderDB(data=data, source_path=self.path).load_data()

    def load_black_list_to_db(self, data: pd.DataFrame):
        BlackListLoaderDB(data=data, source_path=self.path).load_data()

    def load_full_data_to_db(self, data: pd.DataFrame):
        AROFullLoaderDB(data=data, source_path=self.path).load_data()

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
