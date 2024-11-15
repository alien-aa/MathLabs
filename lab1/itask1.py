from abc import ABC, abstractmethod

class ITask1(ABC):
    """
    This class can act as an interface for working with different implementations
    to include the functionality of finding the GCD in your project.
    """
    @abstractmethod
    def gcd_algorithm(self, a_num: int, b_num: int):
        pass
