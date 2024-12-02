import time
import random

from lab2.itask2 import ITask2


class FermatTest(ITask2):
    def __init__(self):
        self.a = None
        self.r = None

    def print_results(self, num: int) -> None:
        print("_____________________________FERMAT TEST_____________________________")
        start = time.time()
        result = self.primality_test(num)
        time_spent = time.time() - start
        if result:
            print(f"Number {num} is probably prime.")
        else:
            print(f"Number {num} is composite.")
        if num > 5:
            print(f"a = {self.a}")
            check_1 = f"\nr = {self.a}^{num - 1} "
            check_2 = f" {self.r}(mod{num})"
            if not result:
                check_result = "Check (is not equal):" + check_1 + "=" + check_2 + f"!= 1(mod{num})."
            else:
                check_result = "Check (is equal):" + check_1 + "=" + check_2 + "."
            print(check_result)
        print(f"Time consumed: {time_spent} sec")
        self.r = None
        self.a = None
        print("_____________________________________________________________________")

    def primality_test(self, num: int) -> bool:
        if num == 4:
            return False
        elif num <= 3 or num == 5:
            return True
        elif num > 5:
            self.a = random.randint(a=2, b=(num - 2))
            self.r = pow(self.a, (num - 1), num)
            return self.r == 1
