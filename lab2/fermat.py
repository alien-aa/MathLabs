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
        time_spent = start - time.time()
        if result:
            print(f"Number {num} is composite.")
        else:
            print(f"Number {num} is probably prime.")
        if num > 5:
            print(f"a = {self.a}")
            check_1 = f"\nr = {self.a}^{num - 1} "
            check_2 = f" {self.r}(mod{num})"
            if result:
                check_result = "Check (is not equal):" + check_1 + "=" + check_2 + f"!= 1(mod{num})."
            else:
                check_result = "Check (is equal):" + check_1 + "=" + check_2 + "."
            print(check_result)
        print(f"Time consumed: {time_spent} sec")
        print("_____________________________________________________________________")

    def primality_test(self, num: int) -> bool:
        if num == 4:
            return True
        elif num <= 3 or num == 5:
            return False
        elif num > 5:
            self.a = random.randint(a=2, b=(num - 2))
            self.r = pow(self.a, num - 1, num)
            return True if self.r == 1 else False
