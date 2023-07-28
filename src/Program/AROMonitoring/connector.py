import abc
from abc import ABC
from Program.ObjectBuilders.sql_speaking_objects import *


class DBConnection():
    def __init__(self,
                 db: SQLSpeakingObject):
        self.db = db

    def check_status(self) -> bool:
        a = self.__check_data()
        b = self.__check_last_date()
        if a and b:
            return True
        else:
            return True

  #  @abc.abstractmethod
    def __check_data(self) -> bool:
        pass

#    @abc.abstractmethod
    def __check_last_date(self) -> bool:
        pass

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
