import abc
from typing import Any


class serializable(abc.ABC):

    @abc.abstractmethod
    def serialize(self) -> bytes:
        pass

    @abc.abstractmethod
    def toDict(self) -> dict[str, Any]:
        pass


class serializeAsJsonFile(abc.ABC):
    pass
