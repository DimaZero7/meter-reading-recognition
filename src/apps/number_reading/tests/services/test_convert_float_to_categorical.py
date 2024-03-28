import numpy as np
from django.test import TestCase

from apps.number_reading.exceptions import NumberIsoLongException
from apps.number_reading.services import convert_float_to_categorical


class ConvertFloatToCategoricalTest(TestCase):
    def test_result_type(self):
        # Create data
        number = 1

        # Action
        result = convert_float_to_categorical(number=number)

        # Check
        self.assertIsInstance(result, np.ndarray)

    def test_result_shape(self):
        # Create data
        number = 1

        # Action
        result = convert_float_to_categorical(number=number)

        # Check
        self.assertEqual(result.shape, (11, 10))

    def test_result_dtype(self):
        # Create data
        number = 1

        # Action
        result = convert_float_to_categorical(number=number)

        # Check
        self.assertEqual(result.dtype, int)

    def test_after_point_zero(self):
        """
        Checks that if a number with a fractional part equal to 0 is passed, then 1 will be at
            position array[0][0].

        Input number: 4.00
        Expected value:
        [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # decimal point at 0th position from the end
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]   # corresponds to digit 4
        ]
        """
        # Create data
        number = 4.00
        expected_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4]

        # Action
        result = convert_float_to_categorical(number=number)

        # Check
        for iteration, column in enumerate(result):
            self.assertEqual(np.argmax(column), expected_values[iteration])

    def test_real_number(self):
        """
        Input number: 123.001
        Expected value:
        [
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # decimal point at 3th position from the end
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 1
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 2
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # corresponds to digit 3
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]   # corresponds to digit 1
        ]
        """
        # Create data
        number = 123.001
        expected_values = [3, 0, 0, 0, 0, 1, 2, 3, 0, 0, 1]

        # Action
        result = convert_float_to_categorical(number=number)

        # Check
        for iteration, column in enumerate(result):
            self.assertEqual(np.argmax(column), expected_values[iteration])

    def test_natural_number(self):
        """
        Input number: 123
        Expected value:
        [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # decimal point at 0th position from the end
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 1
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 2
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]   # corresponds to digit 3
        ]
        """
        # Create data
        number = 123
        expected_values = [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3]

        # Action
        result = convert_float_to_categorical(number=number)

        # Check
        for iteration, column in enumerate(result):
            self.assertEqual(np.argmax(column), expected_values[iteration])

    def test_min_number(self):
        """
        Input number: 0
        Expected value:
        [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # decimal point at 0th position from the end
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]   # corresponds to digit 0
        ]
        """
        # Create data
        number = 0
        expected_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Action
        result = convert_float_to_categorical(number=number)

        # Check
        for iteration, column in enumerate(result):
            self.assertEqual(np.argmax(column), expected_values[iteration])

    def test_max_number(self):
        """
        Input number: 123456789.9
        Expected value:
        [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # decimal point at 0th position from the end
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],  # corresponds to digit 0
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # corresponds to digit 0
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # corresponds to digit 0
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # corresponds to digit 0
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # corresponds to digit 0
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # corresponds to digit 0
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]   # corresponds to digit 0
        ]
        """
        # Create data
        number = 1.234567899
        expected_values = [9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9]

        # Action
        result = convert_float_to_categorical(number=number)

        # Check
        for iteration, column in enumerate(result):
            self.assertEqual(np.argmax(column), expected_values[iteration])

    def test_number_more_11_characters(self):
        # Create data
        number = 123456789.12

        # Check
        with self.assertRaises(NumberIsoLongException):
            convert_float_to_categorical(number=number)
