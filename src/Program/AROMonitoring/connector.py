import abc
from abc import ABC
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from Program.ObjectBuilders.sql_speaking_objects import *


class DBConnection():
    def __init__(self,
                 db: SQLSpeakingObject):
        self.db = db

    def check_status(self) -> bool:
        a = self.__check_data()
        b = True #self.__check_last_date()
        if a and b:
            return True
        else:
            return True

  #  @abc.abstractmethod
    def __check_data(self) -> bool:
        pass

#    @abc.abstractmethod
    def check_last_date(self):
        date = pd.read_sql('SELECT MIN (timeindex_dataframe) FROM arf_prod_ecm', self.db.connection)
        s = str(date['MIN (timeindex_dataframe)'].iloc[0])
        s1 = datetime.datetime.strptime(s, '%Y-%m-%d')
        s2 = s1 - relativedelta(months=1)
        s2 = s2.replace(day=20)
        print('Дата АРО:', s2)
        return s2

    def check_connection(self) -> bool:
        if self.db.connection is not None:
            return True
        else:
            return False


class GfemDBConnection(DBConnection):
    def __init__(self,
                 db: SQLSpeakingObject,
                 ):
        self.db = db
        super().__init__(db=self.db)

    def __check_data(self) -> bool:
        return True

    def __check_last_date(self) -> bool:
        return True


class MorDBConnection(DBConnection):
    def __init__(self,
                 db: SQLSpeakingObject,
                 ):
        self.db = db
        super().__init__(db=self.db)

    def __check_data(self) -> bool:
        return True

    def __check_last_date(self) -> bool:
        return True
