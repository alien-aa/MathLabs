import asyncio

from lab1.euclid import Euclid
from lab1.bineuclid import BinEuclid
from lab1.remaineuclid import RemainEuclid

from lab2.fermat import FermatTest
from lab2.solovay_strassen import SolovayStrassenTest
from lab2.rabin_miller import RabinMillerTest

from lab3.rho_pollard import RhoPollard
from lab3.p_1_pollard import Rho1Pollard


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

def repeat_function(n, func, *args, **kwargs):
    """
    Performs the specified function n times.

    :param n: Number of repetitions
    :param func: Function to be executed
    :param args: Positional arguments for func function
    :param kwargs: Keyword arguments for func function
    """
    for _ in range(n):
        func(*args, **kwargs)

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
    repetition_number = 5
    # source: https://arxiv.org/pdf/math/9803082
    number_1 = 32809426840359564991177172754241
    #num_1_div = [13, 17, 19, 23, 29, 31, 37, 41, 43, 61, 67, 71, 73,  97, 127, 199, 281, 397]
    number_2 = 2810864562635368426005268142616001
    #num_2_div = [13, 17, 19, 23, 29, 31, 37, 41, 43, 61, 67, 71, 73, 109, 113, 127, 151, 281, 353]
    number_3 = 349407515342287435050603204719587201
    #num_3_div = [11, 13, 17, 19, 29, 31, 37, 41, 43, 61, 71, 73, 97, 101, 109, 113, 151, 181, 193, 641]

    algorithm = FermatTest()
    repeat_function(repetition_number, algorithm.print_results, input_numbers["2"][0])
    repeat_function(repetition_number, algorithm.print_results, input_numbers["2"][1])
    repeat_function(repetition_number, algorithm.print_results, input_numbers["2"][2])
    repeat_function(repetition_number, algorithm.print_results, input_numbers["2"][3])
    algorithm = SolovayStrassenTest()
    repeat_function(repetition_number, algorithm.print_results, input_numbers["2"][0])
    repeat_function(repetition_number, algorithm.print_results, input_numbers["2"][1])
    repeat_function(repetition_number, algorithm.print_results, input_numbers["2"][2])
    repeat_function(repetition_number, algorithm.print_results, input_numbers["2"][3])
    algorithm = RabinMillerTest()
    repeat_function(repetition_number, algorithm.print_results, input_numbers["2"][0])
    repeat_function(repetition_number, algorithm.print_results, input_numbers["2"][1])
    repeat_function(repetition_number, algorithm.print_results, input_numbers["2"][2])
    repeat_function(repetition_number, algorithm.print_results, input_numbers["2"][3])

    print("CARMICHAEL NUMBERS:")

    algorithm = FermatTest()
    repeat_function(repetition_number, algorithm.print_results, number_1)
    repeat_function(repetition_number, algorithm.print_results, number_2)
    repeat_function(repetition_number, algorithm.print_results, number_3)

    algorithm = SolovayStrassenTest()
    repeat_function(repetition_number, algorithm.print_results, number_1)
    repeat_function(repetition_number, algorithm.print_results, number_2)
    repeat_function(repetition_number, algorithm.print_results, number_3)

    algorithm = RabinMillerTest()
    repeat_function(repetition_number, algorithm.print_results, number_1)
    repeat_function(repetition_number, algorithm.print_results, number_2)
    repeat_function(repetition_number, algorithm.print_results, number_3)

def task3(input_numbers: dict):
    output_file = "task3_result.txt"
    algorithm = RhoPollard(c=1, add=5)
    asyncio.run(algorithm.print_results(input_numbers["3"][0], output_file))
    algorithm = Rho1Pollard()
    asyncio.run(algorithm.print_results(input_numbers["3"][0], output_file))
    algorithm = RhoPollard(c=1, add=5)
    asyncio.run(algorithm.print_results(input_numbers["3"][1], output_file))
    algorithm = Rho1Pollard()
    asyncio.run(algorithm.print_results(input_numbers["3"][1], output_file))
    algorithm = RhoPollard(c=1, add=5)
    asyncio.run(algorithm.print_results(input_numbers["3"][2], output_file))
    algorithm = Rho1Pollard()
    asyncio.run(algorithm.print_results(input_numbers["3"][2], output_file))


def main(input_file: str = ""):
    numbers = read_input(filename=input_file)
    task2(input_numbers=numbers)
    # task3(input_numbers=numbers)


if __name__ == "__main__":
    file = "input.txt"
    main(file)