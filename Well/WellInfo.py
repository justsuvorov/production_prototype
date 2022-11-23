from Well.ObjectStatus import ObjectStatus
from Well.PlastInfo import PlastInfo

class ObjectInfo:
    def __init__(self,
                 linkList: dict = None,
                 objectStatus: ObjectStatus = None,
                 ):
        self.linkList = linkList
        self.objectStatus = objectStatus


    def build(self):
        pass

class WellInfo:
    def __init__(self,
                 wellType,
                 plastInfo: PlastInfo
                 ):
        self.wellType = wellType
        self.plastInfo = plastInfo