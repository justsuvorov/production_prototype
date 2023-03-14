from Program.BaseObject.Sensor import Sensor
from Program.BaseObject.Object import Object


class ObjectRecord:
    """
    Класс-контейнер сведений об объекте доменной модели
    Позволяет формировать иерархию при создании доменной модели

    inputs:
    name : имя объекта
    type_of_object: тип объекта (Well, Cluster, Pad ... Plast ...)
    Object: указатель (ссылка) на объект
    links: список ссылок на другие объекты иерархии
    status: Sensor. Сигнализатор ошибок внутри объекта
    """
    def __init__(self,
                 name: str,
                 type_of_object: str,
                 object: Object,
                 links: list,
                 status: Sensor
                 ) -> None:
        self.name = name
        self.type_of_object = type_of_object
        self.object = object
        self.links = links
        self.status = status.status

    @classmethod
    def create(cls, object: Object, type_of_object: str):
        return cls(name=str(object.name)+str(object.object_info.link_list['Field']),
                   type_of_object=type_of_object,
                   object=object,
                   links=object.link,
                   status=object.sensor
                   )
