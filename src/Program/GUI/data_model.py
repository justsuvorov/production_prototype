from abc import ABC

class DataModel(ABC):
    def __init__(self):
        pass


class ModelProxy(DataModel):
    def __init__(self,
             modelA: DataModel,
             modelB: DataModel,
             ):
        self.__modelA = modelA
        self.__modelB = modelB
        self.__model = modelA
        self.__modelIndex = 0

    def __getattr__(self, name):
        return getattr(self.__model, name)

    def change_model(self):
        if self.__modelIndex == 0:
            self.__modelIndex = 1
            self.__model = self.__modelB
        else:
            self.__modelIndex = 0
            self.__model = self.__modelA



