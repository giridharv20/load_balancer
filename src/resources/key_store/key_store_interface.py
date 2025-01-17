from abc import abstractmethod, ABCMeta


class KeyStoreInterface(metaclass=ABCMeta):

    # abstractmethod enforces the implementers to implement the
    # abstract methods
    @abstractmethod
    def set(self, key: str, value: str):
        ...

    @abstractmethod
    def get(self, key: str) -> str:
        ...