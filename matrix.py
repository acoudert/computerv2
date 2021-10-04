from customExceptions import *
import copy

class Matrix:
    
    def __init__(self, matrix_str=None, matrix=None, matrix_shape=None):
        if not matrix_str and not matrix and not matrix_shape:
            raise InvalidMatrix
        if matrix_str:
            self.matrix = eval(matrix_str)
        elif matrix:
            self.matrix = matrix
        elif matrix_shape:
            self.matrix = self.createShape(matrix_shape, 0)
        self.shape = []
        self.__getShape(self.matrix)
        self.shape = tuple(self.shape)
        if len(self.shape) == 1:
            raise VectorDeclaration
        self.__checkShapeAndData(self.matrix, 1)

    def createShape(self, shape, n):
        matrix = []
        for i in range(shape[0]):
            matrix.append([])
            for _ in range(shape[1]):
                matrix[i].append(n)
        return matrix

    def __str__(self):
        self.s = "["
        self.__generateStr(self.matrix)
        for _ in range(self.s.count("[") - self.s.count("]")):
            self.s += "]"
        self.s += " "
        return self.s.replace("\n", "\n\t")

    def __generateStr(self, m):
        for i in range(len(m)):
            if type(m[i]) == list:
                if type(m[i][0]) == int or type(m[i][0]) == float:
                    self.s += str(m[i])
                    if i + 1 != len(m):
                        self.s += ",\n"
                else:
                    if i + 1 == len(m):
                        self.s += "],\n"
                    self.s += "["
                    self.__generateStr(m[i])

    def __getShape(self, m):
        if not m and m != 0:
            raise InvalidMatrix
        if type(m) == list:
            self.shape.append(len(m))
            self.__getShape(m[0])

    def __checkShapeAndData(self, m, shape_i):
        for i in range(len(m)):
            if type(m[i]) == list:
                if len(m[i]) != self.shape[shape_i]:
                    raise InvalidMatrix
                self.__checkShapeAndData(m[i], shape_i + 1)
            else:
                if type(m[i]) != int and type(m[i]) != float:
                    raise InvalidMatrix
                if float(m[i]).is_integer():
                    m[i] = int(m[i])

    def __add__(self, other):
        matrix = copy.deepcopy(self.matrix)
        Matrix.add(matrix, other.matrix)
        return Matrix(matrix=matrix)
    
    def __sub__(self, other):
        matrix = copy.deepcopy(self.matrix)
        Matrix.sub(matrix, other.matrix)
        return Matrix(matrix=matrix)
    
    def __mul__(self, other):
        if self.shape != other.shape:
            raise InvalidOperation
        matrix = copy.deepcopy(self.matrix)
        Matrix.mulMatrices(matrix, other.matrix)
        return Matrix(matrix=matrix)

    def mulNum(self, token):
        for i in token.imaginary.values():
            if i != 0:
                raise InvalidOperation
        for i in token.xpower.values():
            if i != 0:
                raise InvalidOperation
        matrix = copy.deepcopy(self.matrix)
        Matrix.mulRational(matrix, token.float)
        return Matrix(matrix=matrix)
    
    def __truediv__(self, token):
        if token.type != "num":
            raise InvalidOperation
        for i in token.imaginary.values():
            if i != 0:
                raise InvalidOperation
        for i in token.xpower.values():
            if i != 0:
                raise InvalidOperation
        if token.float == 0:
            raise InvalidOperation
        matrix = copy.deepcopy(self.matrix)
        Matrix.divRational(matrix, token.float)
        return Matrix(matrix=matrix)
    
    def __mod__(self, token):
        if token.type != "num":
            raise InvalidOperation
        for i in token.imaginary.values():
            if i != 0:
                raise InvalidOperation
        for i in token.xpower.values():
            if i != 0:
                raise InvalidOperation
        if token.float == 0:
            raise InvalidOperation
        matrix = copy.deepcopy(self.matrix)
        Matrix.modRational(matrix, token.float)
        return Matrix(matrix=matrix)

    def __xor__(self, token):
        if token.type != "num":
            raise InvalidOperation
        if not float(token.float).is_integer():
            raise InvalidOperation
        for i in token.imaginary.values():
            if i != 0:
                raise InvalidOperation
        for i in token.xpower.values():
            if i != 0:
                raise InvalidOperation
        matrix = copy.deepcopy(self.matrix)
        if token.float == 0:
            Matrix.pow0(matrix)
        elif token.float > 0:
            for _ in range(int(token.float)):
                Matrix.mulMatrices(matrix, self.matrix)
        else:
            raise InvalidOperation
        return Matrix(matrix=matrix)

    def __pow__(self, other):
        if len(self.shape) != len(other.shape) or len(self.shape) != 2:
            raise InvalidOperation
        if self.shape[0] != other.shape[1] or self.shape[1] != other.shape[0]:
            raise InvalidOperation
        matrix = Matrix(matrix_shape=(self.shape[0], other.shape[1]))
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                for k in range(self.shape[1]):
                    matrix.matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]
        return Matrix(matrix=matrix.matrix)

    @staticmethod
    def add(m1, m2):
        if len(m1) != len(m2):
            raise InvalidOperation
        for i in range(len(m1)):
            if type(m1[i]) == list:
                Matrix.add(m1[i], m2[i])
            else:
                m1[i] += m2[i]
    
    @staticmethod
    def sub(m1, m2):
        if len(m1) != len(m2):
            raise InvalidOperation
        for i in range(len(m1)):
            if type(m1[i]) == list:
                Matrix.sub(m1[i], m2[i])
            else:
                m1[i] -= m2[i]

    @staticmethod
    def mulMatrices(m1, m2):
        for i in range(len(m1)):
            if type(m1[i]) == list:
                Matrix.mulMatrices(m1[i], m2[i])
            else:
                m1[i] *= m2[i]

    @staticmethod
    def mulRational(m1, n):
        for i in range(len(m1)):
            if type(m1[i]) == list:
                Matrix.mulRational(m1[i], n)
            else:
                m1[i] *= n

    @staticmethod
    def divRational(m1, n):
        for i in range(len(m1)):
            if type(m1[i]) == list:
                Matrix.divRational(m1[i], n)
            else:
                m1[i] /= n

    @staticmethod
    def modRational(m1, n):
        for i in range(len(m1)):
            if type(m1[i]) == list:
                Matrix.modRational(m1[i], n)
            else:
                m1[i] %= n

    @staticmethod
    def pow0(m1):
        for i in range(len(m1)):
            if type(m1[i]) == list:
                Matrix.pow0(m1[i])
            else:
                m1[i] = 1







