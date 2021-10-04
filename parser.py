from customExceptions import *
from customNodes import *

class Parser:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.token = self.tokenizer.extractToken()
        self.parse()

    def parse(self):
        self.root = self.__priority1()
        #Parser.printTree(self.root)

    @staticmethod
    def printTree(node, level=0):
        if node != None:
            Parser.printTree(node.right, level + 1)
            print(' ' * 4 * level + "  " + '->', node)
            Parser.printTree(node.left, level + 1)

    # PRIVATE
    
    def __priority1(self):
        node = self.__priority2()
        while self.token.type == "=":
            token = self.token
            self.token = self.tokenizer.extractToken()
            node = BinOp(node, token, self.__priority2())
        return node

    def __priority2(self):
        node = self.__priority3()
        while self.token.type == "?":
            token = self.token
            self.token = self.tokenizer.extractToken()
            node = BinOp(node, token, self.__priority3())
        return node

    def __priority3(self):
        node = self.__priority4()
        while self.token.type in "+-":
            token = self.token
            self.token = self.tokenizer.extractToken()
            node = BinOp(node, token, self.__priority4())
        return node

    def __priority4(self):
        node = self.__priority5()
        while self.token.type in "*/%" or self.token.type == "**":
            token = self.token
            self.token = self.tokenizer.extractToken()
            node = BinOp(node, token, self.__priority5())
        return node
    
    def __priority5(self):
        node = self.__priority6()
        while self.token.type == "^":
            token = self.token
            self.token = self.tokenizer.extractToken()
            node = BinOp(node, token, self.__priority6())
        return node

    def __priority6(self):
        node = self.__priority7()
        while self.token.type == "function":
            token = self.token
            self.token = self.tokenizer.extractToken()
            right = self.__priority3()
            if self.token.type != ")":
                raise InvalidExpression
            self.token = self.tokenizer.extractToken()
            return Function(None, token, right)
        return node
    
    def __priority7(self):
        token = self.token
        if self.token.type in ("num", "matrix", "(", "variable"):
            self.token = self.tokenizer.extractToken()
        if token.type == "(":
            right = self.__priority3()
            if self.token.type != ")":
                raise InvalidExpression
            self.token = self.tokenizer.extractToken()
            return Parenthesis(None, token, right)
        if token.type == "num" or token.type == "matrix":
            return Num(token)
        elif token.type == "variable":
            return Variable(token)
        return None
    
