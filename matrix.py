"""
Matrix class pulled from week3 repo using Mark Murnane's branch as a starting point.
"""


class Matrix(object):
    """This class represents a mathematical Matrix for use in Linear Algebra

    A matrix is a rectangular structure of m x n elements, where m is the number of columns in the matrix and n is the number of rows.
    N.B. All rows of the matrix must be of equal size.

    """

    _ROWS = 0
    _COLS = 1

    def __init__(self, element_data):
        """Creates a new instance of a Matrix.

        Args:
            element_data[[row_data]+]    A list/tuple containing other 1 or more lists/tuples representing each row of the matrix.  Each row must be the same length.

        Return:
            Matrix  Instance of the Matrix class, or None if the element_data is not valid.

        Raises:
            TypeError        If no parameters are provided or the list is empty
            ValueError       If the elements are not all numberic, or the rows are not the same length
        """

        # If element data is (neither a list or tuple) or is empty return an error
        if not (isinstance(element_data, list) or isinstance(element_data, tuple)) or not element_data:
            raise TypeError("Invalid/no parameters .")

        # Then make sure the list does actually contain some other non-empty lists
        elif not all(element_data):
            raise ValueError("Element data is incomplete.  Some rows are empty.")

        # Check that the rows are the same legnthlist elements are actually numbers
        else:
            for row in element_data:
                if not (isinstance(row, list) or isinstance(row, tuple)):
                    raise TypeError(f"Row is not a valid input type {row}")

                row_length = len(element_data[0])
                if len(row) != row_length:
                    raise ValueError("Rows are not a uniform length")

                if not all(isinstance(value, int) or isinstance(value, float) for value in row):
                    raise ValueError(f"Element data contains non-numeric data in row {row}")

        # By definition a matrix has a fixed number of rows and columns.
        # The order/dimensions is the number of rows and all rows will contain the same number of columns as the first row
        self.order = (len(element_data), len(element_data[0]))
        self.elements = tuple(tuple(row) for row in element_data)

    def get_order(self):
        """Returns a tuple with the order of the matrix, i.e. (rows x columns)."""
        return self.order

    def __str__(self):
        mat_str = ''
        for row in self.elements:
            row_str = ''
            for col_val in row:
                row_str = row_str + ' ' + str(col_val) + ' '
            mat_str = mat_str + row_str + '\n'

        return mat_str

    def _is_valid_add_sub_eq_matrix(self, other):
        """Internal helper function that checks if this matrix and other are valid for equality, addition or subtraction.

        To be valid for these operations both must be matrices with the same order.
        """

        if not isinstance(other, self.__class__):
            return False

        if self.get_order() != other.get_order():
            return False

        return True

    def _is_valid_matrix_multiplier(self, other):
        """Internal helper function that checks if this matrix and other can be validly multiplied.

        To be valid the number of columns in this matrix must equal the number of rows in other.
        """

        if not isinstance(other, self.__class__):
            return False

        if self.order[Matrix._COLS] != other.order[Matrix._ROWS]:
            return False

        return True

    def __eq__(self, other):
        """Compares this matrix object to another matrix object.  Returns true if the order of the matrix is the same and the elements at each position are the same."""

        if self._is_valid_add_sub_eq_matrix(other):
            for self_row, other_row in zip(self.elements, other.elements):
                if self_row != other_row:
                    return False
            return True
        else:
            return False

    def _apply_function_to_elements(self, other, lfunc):
        """Returns a list containing the results of the function lfunc applied to rows of both self and other.  Used for simple operations like addition and subtraction.

        The function represented by lfunc is required to take two arguments, representing element values from the matrix.

        """
        return [list(map(lfunc, self_row, other_row)) for self_row, other_row in zip(self.elements, other.elements)]

    def __add__(self, other):
        """Operator overload method for the + operator.  For matrix addition the other matrix must have the same order/dimension as this matrix.

        Calls _apply_function_to_elements, passing a lambda function (lambda x, y: x + y) that takes two parameters and returns their sum.
        """

        if self._is_valid_add_sub_eq_matrix(other):
            return Matrix(self._apply_function_to_elements(other, lambda x, y: x + y))
        else:
            return NotImplemented

    def __sub__(self, other):
        """Operator overload method for the - operator.  For matrix subtraction the other matrix must have the same order/dimension as this matrix.

        Calls _apply_function_to_elements, passing a lambda function (lambda x, y: x + y) that takes two parameters and returns their difference.
        """
        if self._is_valid_add_sub_eq_matrix(other):
            return Matrix(self._apply_function_to_elements(other, lambda x, y: x - y))
        else:
            return NotImplemented

    def _scalar_multiplication(self, other):
        """Internal method to multiply this matrix by a scalar value."""
        if isinstance(other, int):
            # Scalar multiplication uses list comprehension with a map to multiply each element by the scalar
            new_elements = [list(map(lambda element: element * other, row)) for row in self.elements]
            new_matrix = Matrix(new_elements)
            return new_matrix
        else:
            return NotImplemented

    def __mul__(self, other):

        """Operator overload for the * operator.  Multiplies this matrix by a scalar value.

        Scalar multiplication of a matrix is commutative.  This method handles the case of <matrix> * <scalar>.
        """
        return self._scalar_multiplication(other)

    def __rmul__(self, other):

        """Operator overload for the * operator.  Multiplies this matrix by a scalar value.

        Scalar multiplication of a matrix is commutative.  This method handles the case of <scalar> * <matrix>.
        """
        return self._scalar_multiplication(other)

    def __matmul__(self, other):
        """Operator overload for the @ operator.  Multiplies two matrices to return the matrix product.

        For matrix multiplication the number of rows in other must match the number of columns in this matrix.
        """

        # Make sure this is a valid multiplication
        if not self._is_valid_matrix_multiplier(other):
            return NotImplemented

        new_matrix = None

        # Matrix multiplication C=AB, i.e. c = (self)(other)

        # The order/dimension of the Product matrix is the rows from
        c_order = (self.order[Matrix._ROWS], other.order[Matrix._COLS])

        # Initialise the elements array to an m*n array of 0s
        c = [[0] * c_order[Matrix._COLS] for i in range(c_order[Matrix._ROWS])]

        # For each position in the new matrix c, calculate the values from this matrix and other
        # For any C[i][k] = Sum over j of (A[i][j]*B[j][k])
        for i in range(c_order[Matrix._ROWS]):
            for k in range(c_order[Matrix._COLS]):
                #                 c[i][k] = sum(self.elements[i][j] * other.elements[j][k]) for j in range(self.order[Matrix._COLS])
                for j in range(self.order[Matrix._COLS]):
                    c[i][k] += (self.elements[i][j] * other.elements[j][k])

        new_matrix = Matrix(c)

        return new_matrix

    def _determinant(self):
        """Calculate the determinant of the matrix. Note matrix must be square and of size 2 by 2

        Returns: (int) Integer representing the determinant. Can be postive or negative
        """
        rows, cols = self.get_order()
        if rows != cols:
            raise ValueError("Matrix is not square")
        elif rows == 2 and cols == 2:
            return (self.elements[0][0] * self.elements[1][1]) - (self.elements[1][0]) * self.elements[0][1]
        else:
            # TODO Implement determinant for n by n matrix sizes
            raise NotImplementedError

    def _inverse(self):
        """Calculate the inverse of the matrix. Note only works for matrices of size 2 by 2

        Returns: The inverse matrix, can be multiplied by the orignal matrix to get an identity matrix.
        """
        determinant = self._determinant()
        if determinant == 0:
            return None

        a = self.elements[0][0] / determinant
        b = self.elements[0][1] / determinant
        c = self.elements[1][0] / determinant
        d = self.elements[1][1] / determinant

        return Matrix([(d, -b), (-c, a)])

    def _cross_product(self, vector_b):
        """Calculate the cross product for 2 vectors. Vectors must be in 3 dimensions.

        Returns: (Matrix) A new vector representing the cross product of the A X B
        """

        vector_a_rows, vector_a_cols = self.get_order()
        vector_b_rows, vector_b_cols = vector_b.get_order()

        if vector_a_rows != 3 or vector_b_rows != 3 or vector_a_cols != 1 or vector_b_cols != 1:
            raise ValueError("Error: Vectors must be in 3 dimensions")
        else:
            u1 = self.elements[0][0]
            u2 = self.elements[1][0]
            u3 = self.elements[2][0]

            v1 = vector_b.elements[0][0]
            v2 = vector_b.elements[1][0]
            v3 = vector_b.elements[2][0]

            result = ([u2 * v3 - u3 * v2], [u3 * v1 - u1 * v3], [u1 * v2 - u2 * v1])
            cross_product_matrix = Matrix(result)

        return cross_product_matrix
