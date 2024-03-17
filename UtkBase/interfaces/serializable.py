import abc


class serializable(abc.ABC):

    @abc.abstractmethod
    def serialize(self) -> bytes:
        pass
