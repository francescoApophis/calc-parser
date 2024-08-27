from lexer import Lexer
from testing import *

def calc_prec(op): # get precedence of operator
    if op == '+' or op == '-':
        return 1
    elif op == '*' or op == '/':
        return 2

def is_oper(val):
    return val == '+' or val == '-' or val == '*' or val == '/'

class Node:
    def __init__(self, lhs = None, op = None, rhs = None):
        self.lhs = lhs 
        self.op  = op 
        self.rhs = rhs 

class Parser:
    def __init__(self, src_str):
        self.lexer = Lexer(src_str)
        self.tokens = self.lexer.tokens
        self.counter = 0
    
    def increment_counter(self): 
        self.counter += 1 
    
    def parse_primary(self):   
        # returns the rhs of an operator when one is meet
        # 'primary' follows the naming convention on the wikipedia article about 
        # -- operator precedence parser --
        return self.tokens[self.counter + 1]
    
    def peek(self): # get next token
        if self.counter + 1 < len(self.tokens):
            return self.tokens[self.counter + 1]
        return None 
        
    def calc(self, lhs, op, rhs):
        if op == '+':
            return lhs + rhs
        elif op == '-':
            return lhs - rhs
        elif op == '*':
            return lhs * rhs
        elif op == '/':
            return lhs / rhs

    def calc_from_ast(self, node):
        lhs = node['lhs'] if not isinstance(node['lhs'], dict) else self.calc_from_ast(node['lhs'])
        rhs = node['rhs'] if not isinstance(node['rhs'], dict) else self.calc_from_ast(node['rhs'])
        op = node['op']

        return self.calc(lhs, op, rhs)

        
    def parse_and_calc(self, lhs, min_prec = 0):
        nt = self.peek()

        while nt is not None and is_oper(nt) and calc_prec(nt) >= min_prec:
            op = nt 
            self.increment_counter()
            rhs = self.parse_primary()
            self.increment_counter()
            nt = self.peek()
            
            # get result of the operation ahead *FIRST* if the the operator has higher precedence
            while nt is not None and is_oper(nt) and calc_prec(nt) > calc_prec(op):
                new_min_prec =  calc_prec(op) + 1 if calc_prec(nt) > calc_prec(op) else 0
                rhs = self.parse_and_calc(rhs, new_min_prec)
                nt = self.peek()
            
            lhs = int(lhs) if isinstance(lhs, str) else lhs
            rhs = int(rhs) if isinstance(rhs, str) else rhs
            lhs = self.calc(lhs, op, rhs)
        return lhs


    def gen_ast(self, lhs:str, min_prec:int = 0) -> dict:
        nt = self.peek()

        while nt is not None and is_oper(nt) and calc_prec(nt) >= min_prec:
            op = nt 
            self.increment_counter()
            rhs = self.parse_primary()
            self.increment_counter()
            nt = self.peek()

            while nt is not None and is_oper(nt) and calc_prec(nt) > calc_prec(op):
                new_min_prec =  calc_prec(op) + 1 if calc_prec(nt) > calc_prec(op) else 0
                rhs = self.gen_ast(rhs, new_min_prec)
                nt = self.peek()

            lhs_val = int(lhs) if type(lhs) == str else lhs
            rhs = int(rhs) if type(rhs) == str else rhs
            lhs = {'lhs': lhs_val, 'op': op, 'rhs':rhs}
        return lhs 
                

if __name__ == '__main__':
    src_str = '8 * 7 - 200 /1003423'
    parser = Parser(src_str)

    root_node = parser.gen_ast(parser.tokens[0])
    print('result from node:', parser.calc_from_ast(root_node))

    parser.counter = 0
    print('result from alg: ', parser.parse_and_calc(parser.tokens[0]))







