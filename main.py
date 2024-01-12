from errors import * 
# source-str --> Lexer (creates tokens) --> Creation of tree --> Tree parsing

class Lexer:
    # get tokens
    # recognize which tokens mark the beginning of new tokens
    def __init__(self, src_str):
        self.src_str = src_str 
        self.tokens = []
        self.is_invalid(src_str)

    def tokenize(self, src_str, idx = 0):
        if len(src_str) <= 1:
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

        try:
            x = int(src_str[0])
        except IndexError:  
            print("IndexError: given string is empty\n")
            raise
        except ValueError:  # first char is anything but +,-, ( 
            x = src_str[0]
            if x in ["-", "("]:
                pass
            elif x in ["*", "/"]: 
                raise MissingOperandError(0, b = x) 
            elif x == ")":
                raise MismatchedParenthesisError(0, 1)
            elif x == "+":
                src_str = src_str[1:]
        
        # unfinished expression  
        try: 
            if src_str[-1] in ["+", "*", "/", "^"]:
                raise MissingOperandError(idx = len(src_str)-1, a = src_str[-1])
        except MissingOperandError:
            raise

        # string is just a single number
        try:
            if int(src_str):
                raise NoOperatorFoundError 
        except NoOperatorFoundError:
            raise 
        except ValueError:
            pass 

        parenthesis_count = [0,0]
        for idx, c in enumerate(src_str):
            try:
                if idx+1 <= len(src_str)-1:
                    c_next = src_str[idx+1]
                    
                    if c == "/" and c_next == '0':
                        raise ZeroDivisionError
                    if c in ["+", "*", "/", "^"] and c_next in ["+", "*", "/", "^", ")"]:
                        raise MissingOperandError(c, c_next)
                    if c == ")" and c_next == "(": 
                        raise OppositeParenthesisError(idx)
                    if c == "(" and c_next == ")":
                        raise EmptyParenthesisError(idx)
                    
                    if c == "(":
                        parenthesis_count[0]+= 1
                    elif c == ")":
                        parenthesis_count[1]+= 1

            except ZeroDivisionError:
                raise
            except OppositeParenthesisError: 
                raise
            except MissingOperandError:
                raise
            except EmptyParenthesisError:
                raise
        
        try:
            a, b = parenthesis_count
            if a != b:
                raise MismatchedParenthesisError(a, b)
        except MismatchedParenthesisError:
            raise

        self.src_str = src_str 

class Parser:
    def __init__(self):
        pass

src_str = "12*(3+4)^2"
src_str = "456 *((3-3)+2)-2"
src_str = "456 *(3-3+2+256*2))-2"
src_str = ")"
lexer = Lexer(src_str)
lexer.tokenize(lexer.src_str)
print(lexer.tokens)

