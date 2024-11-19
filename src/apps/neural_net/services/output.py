from typing import Union

import numpy as np
import pandas as pd

from apps.neural_net.exceptions import NumberIsoLongException


def convert_float_to_categorical(number: float) -> list:
    """
    Function takes a number and returns its categorical representation
        (a 2-dimensional array of size 11x10), where index column[0]
        denotes the position of the
        decimal point from the end, and indices column[1-10] denote
        the digits of the number.

    Example for the number 2.29:
    [
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # decimal point at 2nd
                                           position from the end
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 2
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]   # corresponds to digit 9
    ]
    """
    if int(number) == number:
        number = int(number)

    height = 11
    length = 10
    dot_index = 0
    categorical = np.zeros(shape=[height, length], dtype=int)
    number_list = list(str(number))

    if len(number_list) > height:
        raise NumberIsoLongException()

    if isinstance(number, float):
        for iteration, digit in enumerate(reversed(number_list)):
            if digit == ".":
                dot_index = iteration
                del number_list[-iteration - 1]
                break

    categorical[0, dot_index] = 1

    for iteration in range(0, height - 1):
        digit = 0
        if iteration < len(number_list):
            digit = number_list[-iteration - 1]
        categorical[height - 1 - iteration, int(digit)] = 1

    return categorical.tolist()


def convert_categorical_to_number(
    array: list,
) -> Union[int, float]:
    dot_index = np.argmax(array[0])
    array = array[1:]

    numbers = list()
    for row in array:
        numbers.append(str(np.argmax(row)))

    number_type = int
    if dot_index > 0:
        numbers.insert(-dot_index, ".")
        number_type = float

    numbers = "".join(numbers)
    return number_type(numbers)


def compare_numbers(
    num1: Union[float, int], num2: Union[float, int]
) -> int:
    str1 = str(num1)
    str2 = str(num2)

    min_length = min(len(str1), len(str2))
    max_length = max(len(str1), len(str2))
    number_mismatches = 0

    for i in range(min_length):
        if str1[i] != str2[i]:
            number_mismatches += 1

    if max_length > min_length:
        number_mismatches += max_length - min_length

    return number_mismatches
