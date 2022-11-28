from BaseObject.ObjectStatus import ObjectStatus


class ObjectInfo:
    def __init__(self,

                 objectStatus: ObjectStatus,
                 link: list = None,
                 ):
        self.link = link
        self.objectStatus = objectStatus

    def build(self):
        pass
