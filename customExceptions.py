class UnknownCharacter(Exception):
    def __str__(self):
        return "Expression contains an unknown character"

class InvalidFloat(Exception):
    def __str__(self):
        return "Expression contains an invalid float"

class InvalidMatrix(Exception):
    def __str__(self):
        return "Expression contains an invalid matrix"

class VectorDeclaration(Exception):
    def __str__(self):
        return "Expression contains a vector"

class InvalidExpression(Exception):
    def __str__(self):
        return "Expression is invalid"

class InvalidOperation(Exception):
    def __str__(self):
        return "Expression contains an invalid operation"

class InverseMatrix(Exception):
    def __str__(self):
        return "Expression assumes a matrix inversion"

class UnknownVariable(Exception):
    def __str__(self):
        return "Expression states an unknown variable"

class UnknownFunction(Exception):
    def __str__(self):
        return "Expression states an unknown function"

class FunctionAsVariable(Exception):
    def __str__(self):
        return "Expression states a function stored as variable"

class VariableAsFunction(Exception):
    def __str__(self):
        return "Expression states a variable stored as function"

class FunctionWithoutArg(Exception):
    def __str__(self):
        return "Expression states a function without argument"

class UnsolvableEquation(Exception):
    def __str__(self):
        return "Equation cannot be solved"
