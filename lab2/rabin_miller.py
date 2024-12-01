import time
import random

from lab2.itask2 import ITask2


class RabinMillerTest(ITask2):
    def __init__(self):
        self.a = None
        self.r = None
        self.jacob = None

    def print_results(self, num: int) -> None:
        print("__________________________RABIN MILLER TEST__________________________")
        start = time.time()
        result = self.primality_test(num)
        time_spent = start - time.time()
        if result:
            print(f"Number {num} is composite.")
        else:
            print(f"Number {num} is probably prime.")
        if num > 5:
            print(f"a = {self.a}")
            if result and self.jacob is None:
                check_1 = f"\nr = {self.a}^({num - 1}/2) "
                check_2 = f" {self.r}(mod{num})"
                check_result = "Check (is not equal):" + check_1 + "=" + check_2 + f"!= 1(mod{num}) and {num - 1}(mod{num})."
            elif result:
                print(f"(a/n) = {self.jacob}")
                check_1 = f"\nr = {self.a}^({num - 1}/2) "
                check_2 = f" {self.r}(mod{num})"
                check_result = "Check (is not equal):" + check_1 + "=" + check_2 + f"!= {self.jacob}(mod{num})."
            else:
                print(f"(a/n) = {self.jacob}")
                check_1 = f"\nr = {self.a}^({num - 1}/2) "
                check_2 = f" {self.r}(mod{num})."
                check_result = "Check (is equal):" + check_1 + "=" + check_2
            print(check_result)
        print(f"Time consumed: {time_spent} sec")
        self.jacob = None
        print("_____________________________________________________________________")

    def primality_test(self, num: int) -> bool:
        if num == 4:
            return True
        elif num <= 3 or num == 5:
            return False
        elif num > 5:
            self.a = random.randint(a=2, b=(num - 2))
            self.r = pow(self.a, (num - 1) // 2, num)
            if self.r != 1 and self.r != num - 1:
                return False
            else:
                self.jacob = self._jacobi(a=self.a, b=num)
                return False if self.jacob != self.r else True
        return False

    @staticmethod
    def _jacobi(a: int, b: int) -> int:
        result = 1
        x = 0
        while a > 1:
            x = 0
            while a % 2 == 0:
                a //= 2
                x += 1
            if x % 2 != 0 and b % 8 != 1 and b % 8 != 7:
                result *= -1
            if a == 1:
                break
            result *= pow(-1, (b-1)*(a-1)//4)
            a, b = (b % a), a
        if a == 0:
            result = 0
        return result
