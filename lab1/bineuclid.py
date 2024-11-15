import pandas as pd
import time

from lab1.itask1 import ITask1

class BinEuclid(ITask1):
    def gcd_algorithm(self, a_num: int, b_num: int) -> None:
        print("__________________EXTENDED BINARY EUCLID ALGORITHM___________________")
        if b_num > a_num:
            a_num, b_num = b_num, a_num
            print(f"Search for GcD({b_num, a_num}) = GCD({a_num, b_num}):")
        else:
            print(f"Search for GCD({a_num, b_num}):")
        start_time = time.time()
        result = self._extended_bin_gcd(a_input=a_num, b_input=b_num)
        end_time = time.time()
        print(f"\ngGCD({a_num}, {b_num}) = {result["gcd"]} \nx = {result["x"]} \ny = {result["y"]}")
        if a_num * result["x"] + b_num * result["y"] == result["gcd"]:
            print(f"[INFO] Check is correct: {a_num} * {result["x"]} + {b_num} * {result["y"]} = {result["gcd"]}")
        else:
            print(f"[ER] Check is incorrect:",
                  f"\n{a_num * result["x"] + b_num * result["y"]}\nis not equal to\n{result["gcd"]}")
        print(f"Time consumed: {end_time - start_time} sec")
        print("_____________________________________________________________________")

    @staticmethod
    def _extended_bin_gcd(a_input: int, b_input: int) -> dict[str, int]:
        mult_c = 1
        if a_input % b_input == 0:
            return {"gcd": b_input,
                    "x": 0,
                    "y": 1}
        if a_input == b_input:
            return {"gcd": a_input,
                    "x": 0,
                    "y": 1}
        while (a_input % 2 == 0) and (b_input % 2 == 0):
            a_input = a_input // 2
            b_input = b_input // 2
            mult_c *= 2
        u_values = [a_input]
        v_values = [b_input]
        a_values = [1]
        b_values = [0]
        c_values = [0]
        d_values = [1]
        u = a_input
        v = b_input
        a = 1
        b = 0
        c = 0
        d = 1
        while u != 0:
            while u % 2 == 0:
                u = u // 2
                if a % 2 == 0 and b % 2 == 0:
                    a = a // 2
                    b = b // 2
                else:
                    a = (a + b_input) // 2
                    b = (b - a_input) // 2
            while v % 2 == 0:
                v = v // 2
                if c % 2 == 0 and d % 2 == 0:
                    c = c // 2
                    d = d // 2
                else:
                    c = (c + b_input) // 2
                    d = (d - a_input) // 2
            u_values.append(u)
            v_values.append(v)
            a_values.append(a)
            b_values.append(b)
            c_values.append(c)
            d_values.append(d)
            if u >= v:
                u = u - v
                a = a - c
                b = b - d
                u_values.append(u)
                v_values.append('-')
                a_values.append(a)
                b_values.append(b)
                c_values.append('-')
                d_values.append('-')
            else:
                v = v - u
                c = c - a
                d = d - b
                u_values.append('-')
                v_values.append(v)
                a_values.append('-')
                b_values.append('-')
                c_values.append(c)
                d_values.append(d)
        gcd = mult_c * v
        x = c
        y = d
        df = pd.DataFrame({'u': u_values, 'v': v_values, 'A': a_values, 'B': b_values, 'C': c_values, 'D': d_values})

        if df.shape[0] > 20:
            print(df.head(5).to_string())
            print("<...>")
            print(df.tail(5).to_string(header=False))
        else:
            print(df)
        return {"gcd": gcd,
                "x": x,
                "y": y}

