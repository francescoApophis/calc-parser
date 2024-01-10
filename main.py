
# source-str --> Lexer (creates tokens) --> Creation of tree --> Tree parsing

class Lexer:
    # get tokens
    # recognize which tokens mark the beginning of new tokens
    def __init__(self, src_str):
        self.src_str = source_string
        self.tokens = []
        
    def tokenize(self, src_str, idx = 0):
        if len(src_str) <= 1:
            self.tokens.append(src_str)
            return
        
        if idx >= len(src_str): return 

        curr_val = src_str[idx] 
        
        if self.is_digit(curr_val):
            self.tokenize(src_str, idx + 1)
        else:
            self.tokens.append(src_str[:idx]) # final number
            self.tokens.append(src_str[idx]) # operator or parenthesis
            self.tokenize(src_str[idx+1:], 0)

    def is_digit(self, value):
       return value not in ["+", "-", "*", "/", "(", ")", "^"] # they indicate start of new number

class Parser:
    def __init__(self):
        pass


src_str = "12*(3+4)^2"

lexer = Lexer(src_str)
lexer.tokenize(lexer.src_str)
print(lexer.tokens)
