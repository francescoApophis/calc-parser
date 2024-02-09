from lexer import Lexer
from testing import *

def calc_prec(op): # get precedence of operator
    if op == '+' or op == '-':
        return 1
    elif op == '*' or op == '/':
        return 2

def is_oper(val):
    return val == '+' or val == '-' or val == '*' or val == '/'

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
        
    def calculate(self, lhs, op, rhs):
        if isinstance(lhs, str):
            lhs = int(lhs)

        if isinstance(rhs, str):
            rhs = int(rhs)
        
        if op == '+':
            return lhs + rhs
        elif op == '-':
            return lhs - rhs
        elif op == '*':
            return lhs * rhs
        elif op == '/':
            return lhs / rhs
        
    def parse(self, lhs, min_prec):
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
                rhs = self.parse(rhs, new_min_prec)
                nt = self.peek()
            
            lhs = self.calculate(lhs, op, rhs)
        return lhs

    def generate_ast(self,lhs, min_prec = 0, higher = False):

        nt = self.peek()
        while nt is not None and is_oper(nt) and calc_prec(nt) >= min_prec:
            op = nt 
            self.increment_counter()
            rhs = self.parse_primary()
            self.increment_counter()
            nt = self.peek()
            
            lhs['op'] = op
            lhs['rhs'] = rhs
            
            while nt is not None and is_oper(nt):
                if calc_prec(nt) > calc_prec(op):
                    new_min_prec = calc_prec(op) + 1 if calc_prec(nt) > calc_prec(op) else 0 
                    rhs = self.generate_ast({'lhs':rhs}, new_min_prec, True)
                    lhs['rhs'] = rhs
                    nt = self.peek()
                else:
                    higher = False
                    break

            if nt is not None and calc_prec(nt) <= calc_prec(op) and not higher:
                node_copy = lhs 
                lhs = {'lhs': node_copy}
            
        return lhs
        
if __name__ == '__main__':
    src_str = "1 / 7 * 4 + 3 / 6 * 5 - 7 " # insert expression
    parser = Parser(src_str)
    print("result:", parser.parse(parser.tokens[0], 0))
    parser.counter = 0
    print("AST:", parser.generate_ast({'lhs': parser.tokens[0]}, 0))

