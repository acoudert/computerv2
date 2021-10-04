import copy
from tokenizer import Token
from customExceptions import *
from sys import exit

class BinOp:
    def __init__(self, left, token, right, in_parenthesis=False):
        self.left = left
        self.token = token
        self.right = right
        self.in_parenthesis = in_parenthesis

    def __str__(self):
        return "BinOp: " + self.token.binop

class Function:
    def __init__(self, left, token, right, in_parenthesis=False):
        self.left = left
        self.token = token
        self.right = right
        self.in_parenthesis = in_parenthesis
    
    def __str__(self):
        return "Function: " + self.token.name

class Variable:
    def __init__(self, token, in_parenthesis=False):
        self.left = None
        self.token = token
        self.right = None
        self.in_parenthesis = in_parenthesis
    
    def __str__(self):
        return "Variable: " + self.token.name

class Parenthesis:
    def __init__(self, left, token, right, in_parenthesis=False):
        self.left = left
        self.token = token
        self.right = right
        self.in_parenthesis = in_parenthesis
    
    def __str__(self):
        return "Parenthesis: " + self.token.binop

class Num:
    def __init__(self, token, in_parenthesis=False):
        self.left = None
        self.token = token
        self.right = None
        self.in_parenthesis = in_parenthesis

    def __str__(self):
        return "Num: " + str(self.token)

    @staticmethod
    def updateFloatImaginary(float, imaginary):
        if 0 in imaginary.keys():
            float += imaginary[0]
            imaginary[0] = 0
        for k in imaginary.keys():
            if k > 0 and k % 2 == 0:
                float += imaginary[k] if k % 4 == 0 else (-1) * imaginary[k]
                imaginary[k] = 0
        return float

    @staticmethod
    def updateFloatXPower(float, xpower):
        if 0 in xpower.keys():
            float += xpower[0]
            xpower[0] = 0
        return float

    def __add__(self, other):
        if self.token.type != other.token.type:
            raise InvalidOperation
        if self.token.type == "matrix":
            matrix = self.token.matrix + other.token.matrix
            return Num(Token("matrix", matrix=matrix), in_parenthesis=self.in_parenthesis)
        float = self.token.float + other.token.float
        imaginary = {p: 0 for p in self.token.imaginary.keys()}
        for p in other.token.imaginary.keys():
            imaginary[p] = 0
        for p in imaginary.keys():
            if p in self.token.imaginary.keys():
                imaginary[p] += self.token.imaginary[p]
            if p in other.token.imaginary.keys():
                imaginary[p] += other.token.imaginary[p]
        xpower = {p: 0 for p in self.token.xpower.keys()}
        for p in other.token.xpower.keys():
            xpower[p] = 0
        for p in xpower.keys():
            if p in self.token.xpower.keys():
                xpower[p] += self.token.xpower[p]
            if p in other.token.xpower.keys():
                xpower[p] += other.token.xpower[p]
        return Num(Token("num", float=float, imaginary=imaginary, xpower=xpower), in_parenthesis=self.in_parenthesis)

    def __sub__(self, other):
        if self.token.type != other.token.type:
            raise InvalidOperation
        if self.token.type == "matrix":
            matrix = self.token.matrix - other.token.matrix
            return Num(Token("matrix", matrix=matrix), in_parenthesis=self.in_parenthesis)
        float = self.token.float - other.token.float
        imaginary = {p: 0 for p in self.token.imaginary.keys()}
        for p in other.token.imaginary.keys():
            imaginary[p] = 0
        for p in imaginary.keys():
            if p in self.token.imaginary.keys():
                imaginary[p] += self.token.imaginary[p]
            if p in other.token.imaginary.keys():
                imaginary[p] -= other.token.imaginary[p]
        xpower = {p: 0 for p in self.token.xpower.keys()}
        for p in other.token.xpower.keys():
            xpower[p] = 0
        for p in xpower.keys():
            if p in self.token.xpower.keys():
                xpower[p] += self.token.xpower[p]
            if p in other.token.xpower.keys():
                xpower[p] -= other.token.xpower[p]
        return Num(Token("num", float=float, imaginary=imaginary, xpower=xpower), in_parenthesis=self.in_parenthesis)
    
    def __mul__(self, other):
        if self.token.type == "matrix" or other.token.type == "matrix":
            if self.token.type == "matrix" and other.token.type == "matrix":
                matrix = self.token.matrix * other.token.matrix
            elif self.token.type == "matrix":
                matrix = self.token.matrix.mulNum(other.token)
            else:
                matrix = other.token.matrix.mulNum(self.token)
            return Num(Token("matrix", matrix=matrix), in_parenthesis=self.in_parenthesis)
        float = 0
        imaginary = {}
        xpower = {}
        float1 = ("float", self.token.float)
        xpower1 = ("xpower", self.token.xpower)
        imaginary1 = ("imaginary", self.token.imaginary)
        float2 = ("float", other.token.float)
        imaginary2 = ("imaginary", other.token.imaginary)
        xpower2 = ("xpower", other.token.xpower)
        for v1 in (float1, imaginary1, xpower1):
            if not v1[1]:
                continue
            for v2 in (float2, imaginary2, xpower2):
                if not v2[1]:
                    continue
                if v1[0] == "float":
                    if v2[0] == "float":
                        float += v1[1] * v2[1]
                    elif v2[0] == "imaginary":
                        temp_imaginary = {p: v1[1] * i for p, i in v2[1].items()}
                        for p, i in temp_imaginary.items():
                            if p not in imaginary.keys():
                                imaginary[p] = 0
                            imaginary[p] += temp_imaginary[p]
                    elif v2[0] == "xpower":
                        temp_xpower = {p: v1[1] * i for p, i in v2[1].items()}
                        for p, i in temp_xpower.items():
                            if p not in xpower.keys():
                                xpower[p] = 0
                            xpower[p] += temp_xpower[p]
                elif v1[0] == "imaginary":
                    if v2[0] == "float":
                        temp_imaginary = {p: i * v2[1] for p, i in v1[1].items()}
                        for p, i in temp_imaginary.items():
                            if p not in imaginary.keys():
                                imaginary[p] = 0
                            imaginary[p] += temp_imaginary[p]
                    elif v2[0] == "imaginary":
                        for p1 in v1[1].keys():
                            for p2 in v2[1].keys():
                                if p1 + p2 not in imaginary.keys():
                                    imaginary[p1 + p2] = 0
                                imaginary[p1 + p2] += v1[1][p1] * v2[1][p2]
                        float = Num.updateFloatImaginary(float, imaginary)
                    elif v2[0] == "xpower":
                        raise InvalidOperation
                elif v1[0] == "xpower":
                    if v2[0] == "float":
                        temp_xpower = {p: i * v2[1] for p, i in v1[1].items()}
                        for p, i in temp_xpower.items():
                            if p not in xpower.keys():
                                xpower[p] = 0
                            xpower[p] += temp_xpower[p]
                    elif v2[0] == "imaginary":
                        raise InvalidOperation
                    elif v2[0] == "xpower":
                        for p1 in v1[1].keys():
                            for p2 in v2[1].keys():
                                if p1 + p2 not in xpower.keys():
                                    xpower[p1 + p2] = 0
                                xpower[p1 + p2] += v1[1][p1] * v2[1][p2]
                        float = Num.updateFloatXPower(float, xpower)
        return Num(Token("num", float=float, imaginary=imaginary, xpower=xpower), in_parenthesis=self.in_parenthesis)

    def __truediv__(self, other):
        if other.token.type == "matrix":
            raise InverseMatrix
        if self.token.type == "matrix":
            matrix = self.token.matrix / other.token
            return Num(Token("matrix", matrix=matrix), in_parenthesis=self.in_parenthesis)
        float = 0
        imaginary = {}
        xpower = {}
        denominator_types = self.__numTypes(other)
        if len(denominator_types) != 1:
            raise InvalidOperation
        denom_type = denominator_types[0]
        float1 = ("float", self.token.float)
        imaginary1 = ("imaginary", self.token.imaginary)
        xpower1 = ("xpower", self.token.xpower)
        for v1 in (float1, imaginary1, xpower1):
            if not v1[1] and v1[1] != 0:
                continue
            if v1[0] == "float":
                if denom_type == "float":
                    if other.token.float == 0:
                        raise InvalidOperation
                    float += v1[1] / other.token.float
                elif denom_type == "imaginary":
                    p = [*{p: i for p, i in other.token.imaginary.items() if i != 0}.keys()][0]
                    if -p not in imaginary:
                        imaginary[-p] = 0
                    imaginary[-p] += v1[1] / other.token.imaginary[p]
                elif denom_type == "xpower":
                    p = [*{p: i for p, i in other.token.xpower.items() if i != 0}.keys()][0]
                    if -p not in xpower:
                        xpower[-p] = 0
                    xpower[-p] += v1[1] / other.token.xpower[p]
            elif v1[0] == "imaginary":
                if denom_type == "float":
                    for p, i in v1[1].items():
                        if p not in imaginary.keys():
                            imaginary[p] = 0
                        imaginary[p] += v1[1][p] / other.token.float
                elif denom_type == "imaginary":
                    p2 = [*{p: i for p, i in other.token.imaginary.items() if i != 0}.keys()][0]
                    i2 = other.token.imaginary[p2]
                    for p, i in v1[1].items():
                        if p - p2 not in imaginary:
                            imaginary[p - p2] = 0
                        imaginary[p - p2] = i / i2
                    float = Num.updateFloatImaginary(float, imaginary)
                elif denom_type == "xpower":
                    raise InvalidOperation
            elif v1[0] == "xpower":
                if denom_type == "float":
                    for p, i in v1[1].items():
                        if p not in xpower.keys():
                            xpower[p] = 0
                        xpower[p] += v1[1][p] / other.token.float
                elif denom_type == "imaginary":
                    raise InvalidOperation
                elif denom_type == "xpower":
                    p2 = [*{p: i for p, i in other.token.xpower.items() if i != 0}.keys()][0]
                    i2 = other.token.xpower[p2]
                    for p, i in v1[1].items():
                        if p - p2 not in xpower:
                            xpower[p - p2] = 0
                        xpower[p - p2] += i / i2
                    float = Num.updateFloatXPower(float, xpower)
        return Num(Token("num", float=float, imaginary=imaginary, xpower=xpower), in_parenthesis=self.in_parenthesis)

    def __mod__(self, other):
        if other.token.type == "matrix":
            raise InvalidOperation
        if self.token.type == "matrix":
            matrix = self.token.matrix % other.token
            return Num(Token("matrix", matrix=matrix), in_parenthesis=self.in_parenthesis)
        float = 0
        imaginary = {}
        xpower = {}
        denominator_types = self.__numTypes(other)
        if len(denominator_types) != 1:
            raise InvalidOperation
        denom_type = denominator_types[0]
        float1 = ("float", self.token.float)
        imaginary1 = ("imaginary", self.token.imaginary)
        xpower1 = ("xpower", self.token.imaginary)
        for v1 in (float1, imaginary1):
            if not v1[1] and v1[1] != 0:
                continue
            if v1[0] == "float":
                if denom_type == "float":
                    if other.token.float == 0:
                        raise InvalidOperation
                    float += v1[1] % other.token.float
                elif denom_type == "imaginary":
                    raise InvalidOperation
                elif denom_type == "xpower":
                    raise InvalidOperation
            elif v1[0] == "imaginary":
                raise InvalidOperation
            elif v1[0] == "xpower":
                raise InvalidOperation
        return Num(Token("num", float=float, imaginary=imaginary, xpower=xpower), in_parenthesis=self.in_parenthesis)

    def __xor__(self, other):
        if other.token.type == "matrix":
            raise InvalidOperation
        if self.token.type == "matrix":
            matrix = self.token.matrix ^ other.token
            return Num(Token("matrix", matrix=matrix), in_parenthesis=self.in_parenthesis)
        float = self.token.float
        imaginary = self.token.imaginary
        xpower = self.token.xpower
        denominator_types = self.__numTypes(other)
        if len(denominator_types) != 1:
            raise InvalidOperation
        denom_type = denominator_types[0]
        if denom_type != "float" or not other.token.float.is_integer():
            if denom_type == "float":
                if other.token.float == 0.5:
                    if not any([coef > 0 for coef in xpower.values()]):
                        if not any([coef > 0 for coef in imaginary.values()]):
                            return Num(Token("num", float=float**0.5), in_parenthesis=self.in_parenthesis)
            raise InvalidOperation
        if other.token.float == 0:
            return Num(Token("num", float=1), in_parenthesis=self.in_parenthesis)
        n = Num(Token("num", float=float, imaginary=imaginary, xpower=xpower), in_parenthesis=self.in_parenthesis)
        if other.token.float > 0:
            for _ in range(1, int(other.token.float)):
                n *= self
        else:
            n1 = Num(Token("num", float=1), in_parenthesis=self.in_parenthesis)
            for _ in range(1, abs(int(other.token.float)) + 1):
                n1 /= n
            n = n1
        return n

    def __pow__(self, other):
        if self.token.type == "matrix" and other.token.type == "matrix":
            matrix = self.token.matrix ** other.token.matrix
            return Num(Token("matrix", matrix=matrix), in_parenthesis=self.in_parenthesis)
        raise InvalidOperation

    def __numTypes(self, node):
        token = node.token
        number_types = []
        if token.imaginary:
            i_number = len([i for i in token.imaginary if i != 0])
            if i_number:
                number_types.append("imaginary")
        if token.xpower:
            x_number = len([i for i in token.xpower if i != 0])
            if x_number:
                number_types.append("xpower")
        if token.float or not number_types:
            number_types.append("float")
        return number_types
