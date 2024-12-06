from abc import ABC, abstractmethod

class ITask3(ABC):
    """
    This class can act as an interface to work with various implementations
    to include the functionality of the factorization into your project.
    """
    def __init__(self):
        self.p = None

    @abstractmethod
    async def print_results(self, num: int, filename: str) -> None:
        pass

    @abstractmethod
    async def factorization(self, num: int) -> None:
        pass
