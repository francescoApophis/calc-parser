from lexer import Lexer
from typing import Union, Tuple, List
from errors import *
import sys


class Parser:
    def __init__(self, expr:str) -> None:
        self.expr = expr
        self.tokens: List[str] = Lexer(expr).tokens
        self.counter = 0

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

    def calc_from_tree(self, node: Union[dict, None] = None) -> int:
        node = self.gen_tree() if node is None else node
        lhs = node['lhs'] if not isinstance(node['lhs'], dict) else self.calc_from_tree(node['lhs'])
        rhs = node['rhs'] if not isinstance(node['rhs'], dict) else self.calc_from_tree(node['rhs'])
        op = node['op']

        return self.calc(lhs, op, rhs)
    
    def gen_tree(self, lhs:Union[str, dict, None] = None, min_prec:int = 0) -> dict:
        lhs = self.tokens[0] if lhs is None else lhs
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

    def parse_and_calc(self, lhs:Union[str,None] = None, min_prec:int = 0, level:int = 0) -> int:
        lhs = self.tokens[0] if lhs is None else lhs
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


class Main:
    valid_flags = ['-c', '-t', '-tc', '-ct', '-all', '-h']

    def __init__(self):
        self.execute()

    def execute(self):
        argv = self.check_argv_count(sys.argv[1:])
        flag = self.check_valid_flag(argv[0])

        if flag == '-h':
            self.print_usage(descr = True)
            exit(0)
        
        expr = argv[1]
        parser = Parser(expr)

        if flag == '-c':
            print('result:', parser.parse_and_calc())
        if flag == '-t':
            print('tree:', parser.gen_tree())
        if flag == '-tc':
            print('result:', parser.parse_and_calc())
            parser.counter = 0
            print('tree:', parser.gen_tree())
        if flag == '-ct':
            print('result_from_tree:', parser.calc_from_tree())
        if flag == '-all':
            print('result:' ,parser.parse_and_calc())
            parser.counter = 0
            print('result_from_tree:', parser.calc_from_tree())
            parser.counter = 0
            tree = parser.gen_tree()
            parser.counter = 0
            print('tree:', tree)
        exit(0)

    def check_argv_count(self, argv):
        if len(argv) > 2:
            self.error_out('too many arguments')
        if len(argv) < 1 or len(argv) == 1 and argv[0] != '-h':
            self.error_out('too few arguments')
        return argv

    def check_valid_flag(self, flag):
        if flag not in Main.valid_flags:
            self.error_out('invalid \'{flag}\' flag')
        return flag

    def error_out(self, msg: str):
        print(f'\nERROR: {msg}\n')
        self.print_usage()
        exit(1)

    def print_usage(self, descr:bool = False):
        if descr:
            print('''Small parser for simple math expressions.
Supported:
    - addition, subtraction, multiplication, division, parentheses
Soon to be implemented:
    - negative and decimal numbers
    - exponentiation
        ''')

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
    main = Main()


