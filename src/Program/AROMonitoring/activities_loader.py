import datetime
import sqlite3

import pandas as pd
import numpy as np
from pathlib import Path
from Program.ObjectBuilders.sql_speaking_objects import *
from Program.AROMonitoring.connector import *
from Program.Production.Logger import Logger


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


class ObjectsIDMapper:
    def __init__(self,
                 db: MonitoringSQLSpeakingObject,
                 activity_data: pd.DataFrame,
                 activity_objects_id: ActivityObjectId):
        self.__db = db
        self.__activity_objects_id = activity_objects_id
        self.__activity_data = activity_data
        self.__archive = self.__db.path + '\monitoring_archive.db'
        self.__logger = Logger(filename='activities_loader.txt')

    def __activity_data_id(self):
        return self.__activity_objects_id.id_list()

    def __db_form_id(self):

        return self.__db.black_list_from_db()[['id', 'Тип объекта', 'Скважина', 'Куст', 'Объект подготовки', 'Месторождение',	'ДО']]

    def __dataframe(self) -> pd.DataFrame:
        data = self.__db.black_list_from_db()[['id', 'Скважина', 'Месторождение']]
        wells = data[['id', 'Скважина', 'Месторождение']]
        con = sqlite3.connect(self.__archive)
        arch_data = pd.read_sql('SELECT * FROM monitoring_obj_archive', con=con)
        arch_wells = arch_data[['id', 'well_name', 'field_name']]
        data = pd.concat([wells, arch_wells.set_axis(['id', 'Скважина', 'Месторождение'], axis=1)])
        return data

    def check_id(self)->bool:
        activity_data = self.__activity_data.fillna('No data')
        status = True
        activity_id = self.__activity_objects_id.id_list()
        db_id_1 = self.__db.black_list_from_db()['id'].tolist()

        try:
            res2 = sqlite3.connect(self.__archive).execute('SELECT id FROM monitoring_obj_archive')
            id_tuple = res2.fetchall()
            id_arch = [elt[0] for elt in id_tuple]
        except sqlite3.DatabaseError:
            raise self.__logger.log('Отсутсует архивная база или она повреждена')
        db_id = db_id_1+id_arch
        data = self.__dataframe()
        for id in activity_id:

            if id in db_id:
                if activity_data.loc[activity_data['id']==id].shape[0] > 1:
                    self.__logger.log('Дублирование Id = ' + str(id))
                    status = False
                well_temp = activity_data.loc[activity_data['id']==id]['Скважина'].astype(dtype='str').iloc[0]
                field_temp = activity_data.loc[activity_data['id'] == id]['Месторождение'].astype(dtype='str').iloc[0]
                w1 = data.loc[data['id']==id]['Скважина'].iloc[0]
                f1 = data.loc[data['id']==id]['Месторождение'].iloc[0]
                if well_temp != w1 or field_temp != f1:
                    status = False
                    d1 = data.loc[data['Скважина'] == well_temp]
                    d2 = d1.loc[d1['Месторождение'] == field_temp]
                    self.__logger.log('Неправильный id в форме мероприятий. Заменить '+  str( id) + ' на'+  str(d2['id'].iloc[0] ))
            else:
                status = False
                self.__logger.log('id = '+  str(id) + ' в форме мероприятий отсутсвует в базе')
                obj = activity_data.loc[activity_data['id'] == id]

                new_id = data.loc[data['Месторождение'].isin(obj['Месторождение'])]
                new_id = new_id.loc[new_id['Скважина'].isin(obj['Скважина'].astype(dtype='str'))]
                try:
                    self.__logger.log('Заменить ' +  str(id) + ' на '+ str(new_id['id'].iloc[0]))
                except IndexError:
                    self.__logger.log('Скважины '+  str( activity_data.loc[activity_data['id'] == 'No data'][['Скважина', 'Месторождение']])+   ' нет в базе мониторинга или отсутсвует id')

        return status
