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
        """ Calculate the dot product between this 3x1 vector and another one.

        This link provides a very consise definition of the dot product.
        http://www.math.pitt.edu/~sparling/23012/*vectors5/node19.html

        """

        if (self.get_nb_cols() == other.get_nb_cols()) and (self.get_nb_cols() == 1) and (self.get_nb_rows() == 3):
            self.initialise_result_matrix(1, 3)
           
            self.result[0][0] = self.get(1,0)*other.get(2,0)-self.get(2,0)*other.get(1,0)
            self.result[1][0] = self.get(2,0)*other.get(0,0)-self.get(0,0)*other.get(2,0)
            self.result[2][0] = self.get(0,0)*other.get(1,0)-self.get(1,0)*other.get(0,0)            

            return self.result        

        else:
            raise ValueError('Only 3x1 vectors are supported for now.')


    def initialise_result_matrix(self, num_cols, num_rows):
        """ Initialise an empty matrix. """
        self.result = [[0 for x in range(num_cols)]
                        for y in range(num_rows)]
        return self.result


# TESTS
def tests():

    m1 = [[2, 3],
          [4, 5]]

    m3 = [[1, 5, 2, 3],
          [3, 2, 6, 5],
          [6, 1, 4, 1],
          [4, 3, 1, 2]]

    m4 = [[2, 1, 4, 5],
          [3, 5, 1, 3],
          [6, 3, 2, 1],
          [1, 4, 6, 4]]


    M1 = Matrix(m1)
    M3 = Matrix(m3)
    M4 = Matrix(m4)

    # Ensure methods are working as expected
    print("M1 matrix  :{}".format(M1.get_matrix()))
    print("M1 det     :{}".format(M1.determinant()))
    print("M1 inverse :{}".format(M1.inverse()))

    assert M1.determinant() == -2
    assert M1.inverse() == (-0.5, [[5, -3], [-4, 2]])

    print("")
    print("M3 matrix  :{}".format(M3.get_matrix()))
    print("M4 matrix  :{}".format(M4.get_matrix()))
    print("M3 + M4    :{}".format(M3.add_or_subtract_matrices(M4, 'add')))
    print("M3 - M4    :{}".format(M3.add_or_subtract_matrices(M4, 'subtract')))
    print("M3 * M4    :{}".format(M3.multiply_matrices(M4)))

    assert M3.add_or_subtract_matrices(M4, 'add') == [[3, 6, 6, 8], [6, 7, 7, 8], [12, 4, 6, 2], [5, 7, 7, 6]]
    assert M3.add_or_subtract_matrices(M4, 'subtract') == [[-1, 4, -2, -2], [0, -3, 5, 2], [0, -2, 2, 0], [3, -1, -5, -2]]
    assert M3.multiply_matrices(M4) == ((32, 44, 31, 34), (53, 51, 56, 47), (40, 27, 39, 41), (25, 30, 33, 38))

    v = [[1], [2], [3]]
    w = [[4], [5], [6]]
    V = Matrix(v)
    W = Matrix(w)
    
    print("")
    print("V          :{}".format(V.get_matrix()))
    print("W          :{}".format(W.get_matrix()))
    print("V X W      :{}".format(V.cross_product(W)))
    
    assert V.cross_product(W) == [[-3], [6], [-3]]

tests()
