from lexer import Lexer
from typing import Union, Tuple, List
from errors import *
import sys


class Parser:
    def __init__(self, expr:str) -> None:
        self.expr = expr
        self.tokens: List[str] = Lexer(expr).tokens
        self.counter = 0

    def start(self, flag: str): 
        if flag == '-c':
            result_from_str = self.parse_and_calc(self.tokens[0])
            self.counter = 0
            return result_from_str

        if flag == '-t':
            tree = self.gen_tree(self.tokens[0])
            self.counter = 0
            return tree

        if flag == '-tc':
            result_from_str = self.parse_and_calc(self.tokens[0])
            self.counter = 0
            tree = self.gen_tree(self.tokens[0])
            self.couner = 0
            return result_from_str, tree

        if flag == '-ct':
            result_from_tree = calc_from_tree(self.gen_tree(self.tokens[0]))
            return result_from_tree

        if flag == '-all':
            tree = self.gen_tree(self.tokens[0])
            self.counter = 0
            result_from_str =  self.parse_and_calc(self.tokens[0])
            self.counter = 0
            result_from_tree = self.calc_from_tree(tree)
            return result_from_str, result_from_tree, tree


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
        return res

    def calc_from_tree(self, node:dict) -> int:
        lhs = node['lhs'] if not isinstance(node['lhs'], dict) else self.calc_from_tree(node['lhs'])
        rhs = node['rhs'] if not isinstance(node['rhs'], dict) else self.calc_from_tree(node['rhs'])
        op = node['op']

        return self.calc(lhs, op, rhs)
    
    def gen_tree(self, lhs:Union[str, dict], min_prec:int = 0) -> dict:
        nt = self.peek()

        while nt is not None and self.is_oper(nt) and self.calc_prec(nt) >= min_prec:
            op = nt 
            self.increment_counter()
            rhs = self.parse_primary()
            self.increment_counter()
            nt = self.peek()

            while nt is not None and self.is_oper(nt) and self.calc_prec(nt) > self.calc_prec(op):
                new_min_prec =  self.calc_prec(op) + 1 if self.calc_prec(nt) > self.calc_prec(op) else 0
                rhs = self.gen_tree(rhs, new_min_prec)
                nt = self.peek()

            lhs = {
                'lhs': int(lhs) if type(lhs) == str else lhs,
                'op': op, 
                'rhs': int(rhs) if type(rhs) == str else rhs,
            }

        return lhs 

    def parse_and_calc(self, lhs:str, min_prec:int = 0, level:int = 0) -> int:
        nt = self.peek()

        while nt is not None:
            if nt == '(' or (nt is not None and nt.isdigit()):
                self.increment_counter()
                lhs = self.parse_and_calc(nt, 0, level + 1)
                self.increment_counter()
                nt = self.peek()

            elif nt == ')':
                if level > 0: return lhs
                self.increment_counter()
                nt = self.peek()
    
            elif self.is_oper(nt) and self.calc_prec(nt) >= min_prec:
                op = nt
                self.increment_counter()
                rhs = self.parse_primary()
                self.increment_counter()
                nt = self.peek()

                if rhs == '(':
                    self.increment_counter()
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
            else:
                break
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
