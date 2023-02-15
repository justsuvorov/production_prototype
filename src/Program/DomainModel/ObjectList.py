from Program.BaseObject.Sensor import Sensor
from Program.BaseObject.Object import Object


class ObjectRecord:
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
        return cls(name=object.name,
                   type_of_object=type_of_object,
                   object=object,
                   links=object.link,
                   status=object.sensor
                   )
