import copy
from customExceptions import *
from customNodes import Num
from tokenizer import Token

class Solver:

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.s = ""

    def solve(self):
        self.__reduce()    
        self.degree = 0
        self.reduced = [self.left.token.float, 0, 0]
        if self.left.token.xpower:
            self.degree = max([p for p in self.left.token.xpower])
            if min([p for p in self.left.token.xpower]) < 0:
                self.degree += abs(min([p for p in self.left.token.xpower]))
            if self.degree > 2:
                self.__getResultsStr()
                return self.s
            for p, coef in self.left.token.xpower.items():
                self.reduced[p] = self.left.token.xpower[p]
        self.solution = self.__calculateSolution()
        self.__getResultsStr()
        return self.s

    def __getResultsStr(self):
        self.s += "{}= 0\n".format(self.left.token)
        self.s += "\tPolynomial degree: {}\n".format(self.degree)
        if self.degree > 2:
            self.s += "\tEquation cannot be solved"
            return
        if hasattr(self, "discriminant"):
            self.s += "\tDiscriminant: {}\n".format(self.discriminant)
        self.s += "\t{}\n".format(self.solution[0])
        for sol in self.solution[1]:
            self.s += "\t\t{}\n".format(sol)
        self.s = self.s[:-1]

    def __reduce(self):
        self.__reduceFloat()
        self.__reduceImaginary1()
        self.__reduceXPower1()
        self.__reduceImaginary2()
        self.__reduceXPower2()

    def __reduceFloat(self):
        self.left -= Num(Token("num", float=self.right.token.float))
        self.right.token.float = 0

    def __reduceImaginary1(self):
        left_imaginary = {p: coef for p, coef in self.left.token.imaginary.items() if coef != 0}
        right_imaginary = {p: coef for p, coef in self.right.token.imaginary.items() if coef != 0}
        for p, coef in right_imaginary.items():
            if p not in left_imaginary:
                self.left.token.imaginary[p] = 0
            self.left -= Num(Token("num", imaginary={p: coef}))
        self.left.token.imaginary = {p: coef for p, coef in self.left.token.imaginary.items() if coef != 0}
        self.right.token.imaginary = {}
        
    def __reduceXPower1(self):
        left_xpower = {p: coef for p, coef in self.left.token.xpower.items() if coef != 0}
        right_xpower = {p: coef for p, coef in self.right.token.xpower.items() if coef != 0}
        for p, coef in left_xpower.items():
            if p in right_xpower:
                self.left -= Num(Token("num", xpower={p: coef}))
                self.right.token.xpower[p] = 0
        self.left.token.xpower = {p: coef for p, coef in self.left.token.xpower.items() if coef != 0}
        self.right.token.xpower = {p: coef for p, coef in self.right.token.xpower.items() if coef != 0}
        if self.right.token.xpower:
            i = 0
            for p, coef in self.right.token.xpower.items():
                i += 1
                if i != len(self.right.token.xpower):
                    self.left -= Num(Token("num", xpower={p: coef}))
                    self.right.token.xpower[p] = 0
        self.left.token.xpower = {p: coef for p, coef in self.left.token.xpower.items() if coef != 0}
        self.right.token.xpower = {p: coef for p, coef in self.right.token.xpower.items() if coef != 0}
    
    def __reduceImaginary2(self):
        n = Num(Token("num", float=self.left.token.float, imaginary=copy.deepcopy(self.left.token.imaginary)))
        mul_nb = 0
        for p, coef in self.left.token.imaginary.items():
            for m in range(abs(p)):
                n *= Num(Token("num", imaginary={1:1}))
                mul_nb += 1
        nxl = Num(Token("num"))
        nxr = Num(Token("num"))
        if self.left.token.xpower:
            if mul_nb % 2:
                raise UnsolvableEquation
            mul_nb_l = mul_nb // 2
            nxl = Num(Token("num", xpower=copy.deepcopy(self.left.token.xpower)))
            for _ in range(mul_nb_l):
                nxl *= Num(Token("num", float=-1))
        if self.right.token.xpower:
            if mul_nb % 2:
                raise UnsolvableEquation
            mul_nb_r = mul_nb // 2
            nxr = Num(Token("num", xpower=copy.deepcopy(self.right.token.xpower)))
            for _ in range(mul_nb_r):
                nxr *= Num(Token("num", float=-1))
        self.left = n + nxl
        self.right = nxr
        self.left.token.imaginary = {p: coef for p, coef in self.left.token.imaginary.items() if coef != 0}
        if self.left.token.imaginary:
            raise UnsolvableEquation

    def __reduceXPower2(self):
        n = copy.deepcopy(self.left)
        if self.right.token.xpower:
            n /= Num(Token("num", xpower=self.right.token.xpower))
            n -= Num(Token("num", float=1))
        n.token.xpower = {p: coef for p, coef in n.token.xpower.items() if coef != 0}
        if n.token.xpower:
            if min([p for p in n.token.xpower]) < 0:
                for _ in range(abs(min([p for p in n.token.xpower]))):
                    n *= Num(Token("num", xpower={1:1}))
            elif max([p for p in n.token.xpower]) > 2:
                for _ in range(2, max([p for p in n.token.xpower])):
                    n /= Num(Token("num", xpower={1:1}))
            n.token.xpower = {p: coef for p, coef in n.token.xpower.items() if coef != 0}
        self.left = n
        self.left.token.xpower = {p: coef for p, coef in self.left.token.xpower.items() if coef != 0}

    def __calculateSolution(self):
        if self.__allRealsSolution():
            return ("The solutions are:", ["All real numbers - R"])
        if self.__unsolvable():
            return ("There is no solution.", [])
        if self.degree == 1:
            return self.__solveDegreeOne()
        self.discriminant = self.__calculateDiscriminant()
        if self.discriminant > 0:
            return self.__solvePositive()
        elif self.discriminant == 0:
            return self.__solveZero()
        else:
            return self.__solveNegative()

    def __allRealsSolution(self):
        return all([i == 0 for i in self.reduced])

    def __unsolvable(self):
        if self.reduced[0] and not any([i for i in self.reduced[1:]]):
            return True
        return False
    
    def __solveDegreeOne(self):
        sol = (-1) * self.reduced[0] / self.reduced[1]
        sol = int(sol) if sol.is_integer() else sol
        return ("The solution is:", [sol])

    def __calculateDiscriminant(self):
        discriminant = float(self.reduced[1] ** 2 - 4 * self.reduced[0] * self.reduced[2])
        if discriminant.is_integer():
            return int(discriminant)
        return discriminant

    def __solvePositive(self):
        sola = ((-1) * self.reduced[1] + self.discriminant ** (1/2)) / (2 * self.reduced[2])
        solb = ((-1) * self.reduced[1] - self.discriminant ** (1/2)) / (2 * self.reduced[2])
        sola = int(sola) if sola.is_integer() else sola
        solb = int(solb) if solb.is_integer() else solb
        return ("The two solutions are:", [sola, solb])

    def __solveZero(self):
        sol = ((-1) * self.reduced[1]) / (2 * self.reduced[2])
        sol = int(sol) if sol.is_integer() else sol
        return ("The solution is:", [sol])

    def __solveNegative(self):
        real = ((-1) * self.reduced[1]) / (2 * self.reduced[2])
        imag = ((-1) * self.discriminant) ** (1/2) / (2 * self.reduced[2])
        sola = complex(real, imag)
        solb = complex(real, (-1) * imag)
        sola = str(sola).replace("-", " - ").replace("+", " + ").replace("j", " i")
        solb = str(solb).replace("-", " - ").replace("+", " + ").replace("j", " i")
        sola = sola[1:-1] if sola[0] == "(" else sola
        solb = solb[1:-1] if solb[0] == "(" else solb
        sola = sola[1:] if sola[0] == " " else sola
        solb = solb[1:] if solb[0] == " " else solb
        return ("The two solutions are:", [sola, solb])
