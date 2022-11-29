from BaseObject.Sensor import Sensor


class ObjectRecord:
    def __init__(self,
                 name: str,
                 type_of_object: str,
                 object,
                 links: list,
                 status: Sensor
                 ) -> None:
        self.name = name
        self.type_of_object = type_of_object
        self.object = object
        self.links = links
        self.status = status.status

    @classmethod
    def create(cls, object, type_of_object: str, links: list = None):
        return cls(name=object.name,
                   type_of_object=type_of_object,
                   object=object,
                   links=links,
                   status=object.sensor
                   )