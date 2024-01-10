
# source-str --> Lexer (creates tokens) --> Creation of tree --> Tree parsing

class Lexer:
    # get tokens
    # recognize which tokens mark the beginning of new tokens
    def __init__(self, source_string):
        self.source_string = source_string
        self.tokens = []
        
    def tokenize(self, source_string, idx = 0):
        if len(source_string) <= 1:
            self.tokens.append(source_string)
            return
        
        if idx >= len(source_string): return 

        curr_val = source_string[idx] 
        
        if self.is_digit(curr_val):
            self.tokenize(source_string, idx + 1)
        else:
            self.tokens.append(source_string[:idx]) # final number
            self.tokens.append(source_string[idx]) # operator or parenthesis
            self.tokenize(source_string[idx+1:], 0)

    def is_digit(self, value):
       return value not in ["+", "-", "*", "/", "(", ")", "^"] # they indicate start of new number

class Parser:
    def __init__(self):
        pass


source_string = "12*(3+4)^2"

lexer = Lexer(source_string)
lexer.tokenize(lexer.source_string)
print(lexer.tokens)
