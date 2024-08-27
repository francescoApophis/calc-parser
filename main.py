from lexer import Lexer
from testing import *
from typing import Union




class Parser:
    def __init__(self, src_str:str) -> None:
        self.tokens:list = Lexer(src_str).tokens
        self.counter:int = 0

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
            return lhs + rhs
        elif op == '-':
            return lhs - rhs
        elif op == '*':
            return lhs * rhs
        elif op == '/':
            return lhs / rhs

    def calc_from_ast(self, node:dict) -> int:
        lhs = node['lhs'] if not isinstance(node['lhs'], dict) else self.calc_from_ast(node['lhs'])
        rhs = node['rhs'] if not isinstance(node['rhs'], dict) else self.calc_from_ast(node['rhs'])
        op = node['op']

        return self.calc(lhs, op, rhs)

        
    def parse_and_calc(self, lhs:str, min_prec:int = 0) -> int:
        nt = self.peek()

        while nt is not None and self.is_oper(nt) and self.calc_prec(nt) >= min_prec:
            op = nt 
            self.increment_counter()
            rhs = self.parse_primary()
            self.increment_counter()
            nt = self.peek()
            
            # get result of the operation ahead *FIRST* if the the operator has higher precedence
            while nt is not None and self.is_oper(nt) and self.calc_prec(nt) > self.calc_prec(op):
                new_min_prec =  self.calc_prec(op) + 1 if self.calc_prec(nt) > self.calc_prec(op) else 0
                rhs = self.parse_and_calc(rhs, new_min_prec)
                nt = self.peek()
            
            lhs = int(lhs) if isinstance(lhs, str) else lhs
            rhs = int(rhs) if isinstance(rhs, str) else rhs
            lhs = self.calc(lhs, op, rhs)
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


if __name__ == '__main__':
    src_str = '8 - 39 / 331'
    parser = Parser(src_str)

    root_node = parser.gen_ast(parser.tokens[0])

    print('result from node:', parser.calc_from_ast(root_node))

    parser.counter = 0
    print('result from alg: ', parser.parse_and_calc(parser.tokens[0]))







