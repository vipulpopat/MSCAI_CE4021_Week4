"""
Code for Etivity-4
"""
class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.debug = False


    def set_debug(self, debug):
        self.debug = debug
        

    def log(self, message):
        if self.debug:
            print(message)
            
            
    def get_matrix(self):
        return self.matrix;
    

    def get(self, row, column):
        return self.matrix[row][column]
    
        
    def get_size(self):
        """Find the size of the matrix """
        cols = len(self.matrix[0])
        rows = len(self.matrix)
        return (rows, cols)


    def add_or_subtract_matrices(self, other_matrix, operation):
        """Add or subtract matrices depending on value of operation parameter
        """
        nb_rows, nb_cols = self.get_size()
        self.initialise_matrix(nb_rows, nb_cols)
        
        # check if matrices are the same shape
        if self.get_size() == other_matrix.get_size():
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    if operation == 'add':
                        self.result[i][j] =  self.matrix[i][j] + other_matrix.get(i,j)
                    elif operation == 'subtract':
                        self.result[i][j] =  self.matrix[i][j] - other_matrix.get(i,j)
        return self.result

        
    def multiply_matrices(self, other_matrix):
        """Multiply a matrix by a matrix or a vector"""
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

    
    def determinant(self):
        """ Calculate the determinant of a 2x2 matrix 
        
        Whereby:
        
        det([[a, c], 
             [b, d]])=ad−bc.
        """
        
        rows, cols = self.get_size()
        if rows == 2 and cols == 2:
            self.log("Calculating determinant for matrix:{}".format(self.matrix))
            return (self.matrix[0][0]*self.matrix[1][1]-self.matrix[1][0]*self.matrix[0][1])
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
        self.initialise_matrix(cols, rows)
        if rows == 2 and cols == 2:
            self.log("Calculating inverse of matrix:{}".format(self.matrix))
            self.result[0][0] = self.matrix[1][1]
            self.result[0][1] = 0 - self.matrix[0][1]
            self.result[1][0] = 0 - self.matrix[1][0]
            self.result[1][1] = self.matrix[0][0]
            
            return (1/self.determinant(), self.result)
        else:
            raise ValueError('Only 2x2 matrices are supported for now.')

    
        
    def initialise_matrix(self, num_cols, num_rows):
        """ Initialise an empty matrix.
        """
        self.result = [[0 for x in range(num_cols)] 
                        for y in range(num_rows)]
        return self.result



# TESTS
def tests():

    m1 = [[2,3],
          [4,5]]
    m2 = [[6,7],
          [8,9]]
    m3 = [[1,5,2,3],
          [3,2,6,5],
          [6,1,4,1],
          [4,3,1,2]]
    m4 = [[2,1,4,5],
          [3,5,1,3],
          [6,3,2,1],
          [1,4,6,4]]
    
    M1 = Matrix(m1)
    M2 = Matrix(m2)
    M3 = Matrix(m3)
    M4 = Matrix(m4)
    
    # Ensure methods are working as expected
    print("M1 matrix  :{}".format(M1.get_matrix()))
    print("M1 size    :{}".format(M1.get_size()))
    print("M1 get(1,1):{}".format(M1.get(1,1)))
    print("M1 det     :{}".format(M1.determinant()))
    print("M1 inverse :{}".format(M1.inverse()))
    print("")
    print("M1 matrix  :{}".format(M1.get_matrix()))
    print("M2 matrix  :{}".format(M2.get_matrix()))
    print("M1 + M2    :{}".format(M1.add_or_subtract_matrices(M2,'add')))
    print("M1 - M2    :{}".format(M1.add_or_subtract_matrices(M2,'subtract')))
    print("M1 * M2    :{}".format(M1.multiply_matrices(M2)))
    
    
    
#    print(add_or_subtract_matrices(m1, m2, 'add'))
 #   print(add_or_subtract_matrices(m1, m2, 'subtract'))
  #  print(multiply_matrices(m1, m2))
   # print(multiply_matrices(m3, m4))    
    #print(determinant(m1))
    #print(inverse(m1))


tests()