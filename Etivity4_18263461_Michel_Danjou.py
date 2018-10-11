"""
Code for Etivity-4
"""
class Matrix:
    """ This class provides matrix operations such as:
        addition, substraction, multiplication,
        determinant, inverse, dot product.
    """

    def __init__(self, matrix):
        """ init """
        self.matrix = matrix
        self.debug = False


    def set_debug(self, debug):
        """ Progrmmatically turn on debug logging. """
        self.debug = debug


    def log(self, message):
        """ Print a message on screen when debug is turned on. """
        if self.debug:
            print(message)


    def get_matrix(self):
        """ Return the underlying matrix. """
        return self.matrix


    def get(self, row, column):
        """ Return a cell from the matrix for the given row, column. """
        return self.matrix[row][column]


    def get_size(self):
        """Return a tuple describing the size of the matrix. """
        try:
            cols = len(self.matrix[0])
            rows = len(self.matrix)
            return (rows, cols)

        except:
            raise ValueError('Invalid matrix:{}'.format(self.matrix))

    def get_nb_rows(self):
        """ Return the number of rows of a the encapsulated 2D array. """
        return self.get_size()[0]


    def get_nb_cols(self):
        """ Return the number of columns of the underlying 2D array. """
        return self.get_size()[1]

    def add(self, other_matrix, operation):
        """ Perform addition. Delegate work to Gerry's original method """
        return self.__add_or_subtract_matrices__(other_matrix, "add")


    def subtract(self, other_matrix, operation):
        """ Perform Subtraction. Delegate work to Gerry's original method """
        return self.__add_or_subtract_matrices__(other_matrix, "subtract")

    def __add_or_subtract_matrices__(self, other_matrix, operation):
        """ Perform addition or substraction of this matrix with another. """
        nb_rows, nb_cols = self.get_size()
        self.__initialise_result_matrix__(nb_rows, nb_cols)

        # check if matrices are the same shape
        if self.get_size() == other_matrix.get_size():
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    if operation == 'add':
                        self.result[i][j] = self.matrix[i][j] + other_matrix.get(i, j)
                    elif operation == 'subtract':
                        self.result[i][j] = self.matrix[i][j] - other_matrix.get(i, j)
            return Matrix(self.result)
        else:
            raise ValueError('Matrices not compatible with addition/substraction.')



    def multiply(self, other_matrix):
        """Multiply a matrix by another matrix or a vector. """
        # Check if row number of matrix 1 equals col number of matrix 2
        if self.get_size()[1] == other_matrix.get_size()[0]:
            product = []
            for i in range(len(self.matrix)):
                i_matrix = []
                for j in range(len(other_matrix.get_matrix()[0])):
                    jk_matrix = 0
                    for k in range(len(other_matrix.get_matrix())):
                        jk_matrix += self.matrix[i][k] * other_matrix.get(k, j)
                    i_matrix.append(jk_matrix)
                product.append(tuple(i_matrix))
            return Matrix(product)
        else:
            raise ValueError('Matrices not compatible with multiplication.')



    def determinant(self):
        """ Calculate the determinant of a 2x2 matrix

        Where:

        det([[a, c],
             [b, d]])=ad−bc.
        """

        rows, cols = self.get_size()
        if rows == 2 and cols == 2:
            self.log("Calculating determinant for matrix:{}".format(self.matrix))
            return self.matrix[0][0]*self.matrix[1][1]-self.matrix[1][0]*self.matrix[0][1]
        else:
            raise ValueError('Only 2x2 matrices are supported for now.')


    def inverse(self):
        """ Calculate the inverse of a 2x2 matrix

        Considering matrix M where
        M=[[a, c],
           [b, d]]

        inverse(M)=1/det(M) * [[d, -c],
                               [-b,a]]
        """
        rows, cols = self.get_size()
        self.__initialise_result_matrix__(cols, rows)

        det = self.determinant()
        if det == 0:
            return None

        if rows == 2 and cols == 2:
            self.log("Calculating inverse of matrix:{}".format(self.matrix))
            self.result[0][0] = self.matrix[1][1] / det
            self.result[0][1] = (0 - self.matrix[0][1]) / det
            self.result[1][0] = (0 - self.matrix[1][0]) / det
            self.result[1][1] = self.matrix[0][0] /  det

            return Matrix(self.result)
        else:
            raise ValueError('Only 2x2 matrices are supported for now.')


    def cross_product(self, other):
        """ Calculate the dot product between this 3x1 vector and another one.

        This link provides a very consise definition of the dot product.
        http://www.math.pitt.edu/~sparling/23012/*vectors5/node19.html

        """

        if (self.get_nb_cols() == other.get_nb_cols()) and (self.get_nb_cols() == 1) and (self.get_nb_rows() == 3):
            self.__initialise_result_matrix__(1, 3)

            self.result[0][0] = self.get(1, 0)*other.get(2, 0)-self.get(2, 0)*other.get(1, 0)
            self.result[1][0] = self.get(2, 0)*other.get(0, 0)-self.get(0, 0)*other.get(2, 0)
            self.result[2][0] = self.get(0, 0)*other.get(1, 0)-self.get(1, 0)*other.get(0, 0)

            return Matrix(self.result)

        else:
            raise ValueError('Only 3x1 vectors are supported for now.')


    def __initialise_result_matrix__(self, num_cols, num_rows):
        """ Initialise an empty matrix. """
        self.result = [[0 for x in range(num_cols)]
                        for y in range(num_rows)]
        return self.result


    def __compare_floats__(self, left_float, right_float):
        """ Return True if 2 floats are identical (reusing code from Etivity-1) """
        return abs(left_float - right_float) < 0.01


    def equals(self, other):
        """ Compare a matrix with another """

        if self.get_size() != other.get_size():
            return False

        for row in range(self.get_nb_rows()):
            for col in range(self.get_nb_cols()):
                if not self.__compare_floats__(self.matrix[row][col], other.matrix[row][col]):
                    return False

        return True

# TESTS
def tests():
    """ Test suite """
    m_0 = [[1, 1],
          [1, 1]]

    m_1 = [[2, 3],
          [4, 5]]

    m_3 = [[1, 5, 2, 3],
          [3, 2, 6, 5],
          [6, 1, 4, 1],
          [4, 3, 1, 2]]

    m_4 = [[2, 1, 4, 5],
          [3, 5, 1, 3],
          [6, 3, 2, 1],
          [1, 4, 6, 4]]


    M_0 = Matrix(m_0)
    M_1 = Matrix(m_1)
    M_3 = Matrix(m_3)
    M_4 = Matrix(m_4)

    # Ensure methods are working as expected
    print("M_0 matrix  :{}".format(M_0.get_matrix()))
    print("M_0 det     :{}".format(M_0.determinant()))
    print("M_0 inverse :{}".format(M_0.inverse()))

    assert M_0.determinant() == 0
    assert M_0.inverse() == None
    print("")

    print("M_1 matrix  :{}".format(M_1.get_matrix()))
    print("M_1 det     :{}".format(M_1.determinant()))
    print("M_1 inverse :{}".format(M_1.inverse().get_matrix()))

    assert M_1.determinant() == -2
    assert M_1.inverse().equals(Matrix([[-2.5, 1.5], [2, -1]]))

    print("")
    print("M_3 matrix   :{}".format(M_3.get_matrix()))
    print("M_4 matrix   :{}".format(M_4.get_matrix()))
    print("M_3 + M_4    :{}".format(M_3.add(M_4, 'add').get_matrix()))
    print("M_3 - M_4    :{}".format(M_3.subtract(M_4, 'subtract').get_matrix()))
    print("M_3 * M_4    :{}".format(M_3.multiply(M_4).get_matrix()))

    assert M_3.add(M_4, 'add').equals(Matrix([[3, 6, 6, 8], [6, 7, 7, 8], [12, 4, 6, 2], [5, 7, 7, 6]]))
    assert M_3.subtract(M_4, 'subtract').equals(Matrix([[-1, 4, -2, -2], [0, -3, 5, 2], [0, -2, 2, 0], [3, -1, -5, -2]]))
    assert M_3.multiply(M_4).equals(Matrix([[32, 44, 31, 34], [53, 51, 56, 47], [40, 27, 39, 41], [25, 30, 33, 38]]))


    v = [[1], [2], [3]]
    w = [[4], [5], [6]]
    V = Matrix(v)
    W = Matrix(w)

    print("")
    print("V          :{}".format(V.get_matrix()))
    print("W          :{}".format(W.get_matrix()))
    print("V X W      :{}".format(V.cross_product(W).get_matrix()))

    assert V.cross_product(W).equals(Matrix([[-3], [6], [-3]]))

tests()
