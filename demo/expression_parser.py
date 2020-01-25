"""
"""

from crocs.yacc import Rule, Grammar, Struct, Yacc
from crocs.lexer import Lexer, LexMap, LexNode, XSpec
from crocs.token import Plus, Minus, LP, RP, Mul, Div, Num, Blank

class CalcTokens(XSpec):
    expression = LexMap()
    LexNode(expression, r'\+', Plus)
    LexNode(expression, r'\-', Minus)
    LexNode(expression, r'\(', LP)
    LexNode(expression, r'\)', RP)
    LexNode(expression, r'\*', Mul)
    LexNode(expression, r'\/', Div)

    LexNode(expression, r'[0-9]+', Num)
    LexNode(expression, r' +', Blank)
    root = expression

class CalcGrammar(Grammar):
    expression = Struct(recursive=True)
    term       = Struct(recursive=True)
    factor     = Struct()

    r_plus  = Rule(expression, Plus, term)
    r_minus = Rule(expression, Minus, term)
    expression.add(term, r_plus,  r_minus)

    r_mul = Rule(term, Mul, factor)
    r_div = Rule(term, Div, factor)
    term.add(factor, r_mul, r_div)

    r_paren = Rule(LP, expression, RP)
    r_num   = Rule(Num)
    factor.add(r_paren, r_num)

    root    = expression
    discard = [Blank]

class CalcParser(Yacc):
    def __init__(self):
        self.lexer = Lexer(CalcTokens)
        super(CalcParser, self).__init__(CalcGrammar)

        self.add_handle(CalcGrammar.r_plus, self.plus)
        self.add_handle(CalcGrammar.r_minus, self.minus)
        self.add_handle(CalcGrammar.r_div, self.div)
        self.add_handle(CalcGrammar.r_mul, self.mul)
        self.add_handle(CalcGrammar.r_paren, self.paren)
        self.add_handle(CalcGrammar.r_num, self.num)

    def plus(self, expr, sign, term):
        return expr.val() + term.val()

    def minus(self, expr, sign, term):
        return expr.val() - term.val()

    def div(self, term, sign, factor):
        return term.val()/factor.val()
    
    def mul(self, term, sign, factor):
        return term.val() * factor.val()

    def paren(self, left, expression, right):
        return expression.val()

    def num(self, num):
        return int(num[0].val())

    def calc(self, data):
        self.lexer.feed(data)
        tokens = self.lexer.run()
        ptree = self.build(tokens)
        ptree = list(ptree)
        return ptree

data = '1 + 2 * (3 /(4 - (5 - (6 + (7 + (8 + (9 + (10 + (11 + (12 + (13+(14 * 15 + 16))))))))))))'
parser = CalcParser()
ptree = parser.calc(data)
print('Consumed:', ptree)



