
# calc-parser

Small parser for simple math expressions. Built to learn about how 
lexing, parsing and operator precendence work.

It uses the '[precedence climbing method](https://en.wikipedia.org/wiki/Operator-precedence_parser)'.
Again, this is for learning purposes and to get a general idea of how this process works, so it may not
use the best algorithm or the best implentation. 

Supported:
- [x] addition, 
- [x] subtraction, 
- [x] multiplication
- [x] division
- [x] parentheses 

Soon to be implemented:
- [ ] negative and decimal numbers
- [ ] exponentiation

## Usage

    python3 main.py <flag> <expr>
    python3 main.py <flag> '<expr>' (to use spacing inside the expression)

    flags:
        -c    calculate and print result from string expression
        -t    generate and print tree from expression 
        -tc   both previous flags
        -ct   calculate and print result from tree, for debugging tree
        -all  all commands at the same time
