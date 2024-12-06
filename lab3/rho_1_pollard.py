import time
import threading
import asyncio
import pandas as pd
import random
import math

from lab3.itask3 import ITask3


class TimeoutException(Exception): pass


class Rho1Pollard(ITask3):
    def __init__(self):
        super().__init__()
        self.b = []
        self.l = []
        self.a = []
        self.d = []
        self.i = 0
        self._stop_event = threading.Event()

    async def print_results(self, num: int, filename: str) -> None:
        terminate = False
        start = time.time()
        thread = threading.Thread(target=self.run_factorization, args=(num,))
        thread.start()
        thread.join(timeout=3600)

        if thread.is_alive():
            self._stop_event.set()
            terminate = True
            thread.join()
        end = time.time()
        with open(filename, "a") as f:
            f.write("____________________________RHO-1 POLLARD____________________________\n")
            f.write(f"Number: {num}\n")
            iterations = self.i
            if not terminate:
                f.write("Result: SUCCESS\n")
                f.write(f"Divider: {self.p}\n")
                f.write(f"Time consumed: {end - start} sec\n")
                f.write(f"Iterations: {iterations}\n")
            else:
                f.write("Result: TIMEOUT\n")
                time_spent = end - start
                time_one_iter = time_spent / iterations
                iterations_need = iterations * math.log(iterations) * pow(math.log(num), 2)
                time_need = time_one_iter * iterations_need
                f.write(f"Time consumed: {time_spent} sec\n")
                f.write(f"Iterations: {iterations}\n")
                f.write(f"Duration of one iteration: {time_one_iter} sec\n")
                f.write(f"Estimated number of iterations: {iterations_need}\n")
                tmp = time_need
                years = tmp // (365 * 24 * 3600)
                tmp %= (365 * 24 * 3600)
                days = tmp // (24 * 3600)
                tmp %= (24 * 3600)
                hours = tmp // 3600
                tmp %= 3600
                minutes = tmp // 60
                seconds = tmp % 60
                f.write(f"Estimated execution time: {time_need} s = {years} y {days} d {hours} h {minutes} m {seconds} s\n")
            if iterations > 10:
                i_array = [i for i in range(1, 6)]
                i_array += [i for i in range(iterations - 4, iterations + 1)]
            else:
                i_array = [i for i in range(1, iterations + 1)]
            df = pd.DataFrame({'i': i_array,
                               'B[i]': self.b,
                               'l': self.l,
                               'a': self.a,
                               'd': self.d})
            f.write(df.to_string(index=False))
            f.write("\n_____________________________________________________________________\n")
        self.b = []
        self.l = []
        self.a = []
        self.d = []
        self.i = 0


    async def factorization(self, num: int) -> None:
        p_i = 3
        a = random.randint(2, num - 2)
        d = self._simplified_gcd_func(a, num)
        if d >= 2:
            self.p = d
            return
        else:
            while not self._stop_event.is_set():
                l = math.log(num) // math.log(p_i)
                a = pow(a, pow(p_i, int(l)), num)
                d = self._simplified_gcd_func(a - 1, num)
                self._append_custom(self.b, p_i)
                self._append_custom(self.l, l)
                self._append_custom(self.a, a)
                self._append_custom(self.d, d)
                self.i += 1
                if d != 1 and d != num:
                    self.p = d
                    return
                else:
                    p_i += 1
                while not self._primality_test(p_i):
                    p_i += 1
                if p_i > num:
                    self.p = -1
                    return

    def run_factorization(self, num: int):
        asyncio.run(self.factorization(num))

    @staticmethod
    def _simplified_gcd_func(a: int, b: int) -> int:
        r1 = max(a, b)
        r2 = min(a, b)
        while r2 != 0:
            r1, r2 = r2, r1 % r2
        return r1

    @staticmethod
    def _primality_test(num: int) -> bool:
        if num == 4:
            return False
        elif num <= 5:
            return True
        r = num - 1
        s = 0
        while r % 2 == 0:
            r = r // 2
            s += 1
        a = random.randint(2, num - 2)
        y = pow(a, r, num)
        if y != 1 and y != num - 1:
            j = 1
            while j <= s - 1 and y != num - 1:
                y = pow(y, 2, num)
                if y == 1:
                    return False
                j += 1
            if y != num - 1:
                return False
        return True

    @staticmethod
    def _append_custom(lst, element):
        lst.append(element)
        if len(lst) > 10:
            middle_index = len(lst) // 2
            lst.pop(middle_index)