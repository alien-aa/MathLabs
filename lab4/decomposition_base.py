import time
import threading
import pandas as pd
import asyncio
import random
import math


from lab4.itask4 import ITask4


class TimeoutException(Exception): pass


class DecompositionBase(ITask4):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()
        self.error_flag = False
        self.base = [-1, 2]
        self.a_m = []
        self.u_i =[]
        self.v = None
        self.smooth_values = []
        self.smooth_count = 0
        self.xv = 0
        self.i = 0

    async def print_results(self,
                            a: int, b: int, p: int, q: int,
                            filename: str) -> None:
        terminate = False
        start = time.time()
        thread = threading.Thread(target=self.run_discrete_logarithm, args=(a, b, p, q,))
        thread.start()
        thread.join(timeout=100)

        if thread.is_alive():
            self._stop_event.set()
            terminate = True
            thread.join()
        end = time.time()

        with open(filename, "a") as f:
            f.write("__________________________DECOMPOSITION BASE_________________________\n")
            f.write(f"Input values: a = {a}, b = {b}, p = {p}, q = {q}\n")
            iterations = self.i
            if not terminate and not self.error_flag:
                f.write("Result: SUCCESS\n")
                f.write(f"Value of x: {self.x}\n")
                f.write(f"v = {self.v}, xv = {self.xv}")
                f.write(f"Time consumed: {end - start} sec\n")
                f.write(f"Iterations: {iterations}\n")
            elif not terminate:
                f.write("Result: ERROR - v and q are not mutually simple, and as a result, the algorithm cannot continue to work.\n")
                f.write(f"Time consumed: {end - start} sec\n")
                f.write(f"Iterations: {iterations}\n")
            else:
                f.write("Result: TIMEOUT\n")
                time_spent = end - start
                time_one_iter = time_spent / iterations if iterations != 0 else time_spent
                iterations_need = int(math.exp(2 * math.sqrt(math.log(p) * math.log(math.log(p)))))
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
            f.write(f"Base len: {len(self.base)}\n")
            f.write(f"Base is: {self.base}\n")
            df = pd.DataFrame({'u_i': self.u_i,
                               'b_i': self.smooth_values})
            f.write(df.to_string(index=False))
            f.write("\nV and vectors:\n")
            f.write(f"V  = {self.v}\n")

            if len(self.a_m) >= 5:
                for i in range(len(self.a_m) - 5, len(self.a_m)):
                    f.write(f"{self.a_m[i]}\n")
            else:
                for i in self.a_m:
                    f.write(f"{i}\n")
            f.write("\n_____________________________________________________________________\n")

        self.error_flag = False
        self.base = [-1, 2]
        self.a_m = []
        self.u_i =[]
        self.v = None
        self.smooth_values = []
        self.xv = 0
        self.smooth_count = 0
        self.i = 0


    async def discrete_logarithm(self, a: int, b: int, p: int, q: int) -> None:
        # ph <= M = L(n)^(0.5)
        # L(n) = exp(sqrt(ln(n) * ln(ln(n))))
        log_p = math.log(p, math.e)
        log_2 = math.log(log_p, math.e)
        prime_limit = math.floor(math.sqrt(int(pow(math.e, math.sqrt(log_p * log_2))))) + 1

        # prime numbers generation
        self._build_base(prime_limit)
        dimension = len(self.base) - 1

        # initialization
        u_vector = []
        x_vector = []
        beta = []
        matrix = []
        for k in range(dimension):
            matrix.append([0] * dimension)
            u_vector.append(0)
            beta.append(0)
            x_vector.append(0)
            self.a_m.append([0] * dimension)

        # finding the first v in which b^v (mod p) is B-smooth
        v = 1
        while not self._stop_event.is_set():
            bv = pow(b, v, p)
            if self._smooth(bv, beta, dimension):
                break
            else:
                v += 1
                for i in range(dimension):
                    beta[i] = 0
        self.v = v

        while not self._stop_event.is_set():
            # zeroing out
            for k in range(dimension):
                matrix[k] = ([0] * dimension)
                self.a_m[k] = ([0] * dimension)
                u_vector[k] = 0
                beta[k] = 0
                x_vector[k] = 0

            # by randomly selecting ui, we will find a set of B-smooth numbers
            i = 0
            while i < dimension and not self._stop_event.is_set():
                ui = random.randint(2, p - 1)
                bi = pow(a, ui, p) # a^ui(mod p)
                if not self._smooth(bi, matrix[i], dimension): # not smooth
                    for j in range(dimension):
                        matrix[i][j] = 0
                    if self._smooth(p - bi, matrix[i], dimension): # (p-bi) is smooth
                        if ui in u_vector:
                            for j in range(dimension):
                                matrix[i][j] = 0
                            continue
                        matrix[i][0] = 1 # if there is no such element, add it to the vector of B-smooth
                        u_vector[i] = ui
                        self._append_custom(self.smooth_values, bi)
                        self.smooth_count += 1
                        self._append_custom(self.u_i, ui)
                        self._append_custom(self.a_m, matrix[i])
                        i += 1
                else: # smooth
                    if ui in u_vector:
                        for j in range(dimension):
                            matrix[i][j] = 0
                        continue
                    u_vector[i] = ui
                    self._append_custom(self.smooth_values, bi)
                    self.smooth_count += 1
                    self._append_custom(self.u_i, ui)
                    self._append_custom(self.a_m, matrix[i])
                    i += 1

            # solving a system of linear algebraic equations
            self.a_m = matrix
            if not self._gauss(matrix, u_vector, x_vector, dimension):
                continue

            self.v = 0
            for i in range(dimension):
                self.xv = (int((self.xv  + beta[i] * x_vector[i]) % q))

            x, y, d = self.extended_gcd(v, q)
            if d != 1:
                self.error_flag = True
                return
            x *= self.xv
            if x < 0:
                while x < 0:
                    x += q
            else:
                while x >= q:
                    x -= q
            if pow(a, int(x), p) != b:
                continue
            self.v = v
            return

    def run_discrete_logarithm(self, a: int, b: int, p: int, q: int) -> None:
        asyncio.run(self.discrete_logarithm(a, b, p, q))

    def _build_base(self, limit: int) -> None:
        for i in range(3, limit, 2):
            if i <= 5:
                self.base.append(i)
                continue
            for j in range(1, len(self.base)):
                if self.base[j] > math.floor(math.sqrt(i)) + 1:
                    self.base.append(i)
                    break
                if i % self.base[j] == 0:
                    break

    def _smooth(self, num: int, vector: list[int], dimension: int) -> bool:
        for k in range(dimension):
            vector[k] = 0
        i = 1
        while i < dimension:
            if num % self.base[i] == 0:
                num /= self.base[i]
                vector[i] += 1
                if num == 1:
                    return True
            else:
                i += 1
        return False

    @staticmethod
    def _gauss(a_matrix: list, b_matrix: list, x_matrix: list, n: int) -> bool:
        k = 0
        while k < n:
            max_elem = abs(a_matrix[k][k])
            index = k
            for i in range(k + 1, n):
                if abs(a_matrix[i][k]) > max_elem:
                    max_elem = abs(a_matrix[i][k])
                    index = i
            if max_elem == 0:
                return False
            for j in range(n):
                a_matrix[k][j], a_matrix[index][j] = a_matrix[index][j], a_matrix[k][j]
            b_matrix[k], b_matrix[index] = b_matrix[index], b_matrix[k]
            for i in range(k, n):
                tmp = a_matrix[i][k]
                if abs(tmp) == 0:
                    continue
                for j in range(n):
                    a_matrix[i][j] /= tmp
                b_matrix[i] /= tmp
                if i == k:
                    continue
                for j in range(n):
                    a_matrix[i][j] -= a_matrix[j][k]
                b_matrix[i] -= b_matrix[k]
            k += 1
        for k in range(n - 1, -1, -1):
            x_matrix[k] = b_matrix[k]
            for i in range(k):
                b_matrix[i] -= a_matrix[i][k] * x_matrix[k]
        return True


    @staticmethod
    def _append_custom(lst, element):
        lst.append(element)
        if len(lst) > 5:
            lst.pop(0)


    @staticmethod
    def extended_gcd(a: int, b: int) -> list[int]:
        x_1, x_2, y_1, y_2 = 1, 0, 0, 1
        while b:
            q = a // b
            a, b = b, a % b
            x_1, x_2 = x_2, x_1 - x_2 * q
            y_1, y_2 = y_2, y_1 - y_2 * q
        return [x_1, y_1, a]