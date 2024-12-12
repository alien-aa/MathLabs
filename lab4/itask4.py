from abc import ABC, abstractmethod

class ITask4(ABC):
    """
    This class can act as an interface to work with various implementations
    to include the functionality of the finding a discrete logarithm into your project.
    """
    def __init__(self):
        self.x = None

    @abstractmethod
    async def print_results(self,
                            a: int, b: int, p: int, q: int,
                            filename: str) -> None:
        pass

    @abstractmethod
    async def discrete_logarithm(self, a: int, b: int, p: int, q: int) -> None:
        pass
# 1.	ро-методом Полларда.
# 2.	Методом Гельфонда;
# 3.	Методом базы разложения
