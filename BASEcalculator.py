"""Базовые классы."""
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, Optional, Type
from uuid import uuid4

#from loguru import logger
from pydantic import BaseModel


#logger = logger.opt(depth=1)
#logger.bind(name='base')


class BASECalculator(ABC):
    """Базовый калькулятор."""
    INPUT_SCHEMA: Optional[Type[BaseModel]] = BaseModel
    OUTPUT_SCHEMA: Optional[Type[BaseModel]] = BaseModel

    def __init__(self, data: INPUT_SCHEMA, **kwargs: Any) -> None:
        self.__id = str(uuid4())
        self.input = deepcopy(data)
        self.output = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Выход из менеджера контекста."""

    @property
    def id(self) -> str:
        """Уникальный идентификатор расчета."""
        return self.__id

    @abstractmethod
    def _calculate(self, *args):
        """Тело расчета."""

    def log(self, msg: str) -> None:
        #"""Логирование расчета."""
        #logger.debug(f'{self.__class__.__name__}#{self.id}: {msg}')
        print({msg})

    def run(self, *args):
        """Запуск калькулятора."""
        self.log('Расчет запущен')
        result = self._calculate()

        self.log('Данные рассчитаны')
        self.output = self.OUTPUT_SCHEMA.parse_obj(result.dict())

        self.log('Данные проверены')
        return self

    def save(self, **kwargs):
        """Отправка рассчитанных данных во внешний интерфейс."""

    @classmethod
    def load(cls, *args):
        """Загрузка входящих данных из источника и возвращение экземпляра калькулятора.

        Источник может быть нескольких видов:
            - путь к файлу;
            - «сырой» JSON;
            - dict;
            - готовая Pydantic-модель.
        """
