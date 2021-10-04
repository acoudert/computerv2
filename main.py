#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt
from customExceptions import *
from tokenizer import Tokenizer
from parser import Parser
from interpreter import Interpreter

def help(_):
    print("Available Commands:")
    print("\thelp: This help")
    print("\texit: Exit the program")
    print("\thist: Display history")
    print("\td_var: Display variables")
    print("\td_fun: Display functions")
    print("\tc_fun: Display functions curves")

def hist(s):
    print(s[:-1])

def d_var(variables):
    print("Stored Variables:")
    for name, value in variables.items():
        if type(value) != dict:
            print("\t{} = {}".format(name, value.token))

def d_fun(variables):
    print("Stored Functions:")
    for name, value in variables.items():
        if type(value) == dict:
            print("\t{} = {}".format(name, value["string"]))

def c_fun(variables):
    for name, value in variables.items():
        if type(value) == dict:
            plt.figure(figsize=(10, 7))
            values = []
            for i in range(value["x0"], value["x1"]):
                tokenizer = Tokenizer("{}({})=?".format(name, i))
                parser = Parser(tokenizer)
                node = Interpreter(parser, variables).n
                if not node.token.imaginary and not node.token.matrix:
                    values.append(node.token.float)
                else:
                    print("Cant display {}({}) due to matrix or imaginary".format(name, value["var_name"]))
                    break
            if values:
                plt.plot(range(value["x0"], value["x1"]), values, "g-")
                plt.xlabel("{}".format(value["var_name"]))
                plt.ylabel("{}({})".format(name, value["var_name"]))
                plt.title("{}({}) = {}".format(name, value["var_name"], value["string"]))
                plt.show()

def exit(_):
    sys.exit(0)

def setUpFunctions(variables):
    s = "exp(x) = 2.7182818284590452353602874713527^x"
    tokenizer = Tokenizer(s)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser, variables, x0=0, x1=16)
    interpreter.getResultStr()
    s = "square(x) = x^0.5"
    tokenizer = Tokenizer(s)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser, variables, x0=0, x1 = 201)
    interpreter.getResultStr()
    s = "abs(x) = x"
    tokenizer = Tokenizer(s)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser, variables, True)
    interpreter.getResultStr()
    variables["abs"]["string"] = "| x |"
    s = "sin(x) = 4*x*(180-x)/(40500-x*(180-x))"
    tokenizer = Tokenizer(s)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser, variables, x0=-180, x1=181)
    interpreter.getResultStr()
    s = "cos(x) = (1-4*x*(180-x)/(40500-x*(180-x))^2)^0.5"
    tokenizer = Tokenizer(s)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser, variables, x0=-180, x1=181)
    interpreter.getResultStr()
    s = "tan(x) = (4*x*(180-x)/(40500-x*(180-x)))/((1-4*x*(180-x)/(40500-x*(180-x))^2)^0.5)"
    tokenizer = Tokenizer(s)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser, variables, x0=-180, x1=181)
    interpreter.getResultStr()
    s = "rad(x) = x * 3.141592653589793 / 180"
    tokenizer = Tokenizer(s)
    parser = Parser(tokenizer)
    interpreter = Interpreter(parser, variables, x0=-180, x1=181)
    interpreter.getResultStr()


def main():
    variables = {}
    key_words = {
            "help": None,
            "exit": None,
            "hist": "",
            "d_var": variables,
            "d_fun": variables,
            "c_fun": variables
        }
    setUpFunctions(variables)
    try:
        f = open(sys.argv[1], "r") if len(sys.argv) > 1 else sys.stdin
    except:
        f = sys.stdin
    while True:
        try:
            expression = input("> ") if f == sys.stdin else f.readline()[:-1]
            if not expression:
                break
            if f != sys.stdin:
                print(">", expression)
            if expression in key_words:
                eval(expression + "(key_words[expression])")
                continue
            tokenizer = Tokenizer(expression)
            parser = Parser(tokenizer)
            interpreter = Interpreter(parser, variables)
            s = interpreter.getResultStr()
            print("\t{}".format(s))
            key_words["hist"] += "> " + expression + "\n\t" + s + "\n"
        except Exception as e:
            print("\tException:", e, file=sys.stderr)

if __name__ == "__main__":
    main()
