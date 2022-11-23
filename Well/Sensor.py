class Sensor:
    def __init__(self,
                 error: bool = False):
        if error != False:
            self.status = 'HasError'
        else:
            self.status = 'HasData'
