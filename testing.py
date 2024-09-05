from main import Parser
from lexer import Lexer
import unittest
from random import randint, choice
import re


def rand_num(expr, end_rand = 100000):
    num = str(randint(1, end_rand))
    return num

opers = ['+', '/', '-', '*']

''' at the moment it doesn't generate exprs with: 
    - negative nums: -1 + (-1 * 5)
    - exponentiation
    - decimal nums '''
def gen_rand_exprs(max_opers_in_sub_expr = 5, nesting_level = 1, curr_level = 1):
    expr = ''
    if curr_level >= nesting_level:
        for i in range(randint(2, max_opers_in_sub_expr)):
            pars = randint(0, 1)
            expr += '(' if pars else ''
            expr += rand_num(expr)
            expr += choice(opers)
            expr += rand_num(expr) if pars else ''
            expr += ')' if pars else ''
            expr += choice(opers) if pars else ''

        if expr[-1] in opers:
            expr = expr[:-1]
        return expr

    pars = randint(0, 1)
    expr += '(' if pars else ''
    expr += gen_rand_exprs(max_opers_in_sub_expr, nesting_level, curr_level + 1)
    expr += choice(opers)
    expr += gen_rand_exprs(max_opers_in_sub_expr, nesting_level, curr_level + 1)
    expr += ')' if pars else ''

    # sometimes it generates zero divison 
    # despite the check in rand_num() 
    # for now this is how I deal with it
    if '/0' in expr:
        expr = expr.replace('/0', '/' + randint(1, 100000))
    return expr


# @unittest.skip('not needed')
class TestRandGenExpressions(unittest.TestCase):
    def test_rand_expressions_are_correct(self):
        for i in range(10 * 1000):
            self.assertTrue(Lexer.is_invalid(gen_rand_exprs(nesting_level = randint(1, 10))))
        

class TestParser(unittest.TestCase):
    def test_gen_trees_from_epxrs(self):
        for i in range(10 * 1000):
            expr = gen_rand_exprs(nesting_level = randint(1, 10))
            parser = Parser(expr)
            py_eval_zero_div_err, parser_zero_div_err = None, None
            py_result, parser_result = None, None

            try: 
                py_result = eval(expr)
            except ZeroDivisionError as inst: 
                py_eval_zero_div_err = inst.args
            try: 
                parser_result = parser.calc_from_tree()
            except ZeroDivisionError as inst: 
                parser_zero_div_err = inst.args

            self.assertEqual(py_eval_zero_div_err, parser_zero_div_err)
            self.assertEqual(parser_result, py_result)
        
    def test_exprs(self):
        for i in range(10 * 1000):
            expr = gen_rand_exprs(nesting_level = randint(1, 10))
            parser = Parser(expr)
            py_eval_zero_div_err, parser_zero_div_err = None, None
            py_result, parser_result = None, None

            try: 
                py_result = eval(expr)
            except ZeroDivisionError as inst: 
                py_eval_zero_div_err = inst.args
            try: 
                parser_result = parser.parse_and_calc()
            except ZeroDivisionError as inst: 
                parser_zero_div_err = inst.args

            self.assertEqual(py_eval_zero_div_err, parser_zero_div_err)
            self.assertEqual(parser_result, py_result)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestParser('test_exprs'))
    suite.addTest(TestParser('test_gen_trees_from_epxrs'))
    return suite

runner = unittest.TextTestRunner(verbosity=3)
runner.run(suite())

# unittest.main(verbosity=3)
