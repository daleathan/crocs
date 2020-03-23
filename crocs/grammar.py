from yacc.yacc import Rule, Grammar, Struct, T
from yacc.lexer import LexMap, LexNode, XSpec
from yacc.token import TokVal, Plus, Minus, LP, RP, Mul, \
Comma, Sof, Eof, Char,  LB, RB, Question, Equal, Hash,\
LBR, RBR, Dot

class RegexTokens(XSpec):
    lexmap = LexMap()
    t_plus = LexNode(r'\+', Plus)

    t_lparen = LexNode(r'\(', LP)
    t_rparen = LexNode(r'\)', RP)

    t_lbracket = LexNode(r'\[', LB)
    t_rbracket = LexNode(r'\]', RB)

    t_lbrace = LexNode(r'\{', LBR)
    t_rbrace = LexNode(r'\}', RBR)
    t_comma  = LexNode(r'\,', Comma)
    t_question = LexNode(r'\*', Question)

    t_mul   = LexNode(r'\*', Mul)
    # t_minus  = LexNode(r'.', Minus)

    t_char  = LexNode(r'.', Char)
    t_hash  = LexNode(r'\#', Hash)
    t_equal = LexNode(r'\=', Equal)

    lexmap.add(t_plus, t_lparen, 
    t_rparen, t_mul, t_lbracket, t_rbracket,
    t_lbrace, t_rbrace, t_comma, t_question,
    t_char,t_hash, t_equal, t_char)

    root = [lexmap]

class RegexGrammar(Grammar):
    regex = Struct()

    r_paren  = Rule(LP, regex, RP, type=regex)
    r_dot    = Rule(Dot, type=regex)
    r_times0 = Rule(LBR, Char, Comma, Char, RBR, type=regex)
    r_times1 = Rule(LBR, Char, RBR, type=regex)
    r_times2 = Rule(LBR, Char, Comma, RBR, type=regex)
    r_times3 = Rule(LBR, Comma, Char, RBR, type=regex)
    r_times4 = Rule(regex, Mul, type=regex)
    r_times5 = Rule(regex, Question, type=regex)

    r_seq    = Rule(Char, TokVal('-'), Char, type=regex)
    r_set    = Rule(LB, T(regex), RB, type=regex)
    r_char   = Rule(Char, type=regex)

    r_done   = Rule(Sof, regex, Eof)

    regex.add(r_char, r_paren, r_done)
    root    = [regex]