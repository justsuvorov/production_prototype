from BaseObject.Sensor import Sensor

class ObjectRecord:
    def __init__(self,
                 name: str,
                 type_of_object: str,
                 object,
                 links: list,
                 status: Sensor
                 ):
        self.name = name
        self.type_of_object = type_of_object
        self.object = object
        self.links = links
        self.status = status.status