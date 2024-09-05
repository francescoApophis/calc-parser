from errors import * 
from typing import List
import re

class Lexer:
    def __init__(self, expr: str) -> None:
        self.expr = self.is_invalid(expr) 
        self.tokens = self.tokenize()

    def tokenize(self) -> List[str]:
        tokenized = re.split('(\+|\-|\*|\/|\(|\))', self.expr)
        tokenized = list(filter(None, tokenized))
        return tokenized

    def tokenize_recurs(self, expr:str, idx:int = 0) -> None:
        if len(expr) == 1:
            self.tokens.append(expr)
            return

        if idx >= len(expr): 
            return 

        curr_val = expr[idx]
        if self.is_digit(curr_val):
            if len(self.tokens) > 0 and self.is_digit(self.tokens[-1]): 
                self.tokens[-1] += curr_val
            else:
                self.tokens.append(curr_val)
            self.tokenize_recurs(expr, idx + 1)
        else:
            self.tokens.append(curr_val) # operator or parenthesis
            self.tokenize_recurs(expr[idx+1:], 0)

    def is_digit(self, value: str) -> bool:
        # they indicate start of new number
        return value not in ["+", "-", "*", "/", "(", ")", "^"] 
       
    @staticmethod
    def is_invalid(expr:str) -> str:
        expr = expr.replace(" ", "")   
        # ERROR: replace whitespace will consider 
        # valid '12 3 + 2' as '123 + 2'
        
        if len(expr) <= 2 or (len(expr) <= 3 and expr[0] == '-'): 
            NotEnoughErr('operands/operators')

        if set(expr) < set("+-*/()^"): NotEnoughErr('operands')
        if expr[0] in '-': NotImplementedErr('negative numbers')
        if expr[0] in '/^*': NotEnoughErr('operands', 0, expr)
        if expr[-1] in "+*/^-": NotEnoughErr('operands', len(expr)-1, expr)
        if expr[0] in '-': NotImplementedErr('negative numbers') 
        if expr[0] == ')': MismatchedParenthesesErr('(', 1)
        if expr[0] == '+': 
            expr = expr.replace('+', '', 1)
            expr = self.is_invalid(expr)

        op_count = 0 #open parenthesis 
        cp_count = 0 #close parenthesis 

        # this needs to change because (320482934) is a valid expression
        # but I don't know, maybe I could keep it 
        for idx, c in enumerate(expr):
            next_c = expr[idx+1] if idx+1 < len(expr) else None

            if not c.isdigit() and not c in "+-*/()^":  
                InvalidSymErr(c, idx, expr)
            if c.isdigit() and next_c == '.':
                NotImplementedErr('decimal numbers')
            if c in "+*/^-" and next_c in "+*/^)":
                NotEnoughErr('operands', idx, expr)
            if c in "+*/^-" and next_c == "-":
                NotImplementedErr('negative numbers')
            if c == "/" and next_c == '0':
                NotSupportedErr('zero division')

            if c == ")" and next_c == "(": 
                ParenthesesErr('operator', idx, expr)
            if c == "(" and next_c == ")":
                ParenthesesErr('expression', idx, expr)

            if c == "(": op_count += 1
            elif c == ")": cp_count += 1

        if op_count != cp_count:
            parenthesis = ")" if op_count > cp_count else "("
            amount = op_count - cp_count if (op_count > cp_count) else cp_count - op_count 
            MismatchedParenthesesErr(parenthesis, amount)
        return expr

