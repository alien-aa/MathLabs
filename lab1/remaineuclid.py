import pandas as pd
import time

from lab1.itask1 import ITask1

class RemainEuclid(ITask1):
    def gcd_algorithm(self, a_num: int, b_num: int) -> None:
        print("__________________EXTENDED REMAIN EUCLID ALGORITHM___________________")
        if b_num > a_num:
            a_num, b_num = b_num, a_num
            print(f"Search for GcD({b_num, a_num}) = GCD({a_num, b_num}):")
        else:
            print(f"Search for GCD({a_num, b_num}):")
        start_time = time.time()
        result = self._extended_remain_gcd(a_input=a_num, b_input=b_num)
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
    def _extended_remain_gcd(a_input: int, b_input: int) -> dict[str, int]:
        q_values = ['-']
        x_values = [1, 0]
        y_values = [0, 1]
        r_values = [a_input]
        x_res = 0
        y_res = 0
        x0, x1, y0, y1, i = 1, 0, 0, 1, 1
        while b_input:
            q = a_input // b_input
            a_input, b_input, r = b_input, a_input % b_input, b_input
            x0, x1 = x1, x0 - x1 * q
            y0, y1 = y1, y0 - y1 * q
            if b_input > r >> 1:
                b_input = r - b_input
                x1, y1 = x0 - x1, y0 - y1
            q_values.append(q)
            r_values.append(r)
            x_values.append(x0)
            y_values.append(y0)
            x_res = x0
            y_res = y0
            i += 1
        q_values.append('-')
        r_values.append('0')
        df = pd.DataFrame({'r': r_values, 'x': x_values, 'y': y_values, 'q': q_values})

        if df.shape[0] > 20:
            print(df.head(5).to_string())
            print("<...>")
            print(df.tail(5).to_string(header=False))
        else:
            print(df)
        return {"gcd": a_input,
                "x": x_res,
                "y": y_res}

