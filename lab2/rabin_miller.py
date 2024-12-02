import time
import random

from lab2.itask2 import ITask2


class RabinMillerTest(ITask2):
    def __init__(self):
        self.a = None
        self.r = None
        self.s = None
        self.y = None

    def print_results(self, num: int) -> None:
        print("__________________________RABIN MILLER TEST__________________________")
        start = time.time()
        result = self.primality_test(num)
        time_spent = time.time() - start
        if result:
            print(f"Number {num} is probably prime.")
        else:
            print(f"Number {num} is composite.")
        if num > 5:
            print(f"a = {self.a}")
            if not result and self.y is not None:
                check_1 = f"\ny = {self.y} "
                check_2 = f" {num - 1}."
                check_result = "Check (is not equal):" + check_1 + "!=" + check_2
            else:
                check_1 = f"\ny = {self.y} "
                check_2 = f" {num - 1}."
                check_result = "Check (is equal):" + check_1 + "=" + check_2
            print(check_result)
        print(f"Time consumed: {time_spent} sec")
        self.a = None
        self.r = None
        self.s = None
        self.y = None
        print("_____________________________________________________________________")

    def primality_test(self, num: int) -> bool:
        if num == 4:
            return False
        elif num <= 3 or num == 5:
            return True
        elif num > 5:
            self.r = num - 1
            self.s = 0
            while self.r % 2 == 0:
                self.r //= 2
                self.s += 1
            for i in range(100):
                self.a = random.randint(a=2, b=(num - 2))
                self.y = pow(self.a, self.r, num)
                if self.y != 1 and self.y != num - 1:
                    j = 1
                    while j <= self.s - 1 and self.y != num - 1:
                        self.y = pow(self.y, 2, num)
                        if self.y == 1:
                            return False
                        else:
                            j += 1
                    if self.y != num - 1:
                        return False
        return True
