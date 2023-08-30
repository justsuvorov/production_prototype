import datetime

import pandas as pd
import numpy as np
from pathlib import Path
from Program.ObjectBuilders.sql_speaking_objects import *
from Program.AROMonitoring.connector import *


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

    def __activity_data_id(self):
        return self.__activity_objects_id.id_list()

    def __db_form_id(self):
        return self.__db.black_list_from_db()[['id', 'Тип объекта', 'Скважина', 'Куст', 'Объект подготовки', 'Месторождение',	'ДО']]

    def __check_id(self)->bool:
        error = False
        activity_id = self.__activity_objects_id.id_list()
        db_id = self.__db.black_list_from_db()['id'].tolist()
        for id in activity_id:
            if id in db_id:
                pass
            else:
                error = True
                try:
                    print('id = ', id , 'в форме мероприятий отсутсвует в базе')
                    obj = self.__activity_data.loc[self.__activity_data['id'] == id]
                    data = self.__db.black_list_from_db()
                    new_id = data.loc[data['Скважина'] == obj['Скважина'] and data['Месторождение'] == obj['Месторождение']]['id']
                    print('Заменить ', id, 'на ', new_id)
                except:
                    pass
        return error


