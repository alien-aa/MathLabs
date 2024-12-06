import time
import threading
import pandas as pd
import asyncio


from lab3.itask3 import ITask3


class TimeoutException(Exception): pass


class RhoPollard(ITask3):
    def __init__(self, c: int, add: int):
        super().__init__()
        self.a = []
        self.b = []
        self.d = []
        self.i = 0
        self.c = c
        self.add = add
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
            f.write("_____________________________RHO POLLARD_____________________________\n")
            f.write(f"Number: {num}\n")
            f.write(f"c = {self.c}, compressive mapping is f(x) = x^2 + {self.add}\n")
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
                iterations_need = pow(num, 0.25)
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
                               'a': self.a,
                               'b': self.b,
                               'd': self.d})
            f.write(df.to_string(index=False))
            f.write("\n_____________________________________________________________________\n")
        self.a = []
        self.b = []
        self.d = []
        self.i = 0

    def run_factorization(self, num: int):
        asyncio.run(self.factorization(num))

    async def factorization(self, num: int) -> None:
        a = self.c
        b = self.c
        d = 1
        while d == 1 and not self._stop_event.is_set():
            self._append_custom(self.a, a)
            self._append_custom(self.b, b)
            self._append_custom(self.d, d)
            self.i += 1
            a = self._compressive_mapping(a, num)
            b = self._compressive_mapping(self._compressive_mapping(b, num), num)
            d = self._simplified_gcd_func(abs(a - b), num)
            if 1 < d < num:
                self.p = d
                break
            if d == num:
                break
        self._append_custom(self.a, a)
        self._append_custom(self.b, b)
        self._append_custom(self.d, d)
        self.i += 1

    def _compressive_mapping(self, x: int, n: int) -> int:
        return (pow(x, 2) + self.add) % n

    @staticmethod
    def _simplified_gcd_func(a: int, b: int) -> int:
        r1 = max(a, b)
        r2 = min(a, b)
        while r2 != 0:
            r1, r2 = r2, r1 % r2
        return r1

    @staticmethod
    def _append_custom(lst, element):
        lst.append(element)
        if len(lst) > 10:
            middle_index = len(lst) // 2
            lst.pop(middle_index)