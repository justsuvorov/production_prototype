class Indicators:

    """
    Класс контейнер показателей и сценария

    Inputs:
    description: имя сценария
    indicators: показатели объекта с описанием сценария. Показатели - словари

    """

    def __init__(self,
                 description: str = None,
                 indicators: dict = None):
        self.indicators = indicators
        self.description = description


