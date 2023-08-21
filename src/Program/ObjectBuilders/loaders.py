import pandas as pd
import sqlite3
from abc import ABC



class Loader(ABC):
    def __init__(self,
                 data: pd.DataFrame,
                 source_path: str,
                 ):
        self.data = data
        self.source_path = source_path

    def load_data(self):
        pass


class BlackListLoaderExcel(Loader):
    def __init__(self,
                 data: pd.DataFrame,
                 source_path: str,
                 ):
        super().__init__(data=data,
                         source_path=source_path)

    def load_data(self):
        self.data.to_excel(self.source_path+'\Black_list.xlsx')
        print('Результаты записаны в Excel')


class BlackListLoaderDB(Loader):
    def __init__(self,
                 data: pd.DataFrame,
                 source_path: str,
                 ):
        super().__init__(data=data,
                         source_path=source_path)
        self.initial_names = ['id', 'obj_type', 'well_name', 'well_group_name', 'preparation_obj_name',
                              'field_name', 'company_name', 'date_creation', 'status']

    def load_data(self):

        engine = sqlite3.connect(self.source_path+'\monitoring.db')
        self.data.columns = self.initial_names
        self.data.to_sql('monitoring_unprofit_obj', con=engine, if_exists='replace', index=False)
        print('BlackListLoaderDB||Результаты записаны в Базу данных')


class AROFullLoaderDB(Loader):
    def __init__(self,
                 data: pd.DataFrame,
                 source_path: str,
                 ):
        super().__init__(data=data,
                         source_path=source_path)
        self.initial_names = ['object_id',
                                'npv_max',
                                'fcf_first_month',
                             #   'oil_production_first_month',
                                'oil_production_full',
                                'fluid_extraction_full',
                                'fcf_full',
                                'oil_production_gap',
                                'fluid_extraction_gap',
                                'fcf_gap',
                                'calculation_horizon',
                                'oil_production_year',
                                'fluid_extraction_year',
                                'fcf_year',
                              ]

    def load_data(self):

        self.data.columns = self.initial_names
        engine = sqlite3.connect(self.source_path+'\monitoring.db')
     #   for row in self.data.iterrows():

        self.data.to_sql('monitoring_ecm_prod_full', con=engine, if_exists='replace', index=False)
        print('AROFullLoaderDB||Результаты записаны в Базу данных')


class ActivityLoaderDB(Loader):
    def __init__(self,
                 data: pd.DataFrame,
                 source_path: str,
                 ):
        super().__init__(data=data,
                         source_path=source_path)

    def load_data(self):
        self.data = self.data.fillna(value='')
        self.data['date_planning'] = self.data['date_planning'].fillna(value='')
        self.data['date_planning'] = pd.to_datetime(self.data['date_planning']).astype('str')
        self.data['date_fact'] = self.data['date_fact'].fillna(value='')
        self.data['date_fact'] = pd.to_datetime(self.data['date_fact']).astype('str')
        self.data['date_creation'] = pd.to_datetime(self.data['date_creation']).astype('str')
        self.data['date_creation'] = pd.to_datetime(self.data['date_creation'], format='%Y-%m-%d')


        engine = sqlite3.connect(self.source_path+'\monitoring.db')
        archive = sqlite3.connect(self.source_path+'\monitoring_archive.db')
        data_to_insert = self.data.values.tolist()
        error = False

        for string in data_to_insert:
            id = string[0]
            res = engine.execute('SELECT id FROM monitoring_unprofit_obj')
            res2 = archive.execute('SELECT id FROM monitoring_obj_archive')
            a = res.fetchall()
            b = res2.fetchall()
            a2 =  [item for item in a if item[0] == id]
            b2 = [item for item in b if item[0] == id]
       #     (object_id, activity_id, activity_comment,
       #      date_planning, date_fact, responsible_person, obj_status, failure, date_creation)
            query_insert = '''INSERT OR IGNORE INTO activity_unprofit  VALUES (?,?,?,?,?,?,?,?,?)'''
            query_update = '''UPDATE activity_unprofit SET  activity_id = (?), activity_comment = (?),
            date_planning = (?), date_fact = (?), responsible_person = (?), obj_status =  (?), failure = (?) WHERE object_id = (?) AND date_creation = (?)'''
            query_insert_arch = '''INSERT OR IGNORE INTO activity_unprofit_archive  VALUES (?,?,?,?,?,?,?,?,?)'''
            query_update_arch = '''UPDATE activity_unprofit_archive SET activity_id = (?), activity_comment = (?),
                       date_planning = (?), date_fact = (?), responsible_person = (?), obj_status =  (?), failure = (?) WHERE object_id = (?) AND date_creation = (?)'''
            string[8] = str(string[8])
            if a2:
                engine.execute(query_insert, string)
                engine.execute(query_update, (string[1], string[2], string[3], string[4], string[5], string[6], string[7], string[0], string[8],))
            elif b2:
                archive.execute(query_insert_arch, string)
                archive.execute(query_update_arch, (string[1], string[2], string[3], string[4], string[5], string[6], string[7], string[0], string[8],))
            else:
                print('Не совпадает id =', id)
                error = True

     #   self.data.to_sql('activity_unprofit', con=engine, if_exists='append', index=False)
     #    engine.cursor()
        if not error:
            engine.commit()
            archive.commit()
            print('ActivityLoaderDB||Результаты записаны в Базу данных')
        else:
            print('ActivityLoaderDB||Ошибка формата формы мероприятий')

class AROMonthTableLoaderDB(Loader):

    def __init__(self,
                 data: pd.DataFrame,
                 source_path: str,
                 ):
        super().__init__(data=data,
                         source_path=source_path)
