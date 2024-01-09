
# source-str --> Lexer (creates tokens) --> Creation of tree --> Tree parsing

source_string = "12*(3+4)^2"

class Lexer:
    # get tokens
    # recognize which tokens mark the beginning of new tokens
    def __init__(self, source_string):
        self.source_string = source_string
        self.tokens = []
        
    def tokenize(self, source_string):
        if len(source_string) <= 1:
            self.tokens.append(source_string)
            return

        self.tokens.append(source_string[0])
        self.tokenize(source_string[1:len(source_string)])
    

class Parser:
    def __init__(self):
        pass


lexer = Lexer(source_string)
lexer.tokenize(lexer.source_string)
print(lexer.tokens)
