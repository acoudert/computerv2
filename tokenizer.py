import string
from customExceptions import *
from matrix import *

class Token:

    def __init__(self, type, float=0, imaginary={}, 
            matrix=None, name=None, binop=None, 
            ft_tree=None, ft_var_name=None,
            xpower={}):
        self.type = type
        self.float = float
        self.imaginary = imaginary
        self.matrix = matrix
        self.xpower = xpower
        self.name = name
        self.binop = binop

    def __str__(self):
        if self.type == "matrix":
            return str(self.matrix)
        self.s = ""
        self.s += self.__floatStr()
        self.s += self.__imaginaryStr()
        self.s += self.__xpowerStr()
        return self.s

    def __floatStr(self):
        if self.float == 0:
            if not self.imaginary or all([coef == 0 for coef in self.imaginary.values()]):
                if not self.matrix:
                    return self.__getStrFromFloatInt(self.float)
            return ""
        return self.__getStrFromFloatInt(self.float)

    def __imaginaryStr(self):
        s = ""
        for p, coef in self.imaginary.items():
            if coef == 0:
                continue
            if abs(coef) != 1:
                s += self.__getStrFromFloatInt(coef)
            elif coef == 1 and self.s:
                s += "+ "
            elif coef == -1:
                s += "- "
            s += "i "
            if p != 1:
                s += "^ "
                s += self.__getStrFromFloatInt(p) if p > 0 else "(" + self.__getStrFromFloatInt(p)[:-1] + ")"
                s += " "
        return s
    
    def __xpowerStr(self):
        s = ""
        for p, coef in self.xpower.items():
            if coef == 0:
                continue
            if abs(coef) != 1:
                s += self.__getStrFromFloatInt(coef)
            elif coef == 1 and self.s:
                s += "+ "
            elif coef == -1:
                s += "- "
            s += "x "
            if p != 1:
                s += "^ "
                if p > 0:
                    s += str(p)
                else:
                    s += "( " + self.__getStrFromFloatInt(p) + ")"
                s += " "
        return s

    def __getStrFromFloatInt(self, v):
        v = float(v)
        if v < 0:
            return "- " + str(abs(int(v)) if v.is_integer() else abs(v)) + " "
        elif self.s:
            return "+ " + str(int(v) if v.is_integer() else v) + " "
        return str(int(v) if v.is_integer() else v) + " "


class Tokenizer:
    
    OPERATORS = "*+-/%^()=?"

    def __init__(self, expression):
        self.expression = expression.replace(' ', '').lower()
        self.__updateExpression()
        self.i = 0
        self.char = self.expression[self.i]

    def __updateExpression(self):
        i = 0
        while i + 1 < len(self.expression):
            if self.expression[i].isdigit():
                if self.expression[i+1] in string.ascii_lowercase:
                    self.expression = self.expression[:i+1] + "*" + self.expression[i+1:]
            if self.expression[i] in string.ascii_lowercase:
                if self.expression[i+1].isdigit():
                    self.expression = self.expression[:i+1] + "*" + self.expression[i+1:]
            i += 1

    def extractToken(self):
        while self.char:
            if self.char in Tokenizer.OPERATORS:
                return self.__extractOperator()
            elif self.char.isdigit():
                return self.__extractFloat()
            elif self.char == "[":
                return self.__extractMatrix()
            elif self.char in string.ascii_lowercase:
                return self.__extractAscii()
            raise UnknownCharacter
        return Token("EOF")


    # PRIVATE

    def __extractOperator(self):
        curr_char = self.char
        self.__advance()
        if curr_char in Tokenizer.OPERATORS[1:] or self.char != "*":
            return Token(curr_char, binop=curr_char)
        self.__advance()
        return Token("**", binop="**")

    def __extractFloat(self):
        value_str = ""
        while self.char and self.char.isdigit():
            value_str += self.char
            self.__advance()
            if self.char == '.':
                if value_str.count('.') != 0:
                    raise InvalidFloat
                value_str += self.char
                self.__advance()
                if not self.char or not self.char.isdigit():
                    raise InvalidFloat
        return Token("num", float=float(value_str))

    def __extractMatrix(self):
        depth = 1
        matrix_str = self.char
        self.__advance()
        while self.char and depth > 0:
            if self.char == "[":
                depth += 1
            elif self.char == "]":
                depth -= 1
            matrix_str += self.char
            self.__advance()
        matrix_str = matrix_str.replace(";", ",")
        try:
            return Token("matrix", matrix=Matrix(matrix_str=matrix_str))
        except:
            raise InvalidMatrix

    def __extractAscii(self):
        value = ""
        while self.char and self.char in string.ascii_lowercase:
            value += self.char
            self.__advance()
        if value == "i":
            return Token("num", imaginary={0:0, 1:1})
        elif self.char == "(":
            self.__advance()
            return Token("function", name=value)
        else:
            return Token("variable", name=value)

    def __advance(self):
        self.i += 1
        self.char = self.expression[self.i] if self.i < len(self.expression) else None
