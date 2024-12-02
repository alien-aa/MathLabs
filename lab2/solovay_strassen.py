import time
import random

from lab2.itask2 import ITask2


class SolovayStrassenTest(ITask2):
    def __init__(self):
        self.a = None
        self.r = None
        self.jacob = None

    def print_results(self, num: int) -> None:
        print("________________________SOLOVAY STRASSEN TEST________________________")
        start = time.time()
        result = self.primality_test(num)
        time_spent = time.time() - start
        if result:
            print(f"Number {num} is probably prime.")
        else:
            print(f"Number {num} is composite.")
        if num > 5:
            print(f"a = {self.a}")
            if not result and self.jacob is None:
                check_1 = f"\nr = {self.a}^({num - 1}/2) "
                check_2 = f" {self.r}(mod{num}) "
                check_result = "Check (is not equal):" + check_1 + "=" + check_2 + f"!= 1(mod{num}) and {num - 1}(mod{num})."
            elif not result:
                print(f"(a/n) = {self.jacob}")
                check_1 = f"\nr = {self.a}^({num - 1}/2) "
                check_2 = f" {self.r}(mod{num}) "
                check_result = "Check (is not equal):" + check_1 + "=" + check_2 + f"!= {self.jacob}(mod{num})."
            else:
                print(f"(a/n) = {self.jacob}")
                check_1 = f"\nr = {self.a}^({num - 1}/2) "
                check_2 = f" {self.r}(mod{num})."
                check_result = "Check (is equal):" + check_1 + "=" + check_2
            print(check_result)
        print(f"Time consumed: {time_spent} sec")
        self.r = None
        self.a = None
        self.jacob = None
        print("_____________________________________________________________________")

    def primality_test(self, num: int) -> bool:
        if num == 4:
            return False
        elif num <= 3 or num == 5:
            return True
        elif num > 5:
            self.a = random.randint(a=2, b=(num - 2))
            self.r = pow(self.a, ((num - 1) // 2), num)
            if self.r != 1 and self.r != num - 1:
                return False
            else:
                self.jacob = self._jacobi(a=self.a, b=num)
                if self.jacob < 0:
                    self.r -= num
                return self.jacob == self.r
        return False

    @staticmethod
    def _jacobi(a: int, b: int) -> int:
        result = 1
        k = 0
        s = 1
        while True:
            if a == 0:
                return 0
            if a == 1:
                return result
            while a % 2 == 0:
                a //= 2
                k += 1
            if k % 2 == 0:
                s = 1
            elif b % 8 == 1 or b % 8 == 7:
                s = 1
            elif b % 8 == 3 or b % 8 == 5:
                s = -1
            result *= s
            if a != 1:
                result *= pow(-1, (b - 1) * (a - 1) // 4)
                a, b = b, a
                a %= b
