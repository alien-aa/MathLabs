from abc import ABC, abstractmethod

class ITask2(ABC):
    """
    This class can act as an interface to work with various implementations
    to include the functionality of the primality testing into your project.
    """
    @abstractmethod
    def print_results(self, num: int) -> None:
        pass

    @abstractmethod
    def primality_test(self, num: int) -> bool:
        """
        :param num: integer number
        :return: True if num is composite, False if num is probably prime
        """
        pass
