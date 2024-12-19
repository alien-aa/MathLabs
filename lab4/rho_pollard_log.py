import time
import threading
import pandas as pd
import asyncio
import random
import math


from lab4.itask4 import ITask4


class TimeoutException(Exception): pass


class RhoPollardLog(ITask4):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()
        self.c = []
        self.d = []
        self.log_c = []
        self.log_d = []
        self.i = 0

    async def print_results(self,
                            a: int, b: int, p: int, q: int,
                            filename: str) -> None:
        terminate = False
        start = time.time()
        thread = threading.Thread(target=self.run_discrete_logarithm, args=(a, b, p, q,))
        thread.start()
        thread.join(timeout=7200)

        if thread.is_alive():
            self._stop_event.set()
            terminate = True
            thread.join()
        end = time.time()

        with open(filename, "a") as f:
            f.write("___________________________RHO POLLARD LOG___________________________\n")
            f.write(f"Input values: a = {a}, b = {b}, p = {p}, q = {q}\n")
            iterations = self.i
            if not terminate:
                f.write("Result: SUCCESS\n")
                f.write(f"Value of x: {self.x}\n")
                f.write(f"Time consumed: {end - start} sec\n")
                f.write(f"Iterations: {iterations}\n")
            else:
                f.write("Result: TIMEOUT\n")
                time_spent = end - start
                time_one_iter = time_spent / iterations
                iterations_need = int(2.82 * math.sqrt(q))
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
                               'c': self.c,
                               'd': self.d,
                               'log(c)': self.log_c,
                               'log(d)': self.log_d})
            f.write(df.to_string(index=False))
            f.write("\n_____________________________________________________________________\n")

        self.c = []
        self.d = []
        self.log_c = []
        self.log_d = []
        self.i = 0


    async def discrete_logarithm(self, a: int, b: int, p: int, q: int) -> None:
        start = time.time()
        u = random.randint(0, p)
        v = random.randint(0, p)
        n, m = u, v
        c = (pow(a, u, p) * pow(b, v, p)) % p
        d = c

        self.i += 1
        self._append_custom(self.c, c)
        self._append_custom(self.log_c, f"{u} + {v}x")
        self._append_custom(self.d, d)
        self._append_custom(self.log_d, f"{n} + {m}x")
        while not self._stop_event.is_set():
            c, u, v = self._branching_mapping(a, b, p, q,
                                              c, u, v)
            d, n, m = self._branching_mapping(a, b, p, q,
                                              d, n, m)
            d, n, m = self._branching_mapping(a, b, p, q,
                                              d, n, m)
            self.i += 1
            self._append_custom(self.c, c)
            self._append_custom(self.log_c, f"{u} + {v}x")
            self._append_custom(self.d, d)
            self._append_custom(self.log_d, f"{n} + {m}x")
            if c == d:
                break

        # u + vx = n + mx (mod q)
        x_mult = v - m
        value = n - u
        x, _, d = self.extended_gcd(x_mult, q)
        if d != 1:
            return
        x *= value
        if x < 0:
            while x < 0 and not self._stop_event.is_set():
                x += q
        else:
            while x >= q and not self._stop_event.is_set():
                x -= q
        self.x = x

    def run_discrete_logarithm(self, a: int, b: int, p: int, q: int) -> None:
        asyncio.run(self.discrete_logarithm(a, b, p, q))

    @staticmethod
    def _branching_mapping(a: int, b: int, p: int, q: int,
                           c: int, u: int, v: int) -> list[int]:
        if c < p // 2:
            c = pow(a * c, 1, p)
            u = pow(u + 1, 1, q)
        else:
            c = pow(b * c, 1, p)
            v = pow(v + 1, 1, q)
        return [c, u, v]

    @staticmethod
    def _append_custom(lst, element):
        lst.append(element)
        if len(lst) > 10:
            middle_index = len(lst) // 2
            lst.pop(middle_index)


    @staticmethod
    def extended_gcd(a: int, b: int) -> list[int]:
        x_1, x_2, y_1, y_2 = 1, 0, 0, 1
        while b:
            q = a // b
            a, b = b, a % b
            x_1, x_2 = x_2, x_1 - x_2 * q
            y_1, y_2 = y_2, y_1 - y_2 * q
        return [x_1, y_1, a]