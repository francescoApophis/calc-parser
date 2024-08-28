from errors import * 

# source-str --> Lexer (creates tokens) --> Creation of tree --> Tree parsing

class Lexer:
    # get tokens
    # recognize which tokens mark the beginning of new tokens

    def __init__(self, src_str):
        self.src_str = self.is_invalid(src_str) 
        self.tokens = []
        self.tokenize(self.src_str)

    def tokenize(self, src_str, idx = 0):
        if len(src_str) == 1:
            self.tokens.append(src_str)
            return

        if idx >= len(src_str): return 

        curr_val = src_str[idx]

        if self.is_digit(curr_val):
            if len(self.tokens) > 0 and self.is_digit(self.tokens[-1]): 
                self.tokens[-1] += curr_val
            else:
                self.tokens.append(curr_val)
            self.tokenize(src_str, idx + 1)
        else:
            self.tokens.append(curr_val) # operator or parenthesis
            self.tokenize(src_str[idx+1:], 0)

    def is_digit(self, value):
        # they indicate start of new number
        return value not in ["+", "-", "*", "/", "(", ")", "^"] 
       
    def is_invalid(self, src_str):
        src_str = src_str.replace(" ", "")   

        if len(src_str) <= 2 or (len(src_str) <= 3 and src_str[0] == '-'): 
            NotEnoughErr('operands/operators')

        if set(src_str) < set("+-*/()^"): NotEnoughErr('operands')
        if src_str[0] in '-': NotImplementedErr('negative numbers')
        if src_str[0] in '/^*': NotEnoughErr('operands', 0, src_str)
        if src_str[-1] in "+*/^-": NotEnoughErr('operands', len(src_str)-1, src_str)
        if src_str[0] in '-': NotImplementedErr('negative numbers') 
        if src_str[0] == '+': 
            src_str = src_str.replace('+', '', 1)
            src_str = self.is_invalid(src_str)

        # op_count = 0 #open parenthesis 
        # cp_count = 0 #close parenthesis 
        for idx, c in enumerate(src_str):
            next_c = src_str[idx+1] if idx+1 < len(src_str) else None

            if not c.isdigit() and not c in "+-*/()^":  
                InvalidSymErr(c, idx, src_str)
            if c in "+*/^-" and next_c in "+*/^)":
                NotEnoughErr('operands', idx, src_str)
            if c in "+*/^-" and next_c == "-":
                NotImplementedErr('negative numbers')
            if c == "/" and next_c == '0':
                NotSupportedErr('zero division')
            if c == '(' or c == ')':
                NotImplementedErr('parentheses')

            # support for parentheses to be implemented yet
            # if c == ")" and next_c == "(": 
                # ParenthesesErr('operator', idx, src_str)
            # if c == "(" and next_c == ")":
                # ParenthesesErr('expression', idx, src_str)

            # if c == "(": op_count += 1
            # elif c == ")": cp_count += 1

        # parenthesis = "(" if op_count > cp_count else ")"
        # amount = op_count - cp_count if op_count > cp_count else cp_count - op_count 
        # if a != b: MismatchedParenthesesError(parenthesis, amount)
        return src_str

