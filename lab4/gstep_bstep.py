import time
import threading
import pandas as pd
import asyncio
import math


from lab4.itask4 import ITask4


class TimeoutException(Exception): pass


class GiantStepBabyStep(ITask4):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()
        self.s = -1
        self.database = []
        self.save_database = []
        self.t = -1
        self.k = -1
        self.time_sec_sequence = 0
        self.i = 0
        self.j = 0

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
            f.write("_________________________GIANT-STEP-BABY-STEP________________________\n")
            f.write(f"Input values: a = {a}, b = {b}, p = {p}, q = {q}\n")
            f.write(f"s = {self.s}\n")
            iterations = self.i
            if not terminate and self.x is not None:
                f.write("Result: SUCCESS\n")
                f.write(f"Value of x: {self.x}\n")
                f.write(f"Time consumed: {end - start} sec\n")
                f.write(f"Iterations: {iterations}, for second sequence: {self.j}\n")
            elif terminate:
                f.write("Result: TIMEOUT\n")
                time_spent = end - start
                time_seq_spent = end - self.time_sec_sequence
                time_one_iter = time_spent / iterations
                iterations_need = math.ceil(2 * (math.sqrt(q) + math.log2(q)) - 1)
                time_need = time_one_iter * iterations_need
                f.write(f"Sequence 2 is built up to the value of t = {self.j}\n")
                f.write(f"Time consumed: {time_spent} sec, for second sequence: {time_seq_spent} sec\n")
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
            else:
                f.write("Result: MEMORY ERROR (too many values in sequence)\n")
                time_spent = end - start
                time_one_iter = time_spent / iterations
                iterations_need = math.ceil(2 * (math.sqrt(q) + math.log2(q)) - 1)
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

            df = pd.DataFrame({'k': [k[0] for k in self.save_database],
                               'sequence element': [x[1] for x in self.save_database]})
            f.write(df.to_string(index=False))
            f.write("\n_____________________________________________________________________\n")

        self.s = -1
        self.database.clear()
        self.t = -1
        self.k = -1
        self.time_sec_sequence = 0
        self.i = 0
        self.j = 0


    async def discrete_logarithm(self, a: int, b: int, p: int, q: int) -> None:
        s = math.floor(math.sqrt(q)) + 1
        self.s = s
        if self._form_first_sequence(a, b, p):
            self.time_sec_sequence = time.time()
            curr_seq_number = 1
            for t in range(s):
                if self._stop_event.is_set():
                    break
                for item in self.database:
                    if item[1] == curr_seq_number:
                        self.t = t
                        self.k = item[0]
                        self.x = (self.t + self.k * self.s) % q
                        return
                    elif item[1] > curr_seq_number:
                        break
                curr_seq_number = (curr_seq_number * a) % p
                self.i += 1
                self.j += 1


    def _form_first_sequence(self, a: int, b: int, p: int) -> bool:
        s = self.s
        x, y, d = self.extended_gcd(pow(a, s, p), p)
        a_1 = x + p
        for k in range(s):
            if self._stop_event.is_set():
                break
            curr_seq_number = (b * pow(a_1, k, p)) % p
            try:
                self._append_custom(self.save_database, [k, curr_seq_number])
                self.database.append([k, curr_seq_number])
            except MemoryError:
                return False
            self.i += 1
        try:
            self.database.sort(key=lambda elem: elem[1])
        except MemoryError:
            return False
        return True

    @staticmethod
    def extended_gcd(a: int, b: int) -> list[int]:
        x_1, x_2, y_1, y_2 = 1, 0, 0, 1
        while b:
            q = a // b
            a, b = b, a % b
            x_1, x_2 = x_2, x_1 - x_2 * q
            y_1, y_2 = y_2, y_1 - y_2 * q
        return [x_1, y_1, a]

    def run_discrete_logarithm(self, a: int, b: int, p: int, q: int) -> None:
        try:
            asyncio.run(self.discrete_logarithm(a, b, p, q))
        except MemoryError:
            return


    @staticmethod
    def _append_custom(lst, element):
        lst.append(element)
        if len(lst) > 10:
            middle_index = len(lst) // 2
            lst.pop(middle_index)