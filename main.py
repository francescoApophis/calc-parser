from lexer import Lexer
from testing import *

def calc_prec(op):
    if op == '+' or op == '-':
        return 1
    elif op == '*' or op == '/':
        return 2

def isOper(val):
    return val == '+' or val == '-' or val == '*' or val == '/'

class Parser:
    def __init__(self, src_str):
        self.lexer = Lexer(src_str)
        self.lexer.tokenize(src_str)
        self.tokens = self.lexer.tokens
         
        self.counter = 0
    
    def increment_counter(self): 
        self.counter += 1 
    
    def parse_primary(self):   
        # returns the right hand side of an operator when one is meet
        # 'primary' follows the naming on the wikipedia article about 
        # -- operator precedence parser --
        return self.tokens[self.counter + 1]
    
    def peek(self):
        if self.counter + 1 < len(self.tokens):
            return self.tokens[self.counter + 1]
        return None 

    def parse(self, lhs, min_prec):
        pass
                
src_str = "45-23"
parser = Parser(src_str)
tokens = parser.tokens
print("result: ", parser.parse_expr(parser.tokens[0], 0))






#            else:
#                print(f"ALT: prec next: {self.op_prec(next_t)}, prec curr: {self.op_prec(op)}")







