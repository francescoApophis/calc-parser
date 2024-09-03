from lexer import Lexer
from typing import Union, Tuple
from errors import *
import sys


class Parser:
    def __init__(self, src_str:str, flag: str) -> None:
        self.src_str = src_str
        self.tokens:list = Lexer(src_str).tokens
        self.counter:int = 0
        # self.start(flag)

    def start(self, flag: str):
        # calculate result from string
        if flag == '-c':
            return self.parse_and_calc(self.tokens[0])

        # generate a tree 
        elif flag == '-t':
            t = self.gen_ast(self.tokens[0])
            return t 

        # calculate result from string and generate a tree 
        elif flag == '-tc':
            print('result:', self.parse_and_calc(self.tokens[0]))
            self.counter = 0
            print('tree:', self.gen_ast(self.tokens[0]))

        # calculate result from ast 
        elif flag == '-ct':
            print('result from ast:', calc_from_ast(self.gen_ast(self.tokens[0])))

        elif flag == '-all':
            tree = self.gen_ast(self.tokens[0])
            print('tree:', tree)
            self.counter = 0
            print('result from str:', self.parse_and_calc(self.tokens[0]))
            self.counter = 0
            print('result from ast:', self.calc_from_ast(tree))


    def calc_prec(self, op: str) -> int: # get precedence of operator
        if op == '+' or op == '-':
            return 1
        elif op == '*' or op == '/':
            return 2

    def is_oper(self, token: str) -> bool:
        return token == '+' or token == '-' or token == '*' or token == '/'
    
    def increment_counter(self) -> None: 
        self.counter += 1 
    
    def parse_primary(self) -> str:   
        # returns the rhs of an operator when one is meet
        # 'primary' follows the naming convention on the wikipedia article about 
        # -- operator precedence parser --
        return self.tokens[self.counter + 1]
    
    def peek(self) -> Union[str, None]: # get next token
        if self.counter + 1 < len(self.tokens):
            return self.tokens[self.counter + 1]
        return None 
        
    def calc(self, lhs:int, op:str, rhs:int) -> int:
        if op == '+':
            res = lhs + rhs
        elif op == '-':
            res = lhs - rhs
        elif op == '*':
            res = lhs * rhs
        elif op == '/':
            res = lhs / rhs
        
        print(f"{round(lhs, 2)} {op} {round(rhs, 2)} = {round(res, 2)}")
        return res

        # if op == '+':
            # return lhs + rhs
        # elif op == '-':
            # return lhs - rhs
        # elif op == '*':
            # return lhs * rhs
        # elif op == '/':
            # return lhs / rhs

    def calc_from_ast(self, node:dict) -> int:
        lhs = node['lhs'] if not isinstance(node['lhs'], dict) else self.calc_from_ast(node['lhs'])
        rhs = node['rhs'] if not isinstance(node['rhs'], dict) else self.calc_from_ast(node['rhs'])
        op = node['op']

        return self.calc(lhs, op, rhs)
    
    def parse_and_calc(self, lhs:str, min_prec:int = 0, level:int = 0) -> int:
        nt = self.peek()

        while nt is not None:
            if nt == '(':
                self.increment_counter()
                lhs = self.parse_and_calc(nt, 0, level + 1)
                nt = self.peek() 
            if nt == ')':
                self.increment_counter()
                nt = self.peek()

            elif nt is not None and nt.isdigit():
                lhs = nt
                self.increment_counter()
                nt = self.peek()

            elif self.is_oper(nt):
                if self.calc_prec(nt) >= min_prec:
                    op = nt 
                    self.increment_counter()
                    rhs = self.parse_primary()
                    self.increment_counter()
                    nt = self.peek()

                    if rhs == '(':
                        rhs = self.parse_and_calc(nt, 0, level + 1)
                        self.increment_counter()
                        nt = self.peek()

                    while nt is not None and self.is_oper(nt) and self.calc_prec(nt) > self.calc_prec(op):
                        new_min_prec =  self.calc_prec(op) + 1 if self.calc_prec(nt) > self.calc_prec(op) else 0
                        rhs = self.parse_and_calc(rhs, new_min_prec, level)
                        nt = self.peek()

                    lhs = int(lhs) if isinstance(lhs, str) else lhs
                    rhs = int(rhs) if isinstance(rhs, str) else rhs
                    lhs = self.calc(lhs, op, rhs)

                    if nt == ')' and level > 0:
                       return lhs 
                else:
                    break
            else:
                break
        return lhs

    def gen_ast(self, lhs:Union[str, dict], min_prec:int = 0) -> dict:
        nt = self.peek()

        while nt is not None and self.is_oper(nt) and self.calc_prec(nt) >= min_prec:
            op = nt 
            self.increment_counter()
            rhs = self.parse_primary()
            self.increment_counter()
            nt = self.peek()

            while nt is not None and self.is_oper(nt) and self.calc_prec(nt) > self.calc_prec(op):
                new_min_prec =  self.calc_prec(op) + 1 if self.calc_prec(nt) > self.calc_prec(op) else 0
                rhs = self.gen_ast(rhs, new_min_prec)
                nt = self.peek()

            lhs = {
                'lhs': int(lhs) if type(lhs) == str else lhs,
                'op': op, 
                'rhs': int(rhs) if type(rhs) == str else rhs,
            }

        return lhs 



def print_descr():
    print(''' Small parser for simple math expressions.
    Supported:
        - addition, subtraction, multiplication and division
    Soon to be implemented:
        - negative and decimal numbers
        - parentheses 
        - exponentiation
    ''')


def print_usage(help: Union[bool, None] = None):
    if help:
        print_descr()
    print('''Usage: 
    python3 main.py <flag> <expr>
    python3 main.py <flag> '<expr>' (to use spacing inside the expression)
    
    flags:
        -c   calculate and print result from string expression
        -t   generate and print tree from expression 
        -tc  both previous flags
        -ct  calculate and print result from tree expression (mainly for 
             debugging tree)
        -all all commands at the same time
    ''')


if __name__ == '__main__':
    argv = sys.argv[1:]

    if not argv:
        print('ERROR: too few arguments')
        print_usage()
        exit(1)

    if len(argv) > 2:
        print('ERROR: too many arguments')
        print_usage()
        exit(1)

    flag = argv[0]

    if flag == '-h':
        print_usage(True)
        exit(0)
    if flag in ['-c', '-t', '-tc', '-ct', '-all']:
        if len(argv) == 2: 
            expr = argv[1]
            parser = Parser(expr, flag)
        else:
            print('ERROR: missing expression')
            print_usage()
            exit(1)
    else:
        print(f'ERROR: invalid \'{flag}\' flag')
        print_usage()
        exit(1)
