class Notation:
    """ base class for all notation """
    def __init__(self):
        self.data = ''
        self.id = 0
        
        self.nodeLeft = None
        self.nodeRight = None
    
    def toGraph(self, rootId, f):
        if(rootId != -1):
            f.write("\tnode{} -- node{}\n".format(rootId, self.id))
        
        f.write("\tnode{} [ label = \"{}\" ]\n".format(str(self.id), self.data)) #root
        
        if(self.nodeLeft != None):
            self.nodeLeft.toGraph(self.id, f)
        if(self.nodeRight != None):
            self.nodeRight.toGraph(self.id, f)

class Number(Notation):
    def __init__(self):
        super(Number, self).__init__()

    def toString(self):
        return self.data

class X(Notation):
    def __init__(self):
        super(X, self).__init__()
        self.data = 'x'

    def toString(self):
        return 'x'

class N(Notation):
    """ natural number notation """
    def __init__(self):
        super(N, self).__init__()
        self.data = 'n'

    def toString(self):
        return "{}".format(self.nodeLeft.toString())

class R(Notation):
    """ real number notation """
    def __init__(self):
        super(R, self).__init__()
        self.data = 'r'

    def toString(self):
        return "({})".format(self.nodeLeft.toString())

class Add(Notation):
    """ + notation """
    def __init__(self):
        super(Add, self).__init__()
        self.data = '+'

    def toString(self):
        return "({}+{})".format(self.nodeLeft.toString(), self.nodeRight.toString())

class Mul(Notation):
    """ * notation """
    def __init__(self):
        super(Mul, self).__init__()
        self.data = '*'

    def toString(self):
        return "({}*{})".format(self.nodeLeft.toString(), self.nodeRight.toString())

class Sub(Notation):
    """ - notation """
    def __init__(self):
        super(Sub, self).__init__()
        self.data = '-'

    def toString(self):
        return "({}-{})".format(self.nodeLeft.toString(), self.nodeRight.toString())

class Div(Notation):
    """ / notation """
    def __init__(self):
        super(Div, self).__init__()
        self.data = '/'

    def toString(self):
        return "({}/{})".format(self.nodeLeft.toString(), self.nodeRight.toString())

class Pow(Notation):
    """ ^ notation """
    def __init__(self):
        super(Pow, self).__init__()
        self.data = '^'

    def toString(self):
        return "({}**{})".format(self.nodeLeft.toString(), self.nodeRight.toString())

class S(Notation):
    """ sin notation """
    def __init__(self):
        super(S, self).__init__()
        self.data = 's'

    def toString(self):
        return "numpy.sin({})".format(self.nodeLeft.toString())

class C(Notation):
    """ Cos notation """
    def __init__(self):
        super(C, self).__init__()
        self.data = 'c'

    def toString(self):
        return "numpy.cos({})".format(self.nodeLeft.toString())

class E(Notation):
    """ exp notation """
    def __init__(self):
        super(E, self).__init__()
        self.data = 'e'

    def toString(self):
        return "(numpy.e**{})".format(self.nodeLeft.toString())

class Ln(Notation):
    """ ln notation """
    def __init__(self):
        super(Ln, self).__init__()
        self.data = 'l'
        
    def toString(self):
        return "numpy.log({})".format(self.nodeLeft.toString())

class Fac(Notation):
    """ factorial notation """
    def __init__(self):
        super(Fac, self).__init__()
        self.data = '!'

    def toString(self):
        return "numpy.math.factorial({})".format(self.nodeLeft.toString())

class P(Notation):
    def __init__(self):
        super(P, self).__init__()
        self.data = 'p'

    def toString(self):
        return "numpy.pi"