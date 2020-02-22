class XNode:
    def __init__(self):
        pass

class PTree(list):
    """
    """
    __slots__ = ['rule', 'type', 'result', 'data']

    def __init__(self, iterable=(), rule=None, type=None):
        super(PTree, self).__init__(iterable)

        self.rule = rule
        self.type = type
        self.data = type
        self.result = None

    def eval(self, handle):
        if handle:
            self.result = handle(*self)

    def val(self):
        return self.result

# class Token(namedtuple('Token', ('data', 'type', 'value'))):
    # def val(self):
        # return self.value
    # 
    # def tlen(self):
        # return 1
# 
    # def clen(self):
        # return len(self.data)
# 
    # def __repr__(self):
        # return '%s(%s)' % (self.type.__name__, repr(self.data))

class Token:
    def __init__(self, data, type=None, cast=None):
        self.data = data
        self.value = cast(data) if cast else data
        self.type = type

    def val(self):
        return self.value
    
    def tlen(self):
        return 1

    def clen(self):
        return len(self.data)

    def __repr__(self):
        return '%s(%s)' % (self.type.__name__, repr(self.data))

class TSeq(list):
    """
    This is meant to be returned by XNode's instances
    that extract strings from a given doc sequentially.
    """

    def __init__(self, *args):
        self.extend(args)

    def clen(self):
        count = 0
        for ind in self:
            count += ind.clen()
        return count

class TokType:
    @classmethod
    def validate(cls, tokens):
        tok = tokens.get()
        if tok != None and cls.istype(tok):
            return tok

    @classmethod
    def istype(cls, tok):
        return tok.type is cls

class TokVal:
    
    def __init__(self, data):
        self.data = data

    def validate(self, tokens):
        tok = tokens.get()
        if tok != None and self.istype(tok):
            return tok

    def istype(self, tok):
        return self.data == tok.data

    def __repr__(self):
        return '%s(%s)' % (self.__name__, repr(self.data))

class Eof(TokType):
    pass

class Sof(TokType):
    pass

class Num(TokType):
    pass

class Plus(TokType):
    pass

class Minus(TokType):
    pass

class Div(TokType):
    pass

class Mul(TokType):
    pass

class RP(TokType):
    pass

class LP(TokType):
    pass

class Blank(TokType):
    pass

class Keyword(TokType):
    pass

class Identifier(TokType):
    pass

class Colon(TokType):
    pass
