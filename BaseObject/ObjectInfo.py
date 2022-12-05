from BaseObject.ObjectStatus import ObjectStatus


class ObjectInfo:
    def __init__(self,
                 object_type: list,
                 link: list = None,
                 ):
        self.object_type = object_type

    def build(self):
        pass