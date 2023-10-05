import datetime
import sqlite3

import pandas as pd
import numpy as np
from pathlib import Path
from Program.ObjectBuilders.sql_speaking_objects import *
from Program.AROMonitoring.connector import *
from Program.Production.Logger import Logger


class DbObjectsId:
    def __init__(self,
                 db: MonitoringSQLSpeakingObject,
                 ):
        self.__db = db
        self.__archive = self.__db.path + '\monitoring_archive.db'

    def id_list(self)->list:

        try:
            db_id_1 = self.__db.black_list_from_db()['id'].tolist()
            res2 = sqlite3.connect(self.__archive).execute('SELECT id FROM monitoring_obj_archive')
            id_tuple = res2.fetchall()
            id_arch = [elt[0] for elt in id_tuple]
        except sqlite3.DatabaseError:
            raise print('Отсутсует архивная база или она повреждена')
        return  db_id_1+id_arch


class ActivityObjectId:
    def __init__(self,
                 data: pd.DataFrame,
                 ):
        self.__activity_data = data

    def id_list(self)->list:
        try:
            id = self.__activity_data['id'].tolist()
        except KeyError:
            id = ['Key_error']
            print('Отсутсвуют id обхектов в форме')
        finally:
            return id


class DBWellData:
    def __init__(self,
                 db: MonitoringSQLSpeakingObject,
                 ):

        self.__db = db
        self.__db_objects_id = DbObjectsId(db=self.__db)
        self.__archive = self.__db.path + '\monitoring_archive.db'
        self.__data = self.__db.black_list_from_db()[['id', 'Скважина', 'Месторождение']]

    def well_name(self, id) -> str:
        data = self.data()
        return data.loc[data['id'] == id]['Скважина'].iloc[0]

    def field_name(self, id) -> str:
        data = self.data()
        return data.loc[data['id'] == id]['Месторождение'].iloc[0]

    def data(self) -> pd.DataFrame:
        data = self.__data
        wells = data[['id', 'Скважина', 'Месторождение']]
        con = sqlite3.connect(self.__archive)
        arch_data = pd.read_sql('SELECT * FROM monitoring_obj_archive', con=con)
        arch_wells = arch_data[['id', 'well_name', 'field_name']]
        data = pd.concat([wells, arch_wells.set_axis(['id', 'Скважина', 'Месторождение'], axis=1)])
        return data

    def id_list(self):
        return self.__db_objects_id.id_list()


class ActivityFormWellData:
    def __init__(self,
                 data: pd.DataFrame
                 ):
        self.__data = data.fillna('No data')
        self.__activity_id = ActivityObjectId(data=self.__data)
        self.__logger = Logger(filename='Activity_data.txt')
        self.__status = True

    def well_name(self, id) -> str:
        error = self.__check_duplication(id=id)
        return str(self.__data.loc[self.__data['id'] == id]['Скважина'].iloc[0])

    def field_name(self, id) -> str:
        return str(self.__data.loc[self.__data['id'] == id]['Месторождение'].iloc[0])

    def full_name(self, id) -> pd.DataFrame:
        return self.__data.loc[self.__data['id'] == id][['id', 'Скважина', 'Месторождение']]

    def __check_duplication(self,id):

        if self.full_name(id=id).shape[0] > 1:
            print(self.__logger.log('Дублирование Id = ' + str(id)))
            self.__status = False
            return True
        else:
            return False

    def status(self):
        return self.__status

    def activity_data(self):
        return self.__data

    def id_list(self):
        return self.__activity_id.id_list()


class WellMapper:
    def __init__(self,
                 activity_well: ActivityFormWellData,
                 db_well: DBWellData,
                 ):
        self.__activity_well = activity_well
        self.__db_well = db_well

    def new_id(self, old_id):
        if old_id == 'No data':
            new_id = self.__search_for_id()
        else:
            db_data = self.__db_well.data()
            obj = self.__activity_well.full_name(id=old_id)
            new_id = db_data.loc[db_data['Месторождение'].isin(obj['Месторождение'])]
            new_id = new_id.loc[new_id['Скважина'].isin(obj['Скважина'].astype(dtype='str'))]
        try:

            return new_id['id'].iloc[0]
        except IndexError:
            return 'Скважины нет в базе'

    def __search_for_id(self):
        df = self.__activity_well.activity_data()
        empty_id_df = df.loc[df['id']=='No data']
        db_data = self.__db_well.data()
        new_id = db_data.loc[db_data['Месторождение'].isin(empty_id_df['Месторождение'])]
        new_id = new_id.loc[new_id['Скважина'].isin(empty_id_df['Скважина'].astype(dtype='str'))]

        return new_id


class ObjectsIDMapper:
    def __init__(self,
                 activity_data: ActivityFormWellData,
                 db_data: DBWellData,
                 ):
        self.__activity_data = activity_data
        self.__db_data = db_data
        self.__logger = Logger(filename='activities_loader.txt')

    def check_id(self)->bool:
        status = True
        activity_id = self.__activity_data.id_list()
        db_id = self.__db_data.id_list()

        for id in activity_id:
            if id in db_id:
                activity_well_name = self.__activity_data.well_name(id=id)
                activity_field_name = self.__activity_data.field_name(id=id)
                db_well_name = self.__db_data.well_name(id=id)
                db_field_name = self.__db_data.field_name(id=id)
                status = self.__activity_data.status()
                if (activity_well_name != db_well_name) or (activity_field_name != db_field_name):
                    status = False
                    self.__logger.log('Неправильный id в форме мероприятий. Проверить '+  str(id) + activity_well_name + activity_field_name)
            else:
                status = False
                self.__logger.log('id = '+  str(id) + ' в форме мероприятий отсутсвует в базе')
                new_id = WellMapper(activity_well=self.__activity_data, db_well=self.__db_data).new_id(old_id=id)
                try:
                    self.__logger.log('Заменить ' +  str(id) + ' на '+ str(new_id))
                except IndexError:
                    self.__logger.log('Скважины '+  self.__activity_data.well_name(id=id) +
                                      self.__activity_data.field_name(id=id) +
                                      ' нет в базе мониторинга или отсутсвует id')
        return status
