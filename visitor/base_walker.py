from abc import ABC, abstractmethod


class BaseSbomParser(ABC):
    @abstractmethod
    def walk(self, component: str) -> str:
        """Search for the component in tree of product and returns its cpe"""
        raise NotImplementedError
