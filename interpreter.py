import copy
from customExceptions import *
from customNodes import *
from tokenizer import Token
from parser import Parser
from solver import Solver

class Interpreter:

    def __init__(self, parser, variables, absolute=False, x0=-100, x1=101):
        self.parser = parser
        self.variables = variables
        self.root = self.parser.root
        self.absolute = absolute
        self.x0 = x0
        self.x1 = x1
        if self.root.token.binop != "=":
            raise InvalidExpression
        if not self.root.left or not self.root.right:
            raise InvalidExpression
        self.ft_var_assignation_name = None
        self.ft_var_calculation_node = None
        self.ft_var_calculation_name = None
        self.solving_quadratic = False
        self.s = ""
        self.n = self.assignementHandler() if self.isAssignement() else self.calculationHandler()
        if self.n:
            self.n.token.imaginary = {p: coef for p, coef in self.n.token.imaginary.items() if coef != 0}
            self.n.token.xpower = {p: coef for p, coef in self.n.token.xpower.items() if coef != 0}

    def isAssignement(self):
        return False if self.root.right.token.type == "?" else True

    def getResultStr(self):
        if not self.solving_quadratic:
            self.__getResult(self.n)
            if self.ft_var_assignation_name:
                self.variables[self.root.left.token.name]["string"] = self.s
        return self.s

    def __getResult(self, node):
        parenthesis = False
        if node:
            if node.in_parenthesis and self.ft_var_assignation_name:
                self.s += "("
            if node.token.binop:
                self.__getResult(node.left)
                self.s += node.token.binop + " "
                if node.token.binop in "*/%^":
                    for p, coef in node.right.token.imaginary.items():
                        if coef:
                            if coef < 0:
                                parenthesis = True
                            break
                    if node.right.token.float < 0:
                        parenthesis = True
                if parenthesis and not self.ft_var_assignation_name:
                    self.s += "("
                self.__getResult(node.right)
                if parenthesis and not self.ft_var_assignation_name:
                    self.s =self.s[:-1] + ") " 
            elif node.token.name:
                self.s += node.token.name + " "
            else:
                self.s += str(node.token)
            if node.in_parenthesis and self.ft_var_assignation_name:
                self.s = self.s[:-1] + ") "


##################
### ASSIGNEMENT
##################

    def assignementHandler(self):
        if not self.root.left:
            raise InvalidExpression
        var_type = type(self.root.left)
        if var_type == Variable:
            return self.__assignementVariable()
        if var_type == Function:
            return self.__assignementFunction()
        raise InvalidExpression

    def __assignementVariable(self):
        if self.root.left.left or self.root.left.right:
            raise InvalidExpression
        n = self.calculate(self.root.right)
        self.variables[self.root.left.token.name] = n
        return n

    def __assignementFunction(self):
        if self.root.left.left:
            raise InvalidExpression
        sub_node = self.root.left.right
        if type(sub_node) != Variable:
            raise InvalidExpression
        if sub_node.left or sub_node.right:
            raise InvalidExpression
        self.ft_var_assignation_name = sub_node.token.name
        n = self.calculate(self.root.right)
        self.variables[self.root.left.token.name] = {
                "var_name": self.ft_var_assignation_name,
                "tree": n,
                "string": "",
                "abs": self.absolute,
                "x0": self.x0,
                "x1": self.x1
            }
        return n


##################
### CALCULATION
##################

    def calculationHandler(self):
        return self.solveQuadratic() if self.isQuadratic() else self.calculate(self.root.left)

    def solveQuadratic(self):
        self.solving_quadratic = True
        self.ft_var_assignation_name = self.variables[self.root.left.token.name]["var_name"]
        left = self.calculate(copy.deepcopy(self.variables[self.root.left.token.name]["tree"]))
        right = self.calculate(self.root.right.left)
        solver = Solver(left, right)
        self.s = solver.solve()

    def isQuadratic(self):
        left = self.root.left
        right = self.root.right
        if right.token.type == "?":
            if right.left or right.right:
                if right.left and not right.right:
                    if self.isFt(left):
                        return True
                raise InvalidOperation
        return False

    def isFt(self, node):
        if type(node) == Function:
            if node.token.name in self.variables:
                if type(self.variables[node.token.name]) == dict:
                    if type(node.right) == Variable:
                        if node.right.token.name == self.variables[node.token.name]["var_name"]:
                            return True
        return False


##################
### COMMON
##################

    def calculate(self, node):
        return self.__visit(node)

    def error(self, *args):
        raise InvalidExpression

    def __visit(self, node):
        method_name = "_Interpreter__visit_" + type(node).__name__
        visitor =  getattr(self, method_name, self.error)
        n =  visitor(node)
        return n

    def __visit_BinOp(self, node):
        if node.left:
            node.left = self.__visit(node.left)
            if node.left.token.type == "variable":
                return BinOp(node.left, node.token, self.__visit(node.right))
        if node.right:
            node.right = self.__visit(node.right)
            if node.right.token.type == "variable":
                if node.left:
                    return BinOp(self.__visit(node.left), node.token, node.right)
                return BinOp(None, node.token, node.right)
        else:
            raise InvalidExpression
        if (node.left and node.left.token.binop) or node.right.token.binop:
            return node
        if node.token.type == "+":
            if node.left:
                return node.left + node.right
            return node.right
        elif node.token.type == "-":
            if node.left:
                return node.left - node.right
            return Num(Token("num", float=-1)) * node.right
        elif node.token.type == "*":
            if not node.left:
                raise InvalidExpression
            return node.left * node.right
        elif node.token.type == "/":
            if not node.left:
                raise InvalidExpression
            return node.left / node.right
        elif node.token.type == "%":
            if not node.left:
                raise InvalidExpression
            return node.left % node.right
        elif node.token.type == "^":
            if not node.left:
                raise InvalidExpression
            return node.left ^ node.right
        elif node.token.type == "**":
            if not node.left:
                raise InvalidExpression
            return node.left ** node.right
        raise InvalidExpression

    def __visit_Num(self, node):
        return node
    
    def __visit_Variable(self, node):
        if self.ft_var_assignation_name == node.token.name:
            if self.solving_quadratic:
                return Num(Token("num", xpower={0:0, 1:1}))
            return Variable(Token("variable", name=self.ft_var_assignation_name))
        if self.ft_var_calculation_name == node.token.name:
            return self.ft_var_calculation_node
        if node.token.name in self.variables.keys():
            if type(self.variables[node.token.name]) == dict:
                raise VariableAsFunction
            return self.variables[node.token.name]
        raise UnknownVariable

    def __visit_Function(self, node):
        if node.token.name not in self.variables:
            raise UnknownFunction
        ft = self.variables[node.token.name]
        if type(ft) != dict:
            raise FunctionAsVariable
        if not node.right:
            raise FunctionWithoutArg
        self.ft_var_calculation_node = self.__visit(node.right)
        self.ft_var_calculation_name = ft["var_name"]
        n = self.__visit(copy.deepcopy(ft["tree"]))
        self.ft_var_calculation_node = None
        self.ft_var_calculation_name = None
        if ft["abs"]:
            n.token.imaginary = {p: coef for p, coef in n.token.imaginary.items() if coef != 0}
            n.token.xpower = {p: coef for p, coef in n.token.xpower.items() if coef != 0}
            if not n.token.imaginary and not n.token.xpower and not n.token.matrix:
                n.token.float = n.token.float if n.token.float >= 0 else n.token.float * (-1)
        return n

    def __visit_Parenthesis(self, node):
        if not node.right:
            raise InvalidExpression
        n = self.__visit(node.right)
        n.in_parenthesis = True
        return n

    
