from lexer import Lexer
from testing import *

class Tree:
    def __init__(self, op = None, lhs = None, rhs = None):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

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
        return self.tokens[self.counter + 1]

    def parse(self, lhs, min_prec):
        pass
                
src_str = "45-23"
parser = Parser(src_str)
tokens = parser.tokens
print("result: ", parser.parse_expr(parser.tokens[0], 0))






#            else:
#                print(f"ALT: prec next: {self.op_prec(next_t)}, prec curr: {self.op_prec(op)}")







