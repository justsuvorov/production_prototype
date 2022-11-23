from ObjectStatus import ObjectStatus


class ObjectInfo:
    def __init__(self,
                 linkList: dict,
                 objectStatus: ObjectStatus,
                 ):
        self.linkList = linkList
        self.objectStatus = objectStatus

    def build(self):
        pass
