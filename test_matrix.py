"""
Test Matrix class pulled from week3 repo using Mark Murnane's branch as a starting point
as required via assignment specification. Class names and references here are referencing etivity 3

I have added to these tests the extra requirements for Etivitiy 4
"""

import unittest

from matrix import Matrix


class TestMatrixImplementationEtivity3(unittest.TestCase):
    """Tests the implementation of the Matrix class for Etivity 3.

    Unit tests are:
        1) Create a new matrix and confirm size is correctly reported in a tuple
        2) Add two matrices
        3) Subtract two matrices
        5) Multiply a matrix by a scalar
        6) Multiply a matrix by a vector
        7) Multiply a matrix by a matrix
        8) Test equality and inequality

    Edge Cases in this Unit Test are:
        1) Create a new matrix with an empty list or non-list parameter
        2) Create a matrix with non-list rows
        3) Create a matrix with empty rows
        4) Create a matrix with rows that are not the same length
        5) Perform addition/subtraction of a matrix and a non-matrix
        6) Perform addition/subtraction of a matrix and an incompatible matrix
        7) Multiply a matrix by a non-numeric value
        8) Multiply a matrix by an incompatible matrix

        ========================================================================

        Added 3 more tests to show that determinant, inverse and cross product are all working.
    """

    # Internal matrix and (column) vector representations for test cases
    def setUp(self):
        self._A_2x2 = ((1, 3), (5, 7))
        self._B_2x2 = ((2, 4), (6, 8))
        self._C_2x2 = ((4, 7), (2, 6))

        self._E_vector = ([1], [2], [3])
        self._F_vector = ([1], [5], [7])

        self._Err_A_2x2 = [[1, 3], ["5", 7]]
        self._Err_B_2x2 = [[2, 4], []]
        self._Err_C_2x2 = [[1, 2], [4, 5, 6]]
        self._Err_D = [[3, 4], 5]

        self._B_2x1 = [[2], [1]]

        self._A_3x3 = [[1, 2, 3], [0, 3, 4], [5, 6, 8]]
        self._B_3x3 = [[1, 3, 6], [2, 1, 2], [4, 2, 1]]

        self._B_3x1 = [[2], [1], [3]]

        self._B_3x2 = [[4, 7], [3, 9], [5, 2]]

    def test_matrix_creation(self):
        # Checks that a matrix is created successfully with the correct dimensions and content
        a = Matrix(self._A_2x2)
        self.assertEqual(a.get_order(), (2, 2))
        self.assertEqual(a.elements, self._A_2x2)

    def test_matrix_invalid_creation(self):
        # Checks that a matrix can't be created without a valid element list
        self.assertRaises(TypeError, Matrix, None)
        self.assertRaises(TypeError, Matrix, [])
        self.assertRaises(TypeError, Matrix, self._Err_D)
        self.assertRaises(ValueError, Matrix, self._Err_A_2x2)
        self.assertRaises(ValueError, Matrix, self._Err_B_2x2)
        self.assertRaises(ValueError, Matrix, self._Err_C_2x2)

    def test_matrix_add_matrices(self):
        # Checks that two same size matrices are added together correctly
        a = Matrix(self._A_2x2)
        b = Matrix(self._B_2x2)
        c = a + b
        expected = ((3, 7), (11, 15))
        self.assertEqual(c.elements, expected)

    def test_matrix_add_invalid_matrices(self):
        # Checks that two same differing size matrices can't be added or subtracted
        a = Matrix(self._A_2x2)
        b = Matrix(self._B_3x3)

        func = lambda x, y: x + y

        self.assertRaises(TypeError, func, a, b)
        self.assertRaises(TypeError, func, a, 3)
        self.assertRaises(TypeError, func, a, "")

    def test_matrix_subtract_matrices(self):
        # Checks that two same size matrices are added together correctly
        a = Matrix(self._A_2x2)
        b = Matrix(self._B_2x2)
        c = a - b
        expected = ((-1, -1), (-1, -1))
        self.assertEqual(c.elements, expected)

    def test_matrix_subtract_invalid_matrices(self):
        # Checks that two same differing size matrices can't be added or subtracted
        a = Matrix(self._A_2x2)
        b = Matrix(self._B_3x3)

        func = lambda x, y: x - y

        self.assertRaises(TypeError, func, a, b)
        self.assertRaises(TypeError, func, a, 3)
        self.assertRaises(TypeError, func, a, "")

    def test_matrix_multiply_by_scalar(self):
        # Checks the correct multiplication of a matrix by a scalar
        a = Matrix(self._B_3x2)
        b = a * 3
        expected = ((12, 21), (9, 27), (15, 6))
        self.assertEqual(b.elements, expected)

    def test_matrix_multiply_by_vector(self):
        # Checks the correct multiplication of a matrix by a vector
        a = Matrix(self._B_2x2)
        b = Matrix(self._B_2x1)
        c = a @ b
        expected = ((8,), (20,))
        self.assertEqual(c.elements, expected)

    def test_matrix_multiply_same_order_matrices(self):
        # Checks that two same size matrices are multiplied together correctly
        a = Matrix(self._A_2x2)
        b = Matrix(self._B_2x2)
        c = a @ b
        expected = ((20, 28), (52, 76))
        self.assertEqual(c.elements, expected)

    def test_matrix_multiply_nonsquare_matrices(self):
        # Checks that two different size matrices are multiplied together correctly
        a = Matrix(self._A_3x3)
        b = Matrix(self._B_3x2)
        c = a @ b
        expected = ((25, 31), (29, 35), (78, 105))
        self.assertEqual(c.elements, expected)

    def test_matrix_multiply_incompatible_matrices(self):
        # Checks that matrices with incompatible dimension/order can't be multiplied
        a = Matrix(self._A_3x3)
        b = Matrix(self._B_3x2)

        func = lambda x, y: x * y

        self.assertRaises(TypeError, func, b, a)

    def test_matrix_multiply_non_numeric(self):
        # Checks that matrices can't be multiplied by a string or non-Matrix object
        a = Matrix(self._A_2x2)

        func = lambda x, y: x * y

        self.assertRaises(TypeError, func, a, "")
        self.assertRaises(TypeError, func, a, None)
        self.assertRaises(TypeError, func, a, [])

    def test_matrix_equality(self):
        # Check that matrix equality rules are correct
        a = Matrix(self._A_2x2)
        b = Matrix(self._B_2x2)
        c = Matrix([[1, 3], [5, 7]])
        d = Matrix(self._A_3x3)

        self.assertTrue(a != b)
        self.assertTrue(a == c)
        self.assertFalse(a == d)
        self.assertFalse(c == d)

    # ===============================================================
    # Tests for Etivity 4 based on persons code from etivity 3
    #
    # Requirements from SULIS:
    #   - Sum of a 4x4 with a 4x4 matrix
    #   - Multiplication of a 4x4 with a 4x4 matrix
    #   - Multiplication of a 4x4 matrix with a suitable vector
    #   - Determinant of a 2x2 matrix
    #   - Inverse of a 2x2 matrix
    #   - Cross-product of 2 suitable tensors

    def test_sum_4_by_4_matrix(self):
        a = Matrix([[2, 3, 2, 9], [8, 3, 1, 7], [4, 1, 9, 5], [2, 4, 0, 9]])
        b = Matrix([[2, 3, 5, 2], [1, 9, 1, 7], [6, 3, 9, 4], [5, 2, 4, 7]])
        expected_result = Matrix([[4, 6, 7, 11], [9, 12, 2, 14], [10, 4, 18, 9], [7, 6, 4, 16]])

        result = a + b

        self.assertEqual(result, expected_result)

    def test_multiply_4_by_4_matrix(self):
        a = Matrix([[2, 3, 2, 9], [8, 3, 1, 7], [4, 1, 9, 5], [2, 4, 0, 9]])
        b = Matrix([[2, 3, 5, 2], [1, 9, 1, 7], [6, 3, 9, 4], [5, 2, 4, 7]])
        expected_result = Matrix([[64, 57, 67, 96], [60, 68, 80, 90], [88, 58, 122, 86], [53, 60, 50, 95]])

        result = a @ b

        self.assertEqual(result, expected_result)

    def test_scalar_multiplication_4_by_4(self):
        a = Matrix([[2, 3, 2, 9], [8, 3, 1, 7], [4, 1, 9, 5], [2, 4, 0, 9]])
        v = Matrix([[2], [1], [6], [5]])
        expected_result = Matrix([[64], [60], [88], [53]])

        result = a @ v

        self.assertEqual(result, expected_result)

    def test_matrix_determinent(self):
        a = Matrix(self._A_2x2)
        det_a = a._determinant()
        expected_det = -8
        self.assertEqual(expected_det, det_a)

    def test_matrix_inverse(self):
        c = Matrix(self._C_2x2)
        inverse_c = c._inverse()
        expected_inverse = Matrix([(0.6, -0.7), (-0.2, 0.4)])

        self.assertEqual(expected_inverse, inverse_c)

    def test_matrix_cross_product(self):
        vector_e = Matrix(self._E_vector)
        vector_f = Matrix(self._F_vector)
        expected_cross_product = Matrix(([-1], [-4], [3]))
        actual_cross_product = vector_e._cross_product(vector_f)

        self.assertEqual(expected_cross_product, actual_cross_product)
