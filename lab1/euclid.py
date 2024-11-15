import pandas as pd
import time

from lab1.itask1 import ITask1

class Euclid(ITask1):
    def gcd_algorithm(self, a_num: int, b_num: int) -> None:
        print("______________________EXTENDED EUCLID ALGORITHM______________________")
        if b_num > a_num:
            a_num, b_num = b_num, a_num
            print(f"Search for GCD({b_num, a_num}) = GCD(){a_num, b_num}:")
        else:
            print(f"Search for GCD({a_num, b_num}):")
        start_time = time.time()
        result = self._extended_gcd(a=a_num, b=b_num)
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
    def _extended_gcd(a: int, b: int) -> dict[str, int]:
        if a % b == 0:
            return {"gcd": b,
                    "x": 0,
                    "y": 1}
        if a == b:
            return {"gcd": a,
                    "x": 0,
                    "y": 1}
        r_values = [a, b]
        x_values = [1, 0]
        y_values = [0, 1]
        q_values = [0]
        i = 1
        gcd = 0
        x_res = 0
        y_res = 0
        while r_values[i] != 0:
            q = r_values[i - 1] // r_values[i]
            q_values.append(q)
            r = r_values[i - 1] % r_values[i]
            r_values.append(r)
            x = x_values[i - 1] - q * x_values[i]
            x_values.append(x)
            y = y_values[i - 1] - q * y_values[i]
            y_values.append(y)
            gcd = r_values[i]
            x_res = x_values[i]
            y_res = y_values[i]
            i += 1
        q_values.append(0)
        df = pd.DataFrame({'r': r_values, 'x': x_values, 'y': y_values, 'q': q_values})

        if df.shape[0] > 20:
            print(df.head(5).to_string())
            print("<...>")
            print(df.tail(5).to_string(header=False))
        else:
            print(df)
        return {"gcd": gcd,
                "x": x_res,
                "y": y_res}
