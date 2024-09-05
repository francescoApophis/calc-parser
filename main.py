from typing import Union, Tuple, List
from parser import Parser
import sys


class Main:
    valid_flags:List[str] = ['-c', '-t', '-tc', '-ct', '-all', '-h']

    def __init__(self) -> None:
        self.execute()

    def execute(self) -> None:
        argv = self.check_argv_count(sys.argv[1:])
        flag = self.check_valid_flag(argv[0])

        if flag == '-h':
            self.print_usage(descr = True)
            exit(0)
        
        expr = argv[1]
        parser = Parser(expr)

        if flag == '-c':
            print('result:', parser.parse_and_calc())
        if flag == '-t':
            print('tree:', parser.gen_tree())
        if flag == '-tc':
            print('result:', parser.parse_and_calc())
            parser.counter = 0
            print('tree:', parser.gen_tree())
        if flag == '-ct':
            print('result_from_tree:', parser.calc_from_tree())
        if flag == '-all':
            print('result:' ,parser.parse_and_calc())
            parser.counter = 0
            print('result_from_tree:', parser.calc_from_tree())
            parser.counter = 0
            tree = parser.gen_tree()
            parser.counter = 0
            print('tree:', tree)
        exit(0)

    def check_argv_count(self, argv: List[str]) -> List[str]:
        if len(argv) > 2:
            self.error_out('too many arguments')
        if len(argv) < 1 or len(argv) == 1 and argv[0] != '-h':
            self.error_out('too few arguments')
        return argv

    def check_valid_flag(self, flag:str) -> str:
        if flag not in Main.valid_flags:
            self.error_out('invalid \'{flag}\' flag')
        return flag

    def error_out(self, msg: str) -> None:
        print(f'\nERROR: {msg}\n')
        self.print_usage()
        exit(1)

    def print_usage(self, descr:bool = False):
        if descr:
            print('''Small parser for simple math expressions.
Supported:
    - addition
    - subtraction,
    - multiplication
    - division
    - parentheses
Soon to be implemented:
    - negative and decimal numbers
    - exponentiation
        ''')

        print('''Usage: 
    python3 main.py <flag> <expr>
    python3 main.py <flag> '<expr>' (to use spacing inside the expression)

flags:
    -c   calculate and print result from string expression
    -t   generate and print tree from expression 
    -tc  both previous flags
    -ct  calculate and print result from tree expression (mainly for 
         debugging tree)
    -all all commands at the same time
        ''')


if __name__ == '__main__':  
    main = Main()


