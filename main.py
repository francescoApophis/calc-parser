from lexer import Lexer
from testing import *


class Parser:
    def __init__(self):
        pass

src_str = "45-(45-23*39)-3-45/0"
lexer = Lexer(src_str)
lexer.tokenize(lexer.src_str)
print(lexer.tokens)

'''
if __name__ == '__main__':
    unittest.main(verbosity = 2 )
'''


