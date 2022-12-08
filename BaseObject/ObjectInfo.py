from BaseObject.ObjectStatus import ObjectStatus


class ObjectInfo:
    def __init__(self,
                 object_type: list,

                 object_activity,
                 link_list: dict = None
                 ):
        self.object_type = object_type
        self.object_activity = object_activity
        self.link_list = link_list


    def build(self):
        pass