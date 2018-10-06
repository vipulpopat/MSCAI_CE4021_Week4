"""
Code for Etivity-4
"""
class Matrix:
    def __init__(self, matrix):
        """ init """
        self.matrix = matrix
        self.debug = False


    def set_debug(self, debug):
        """ Progrommatically turn on debug logging. """
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


    def add_or_subtract_matrices(self, other_matrix, operation):
        """ Perform addition or substraction of this matrix with another. """
        nb_rows, nb_cols = self.get_size()
        self.initialise_result_matrix(nb_rows, nb_cols)

        # check if matrices are the same shape
        if self.get_size() == other_matrix.get_size():
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    if operation == 'add':
                        self.result[i][j] = self.matrix[i][j] + other_matrix.get(i, j)
                    elif operation == 'subtract':
                        self.result[i][j] = self.matrix[i][j] - other_matrix.get(i, j)
            return self.result
        else:
            raise ValueError('Matrices not compatible with addition/substraction.')



    def multiply_matrices(self, other_matrix):
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
            return tuple(product)
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
        self.initialise_result_matrix(cols, rows)
        if rows == 2 and cols == 2:
            self.log("Calculating inverse of matrix:{}".format(self.matrix))
            self.result[0][0] = self.matrix[1][1]
            self.result[0][1] = 0 - self.matrix[0][1]
            self.result[1][0] = 0 - self.matrix[1][0]
            self.result[1][1] = self.matrix[0][0]

            return (1/self.determinant(), self.result)
        else:
            raise ValueError('Only 2x2 matrices are supported for now.')


    def cross_product(self, other):
        """ Calculate the dot product between this vector and another one. """

        if (self.get_nb_cols() == other.get_nb_cols()) and (self.get_nb_cols() == 1) and (self.get_nb_rows() == 2):
            self.log("nb of cols compatible with dot product")
            self.initialise_result_matrix(2, 2)

            self.copy_column_into_result_matrix(self, 0)
            self.copy_column_into_result_matrix(other, 1)

            M_temp = Matrix(self.result)
            self.log("Matrix_temp:{}".format(M_temp.get_matrix()))

            return M_temp.determinant()

        else:
            raise ValueError('Only 2x1 vectors are supported for now.')


    def copy_column_into_result_matrix(self, column_matrix, to_col_nb):
        """ Copy the content of a column matrix into a the result matrix at the
            given column position.
        """
        nb_rows = column_matrix.get_nb_rows()
        for i in range(nb_rows):
            self.result[i][to_col_nb] = column_matrix.get(i, 0)
        self.log("result:{}".format(self.result))


    def initialise_result_matrix(self, num_cols, num_rows):
        """ Initialise an empty matrix. """
        self.result = [[0 for x in range(num_cols)]
                        for y in range(num_rows)]
        return self.result


# TESTS
def tests():

    m1 = [[2, 3],
          [4, 5]]

    m2 = [[6, 7],
          [8, 9]]

    m3 = [[1, 5, 2, 3],
          [3, 2, 6, 5],
          [6, 1, 4, 1],
          [4, 3, 1, 2]]

    m4 = [[2, 1, 4, 5],
          [3, 5, 1, 3],
          [6, 3, 2, 1],
          [1, 4, 6, 4]]

    v1 = [[1], [2]]
    v2 = [[3], [4]]

    M1 = Matrix(m1)
    M2 = Matrix(m2)
    M3 = Matrix(m3)
    M4 = Matrix(m4)
    V1 = Matrix(v1)
    V2 = Matrix(v2)

    # Ensure methods are working as expected
    print("M1 matrix  :{}".format(M1.get_matrix()))
    print("M1 det     :{}".format(M1.determinant()))
    print("M1 inverse :{}".format(M1.inverse()))

    print("")
    print("M3 matrix  :{}".format(M3.get_matrix()))
    print("M4 matrix  :{}".format(M4.get_matrix()))
    print("M3 + M4    :{}".format(M3.add_or_subtract_matrices(M4, 'add')))
    print("M3 - M4    :{}".format(M3.add_or_subtract_matrices(M4, 'subtract')))
    print("M3 * M4    :{}".format(M3.multiply_matrices(M4)))

    print("")
    print("V1         :{}".format(V1.get_matrix()))
    print("V2         :{}".format(V2.get_matrix()))
    print("V1 X V2    :{}".format(V1.cross_product(V2)))

tests()