

class ObjectInfo:
    """
      Класс информациия о базовом объекте добычи нефти

      Inputs:
      object_type: тип объекта (для скважины: нефтяная, нагнетающая и т.п.)
      object_activity: массив 0/1 аквтиности объектов.
      link_list: словарь название объектов иерархии. По нему строятся актвивные ссылки на другие объекты иерархии

      """
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


class ObjectActivity:
    def __init__(self,
                 last_status: bool) -> None:
        self.last_status = last_status

    def switch_status(self):
        self._check_status()
        self.last_status = not self.last_status

    def _check_status(self):
        if self.last_status == None:
            self.last_status = True

