from errors import * 

# source-str --> Lexer (creates tokens) --> Creation of tree --> Tree parsing

class Lexer:
    # get tokens
    # recognize which tokens mark the beginning of new tokens

    def __init__(self, src_str):
        self.is_invalid(src_str)
        self.src_str = src_str 
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
        
        #------------empty or 1 char strings------------ 

        try:
            if len(src_str) < 1:
                raise IndexError("given string is empty") 
            
            elif len(src_str) == 1:
                if src_str.isdigit():
                    raise ValueError("string is a single number; no operation to perform") 
                elif src_str in "+-*/()^":
                    raise ValueError("no operands found; no operation to perform") 
                else: 
                    raise ValueError(f"invalid math symbol '{src_str}'; no operation to perform") 
        except IndexError: raise
        except ValueError: raise        
        
        #------------multiple char strings------------

        try:
            if src_str.isdigit():
                raise ValueError("string is a single number; no operation to perform")
            if set(src_str) < set("+-*/()^"): # if it's subset all chars are operators 
                raise ValueError("no operand found; no operation to perform") 

            if src_str[0] in "/^*": # 
                raise MissingOperandError(0, b = src_str[0]) 
            elif src_str[0] == ")":
                raise MismatchedParenthesisError(0, 1)
            elif src_str[0] == "+":
                if src_str.replace("+", "").isdigit():
                    raise ValueError("string is a single number; no operation to perform") 
                else:
                    src = src_str.replace("+", "")
                
            elif src_str[0] in "-(": 
                pass 
            else:
                pass # letters and other symbols are dealt with in the for loop below 
            
            # unfinished expression
            if src_str[-1] in "+*/^-":
                raise MissingOperandError(len(src_str)-1, a = src_str[-1])
        except MissingOperandError: raise
        except MismatchedParenthesisError: raise
        except ValueError: raise 

        
        parenthesis_count = [0,0]
        for idx, c in enumerate(src_str):
            try:
                c_next = src_str[idx+1] if idx+1 < len(src_str) else None
                if not c.isdigit() and not c in "+-*/()^":  
                    raise ValueError(f"invalid math symbol '{c}' at '{idx}'") 

                if c in "+*/^-" and c_next != None and c_next in "+*/^)":
                    raise MissingOperandError(idx, c, c_next) 

                if c == "/" and c_next == '0':
                    raise ZeroDivisionError
                
                if c == ")" and c_next == "(": 
                    raise OppositeParenthesisError(idx)
                
                if c == "(" and c_next == ")":
                    raise EmptyParenthesisError(idx)

                if c == "(":
                    parenthesis_count[0]+= 1
                elif c == ")":
                    parenthesis_count[1]+= 1
                
            except ValueError: raise
            except MissingOperandError: raise
         
        try:
            a, b = parenthesis_count
            if a != b:
                raise MismatchedParenthesisError(a, b)
        except MismatchedParenthesisError:
            raise
        
