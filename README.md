
# calc-parser

Small parser for simple math expressions. Built to learn about 
lexing, parsing and operator precendence work.

It uses the '[precedence climbing method](https://en.wikipedia.org/wiki/Operator-precedence_parser)'.

Supported:
- addition, 
- subtraction, 
- multiplication
- division

Soon to be implemented:
- negative and decimal numbers
- parentheses 
- exponentiation

## Usage

    python3 main.py <flag> <expr>
    python3 main.py <flag> '<expr>' (to use spacing inside the expression)

    flags:
        -c    calculate and print result from string expression
        -t    generate and print tree from expression 
        -tc   both previous flags
        -ct   calculate and print result from tree, for debugging tree
        -all  all commands at the same time
