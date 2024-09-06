from lexer import Lexer
from typing import Union, Tuple, List


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
        try:
            if op == '+':
                res = lhs + rhs
            elif op == '-':
                res = lhs - rhs
            elif op == '*':
                res = lhs * rhs
            elif op == '/':
                res = lhs / rhs
        except ZeroDivisionError:
            res = 'undefined'
        return res

    def calc_from_tree(self, node: Union[dict, None] = None) -> int:
        node = self.gen_tree() if node is None else node
        lhs = node['lhs'] if not isinstance(node['lhs'], dict) else self.calc_from_tree(node['lhs'])
        rhs = node['rhs'] if not isinstance(node['rhs'], dict) else self.calc_from_tree(node['rhs'])
        op = node['op']

        if lhs == 'undefined': return lhs
        if rhs == 'undefined': return rhs

        return self.calc(lhs, op, rhs)
    
    def gen_tree(self, lhs:Union[str, dict, None] = None, min_prec:int = 0, level:int = 0) -> dict:
        lhs = self.tokens[0] if lhs is None else lhs
        nt = self.peek()

        while nt is not None:
            if nt == '(' or (nt is not None and nt.isdigit()):
                self.increment_counter()
                lhs = self.gen_tree(nt, 0, level + 1)
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
                    rhs = self.gen_tree(nt, 0, level + 1)
                    self.increment_counter()
                    nt = self.peek()

                while nt is not None and self.is_oper(nt) and self.calc_prec(nt) > self.calc_prec(op):
                    new_min_prec =  self.calc_prec(op) + 1 if self.calc_prec(nt) > self.calc_prec(op) else 0
                    rhs = self.gen_tree(rhs, new_min_prec, level)
                    nt = self.peek()

                lhs = {
                    'lhs': int(lhs) if type(lhs) == str else lhs,
                    'op': op, 
                    'rhs': int(rhs) if type(rhs) == str else rhs,
                }
            else:
                break
        return lhs

    def parse_and_calc(self, lhs:Union[str,None] = None, min_prec:int = 0, level:int = 0) -> int:
        lhs = self.tokens[0] if lhs is None else lhs
        nt = self.peek()
        while nt is not None:
            if lhs == 'undefined':
                return lhs

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

                if rhs == 'undefined':
                    return rhs

                lhs = int(lhs) if isinstance(lhs, str) else lhs
                rhs = int(rhs) if isinstance(rhs, str) else rhs
                lhs = self.calc(lhs, op, rhs)
            else:
                break
        return lhs

