from lab1.euclid import Euclid
from lab1.bineuclid import BinEuclid
from lab1.remaineuclid import RemainEuclid

from lab2.fermat import FermatTest
from lab2.solovay_strassen import SolovayStrassenTest
from lab2.rabin_miller import RabinMillerTest


def read_input(filename: str = ""):
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.readlines()
    tasks = {}
    curr_task = "Not task, but have data"
    tasks[curr_task] = []
    for line in data:
        line = line.strip()
        if line.startswith("Задание"):
            curr_task = line[-1:]
            tasks[curr_task] = []
        elif line and curr_task == "1":
            tasks[curr_task].append(int(line[3:]))
        elif line and curr_task == "2":
            tasks[curr_task].append(int(line[2:]))
        elif line and curr_task == "3":
            tasks[curr_task].append(int(line[2:]))
        elif line and curr_task == "4":
            tasks[curr_task].append(int(line[2:]))
    return tasks

def task1(input_numbers: dict):
    algorithm = Euclid()
    algorithm.gcd_algorithm(a_num=input_numbers["1"][0], b_num=input_numbers["1"][1])
    algorithm.gcd_algorithm(a_num=input_numbers["1"][2], b_num=input_numbers["1"][3])
    algorithm.gcd_algorithm(a_num=input_numbers["1"][4], b_num=input_numbers["1"][5])
    algorithm = BinEuclid()
    algorithm.gcd_algorithm(a_num=input_numbers["1"][0], b_num=input_numbers["1"][1])
    algorithm.gcd_algorithm(a_num=input_numbers["1"][2], b_num=input_numbers["1"][3])
    algorithm.gcd_algorithm(a_num=input_numbers["1"][4], b_num=input_numbers["1"][5])
    algorithm = RemainEuclid()
    algorithm.gcd_algorithm(a_num=input_numbers["1"][0], b_num=input_numbers["1"][1])
    algorithm.gcd_algorithm(a_num=input_numbers["1"][2], b_num=input_numbers["1"][3])
    algorithm.gcd_algorithm(a_num=input_numbers["1"][4], b_num=input_numbers["1"][5])

def task2(input_numbers: dict):
    algorithm = FermatTest()
    algorithm.print_results(num=input_numbers["2"][0])
    algorithm.print_results(num=input_numbers["2"][1])
    algorithm.print_results(num=input_numbers["2"][2])
    algorithm.print_results(num=input_numbers["2"][3])
    algorithm = SolovayStrassenTest()
    algorithm.print_results(num=input_numbers["2"][0])
    algorithm.print_results(num=input_numbers["2"][1])
    algorithm.print_results(num=input_numbers["2"][2])
    algorithm.print_results(num=input_numbers["2"][3])
    algorithm = RabinMillerTest()
    algorithm.print_results(num=input_numbers["2"][0])
    algorithm.print_results(num=input_numbers["2"][1])
    algorithm.print_results(num=input_numbers["2"][2])
    algorithm.print_results(num=input_numbers["2"][3])


def main(input_file: str = ""):
    numbers = read_input(filename=input_file)
    task1(input_numbers=numbers)


if __name__ == "__main__":
    file = "input.txt"
    main(file)