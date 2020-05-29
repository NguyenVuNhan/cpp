class Notation:
    """ base class for all notation """
    def __init__(self, nodeLeft=None, nodeRight=None):
        self.data = ''
        self.id = 0
        
        self.nodeLeft = nodeLeft
        self.nodeRight = nodeRight

    def simplify(self):
        return self

    def getDerivative(self):
        return None

    def toFunction(self):
        return self.data

    def toString(self):
        return self.toFunction()

    def toGraph(self, rootId, f):
        if(rootId != -1):
            f.write("\tnode{} -- node{}\n".format(rootId, self.id))
        
        f.write("\tnode{} [ label = \"{}\" ]\n".format(str(self.id), self.data)) #root
        
        if(self.nodeLeft != None):
            self.nodeLeft.toGraph(self.id, f)
        if(self.nodeRight != None):
            self.nodeRight.toGraph(self.id, f)

class Number(Notation):
    def __init__(self, nodeLeft=None, nodeRight=None, data=""):
        super(Number, self).__init__(nodeLeft, nodeRight)
        self.data = data

class H(Notation):
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(H, self).__init__(nodeLeft, nodeRight)
        self.data = 'h'

    def getDerivative(self):
        return self

class X(Notation):
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(X, self).__init__(nodeLeft, nodeRight)
        self.data = 'x'

    def getDerivative(self):
        node = Number(data="1")
        return node

class N(Notation):
    """ natural number notation """
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(N, self).__init__(nodeLeft, nodeRight)
        self.data = 'n'

    def toFunction(self):
        return "{}".format(self.nodeLeft.toFunction())

class R(Notation):
    """ real number notation """
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(R, self).__init__(nodeLeft, nodeRight)
        self.data = 'r'

    def toFunction(self):
        return "({})".format(self.nodeLeft.toFunction())

    def toString(self):
        return "({})".format(self.nodeLeft.toString())

class Add(Notation):
    """ + notation """
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(Add, self).__init__(nodeLeft, nodeRight)
        self.data = '+'

    def simplify(self):
        # Update the node left and right
        self.nodeLeft = self.nodeLeft.simplify()
        self.nodeRight = self.nodeRight.simplify()

        # Simplify rules
        # 0 + 0
        if ( self.nodeLeft.toString() == '0' and
                self.nodeRight.toString() == '0' ):
            return N(Number(data='0'))
        # a + 0
        if ( self.nodeLeft.toString() == '0' ):
            return self.nodeRight
        if ( self.nodeRight.toString() == '0' ):
            return self.nodeLeft
        # a + b
        if ( type(self.nodeLeft) == Number and
                type(self.nodeRight) == Number ):
            return Number(data=str(float(self.nodeLeft.data.replace(',','.'))+float(self.nodeRight.data.replace(',','.'))).replace(".0",""))
        if ( ( type(self.nodeLeft) == N or
                type(self.nodeLeft) == R ) and
                ( type(self.nodeRight) == N or
                    type(self.nodeRight) == R ) ):
            return Number(data=str(float(self.nodeLeft.nodeLeft.data.replace(',','.'))+float(self.nodeRight.nodeLeft.data.replace(',','.'))).replace(".0",""))
        # f(x) + f(x)
        if ( self.nodeLeft.toString() == self.nodeRight.toString() ):
            return Mul(self.nodeLeft, N(Number(data='2')))
        # a*f(x)+f(x)
        if ( type(self.nodeLeft) == Mul):
            if ( self.nodeLeft.nodeLeft.toString() == self.nodeRight.toString() ):
                return Mul(Add(self.nodeLeft.nodeRight, Number(data="1").simplify()), self.nodeRight)
            elif ( self.nodeLeft.nodeRight.toString() == self.nodeRight.toString() ):
                return Mul(Add(self.nodeLeft.nodeLeft, Number(data="1").simplify()), self.nodeRight)
        if ( type(self.nodeRight) == Mul):
            if ( self.nodeRight.nodeLeft.toString() == self.nodeLeft.toString() ):
                return Mul(Add(self.nodeRight.nodeRight, Number(data="1").simplify()), self.nodeLeft)
            elif ( self.nodeRight.nodeRight.toString() == self.nodeLeft.toString() ):
                return Mul(Add(self.nodeRight.nodeLeft, Number(data="1").simplify()), self.nodeLeft)
        # ((f(x) + a(x)) + (f(x) + b(x)))
        if ( type(self.nodeLeft) == type(self.nodeRight) == Add ):
            node_ll = Add(Add(self.nodeLeft.nodeLeft, self.nodeRight.nodeLeft).simplify(), Add(self.nodeLeft.nodeRight, self.nodeRight.nodeRight).simplify()).simplify()
            node_lr = Add(Add(self.nodeLeft.nodeLeft, self.nodeRight.nodeRight).simplify(), Add(self.nodeLeft.nodeRight, self.nodeRight.nodeLeft).simplify()).simplify()
            if ( len(node_ll.toString()) <= len(node_lr.toString()) ):
                return node_ll
            else:
                return node_lr
        return self

    def toFunction(self):
        return "({}+{})".format(self.nodeLeft.toFunction(), self.nodeRight.toFunction())

    def toString(self):
        return "({}+{})".format(self.nodeLeft.toString(), self.nodeRight.toString())

    def getDerivative(self):
        u = self.nodeLeft.getDerivative()
        v = self.nodeRight.getDerivative()
        if ( u == None and v == None):
            return None
        if ( u == None ):
            return v
        if ( v == None ):
            return u
        node = Add(u,v)
        return node

class Mul(Notation):
    """ * notation """
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(Mul, self).__init__(nodeLeft, nodeRight)
        self.data = '*'

    def simplify(self):
        # Update node left and right
        self.nodeLeft = self.nodeLeft.simplify()
        self.nodeRight = self.nodeRight.simplify()

        # Simplify rules
        # f(x)*1
        if ( self.nodeLeft.toString() == '1' ):
            return self.nodeRight
        if ( self.nodeRight.toString() == '1'):
            return self.nodeLeft
        # f(x)*0
        if ( self.nodeLeft.toString() == '0' or
            self.nodeRight.toString() == '0' ):
            return Number(data='0')
        # a*b
        if ( type(self.nodeLeft) == Number and
                type(self.nodeRight) == Number ):
            return Number(data=str(float(self.nodeLeft.data.replace(',','.'))*float(self.nodeRight.data.replace(',','.'))).replace(".0",""))
        if ( ( type(self.nodeLeft) == N or
                type(self.nodeLeft) == R ) and
                ( type(self.nodeRight) == N or
                    type(self.nodeRight) == R ) ):
            return Number(data=str(float(self.nodeLeft.nodeLeft.data.replace(',','.'))*float(self.nodeRight.nodeLeft.data.replace(',','.'))).replace(".0",""))
        # f(x)*f(x)
        if ( self.nodeLeft.toString() == self.nodeRight.toString() ):
            return Pow(self.nodeLeft, N(Number(data='2')))
        # a*f(x)*f(x)
        if ( type(self.nodeLeft) == Mul):
            if ( self.nodeLeft.nodeLeft.toString() == self.nodeRight.toString() ):
                return Mul(self.nodeLeft.nodeRight, Pow(self.nodeRight, Number(data="2").simplify()))
            elif ( self.nodeLeft.nodeRight.toString() == self.nodeRight.toString() ):
                return Mul(self.nodeLeft.nodeLeft, Pow(self.nodeRight, Number(data="2").simplify()))
        if ( type(self.nodeRight) == Mul):
            if ( self.nodeRight.nodeLeft.toString() == self.nodeLeft.toString() ):
                return Mul(self.nodeRight.nodeRight, Pow(self.nodeRight, Number(data="2").simplify()))
            elif ( self.nodeRight.nodeRight.toString() == self.nodeLeft.toString() ):
                return Mul(self.nodeRight.nodeLeft, Pow(self.nodeRight, Number(data="1").simplify()))
        return self

    def toFunction(self):
        return "({}*{})".format(self.nodeLeft.toFunction(), self.nodeRight.toFunction())

    def toString(self):
        return "({}*{})".format(self.nodeLeft.toString(), self.nodeRight.toString())

    def getDerivative(self):
        u = self.nodeLeft.getDerivative()
        v = self.nodeRight.getDerivative()
        if ( u == None and v == None):
            return None
        if ( u == None ):
            return Mul(v, self.nodeLeft)
        if ( v == None ):
            return Mul(u, self.nodeRight) 
        node = Add(Mul(v,self.nodeLeft),Mul(u,self.nodeRight))
        return node

class Sub(Notation):
    """ - notation """
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(Sub, self).__init__(nodeLeft, nodeRight)
        self.data = '-'

    def simplify(self):
        # Update the node left and right
        self.nodeLeft = self.nodeLeft.simplify()
        self.nodeRight = self.nodeRight.simplify()

        # Simplify rules
        # 0 - 0
        if ( self.nodeLeft.toString() == '0' and
                self.nodeRight.toString() == '0' ):
            return N(Number(data='0'))
        # a - 0
        if ( self.nodeLeft.toString() == '0' ):
            return self.nodeRight
        if ( self.nodeRight.toString() == '0' ):
            return self.nodeLeft
        # a - b
        if ( type(self.nodeLeft) == Number and
                type(self.nodeRight) == Number ):
            return Number(data=str(float(self.nodeLeft.data.replace(',','.'))-float(self.nodeRight.data.replace(',','.'))).replace(".0",""))
        if ( ( type(self.nodeLeft) == N or
                type(self.nodeLeft) == R ) and
                ( type(self.nodeRight) == N or
                    type(self.nodeRight) == R ) ):
            return Number(data=str(float(self.nodeLeft.nodeLeft.data.replace(',','.'))-float(self.nodeRight.nodeLeft.data.replace(',','.'))).replace(".0",""))
        # f(x) - f(x)
        if ( self.nodeLeft.toString() == self.nodeRight.toString() ):
            return N(Number(data='0'))
        # a*f(x)-f(x)
        if ( type(self.nodeLeft) == Mul):
            if ( self.nodeLeft.nodeLeft.toString() == self.nodeRight.toString() ):
                return Mul(Sub(self.nodeLeft.nodeRight, Number(data="1").simplify()), self.nodeRight)
            elif ( self.nodeLeft.nodeRight.toString() == self.nodeRight.toString() ):
                return Mul(Sub(self.nodeLeft.nodeLeft, Number(data="1").simplify()), self.nodeRight)
        if ( type(self.nodeRight) == Mul):
            if ( self.nodeRight.nodeLeft.toString() == self.nodeLeft.toString() ):
                return Mul(Sub(self.nodeRight.nodeRight, Number(data="1").simplify()), self.nodeLeft)
            elif ( self.nodeRight.nodeRight.toString() == self.nodeLeft.toString() ):
                return Mul(Sub(self.nodeRight.nodeLeft, Number(data="1").simplify()), self.nodeLeft)
        # ((f(x) + a(x)) + (f(x) + b(x)))
        if ( type(self.nodeLeft) == type(self.nodeRight) == Add ):
            node_ll = Add(Sub(self.nodeLeft.nodeLeft, self.nodeRight.nodeLeft).simplify(), Sub(self.nodeLeft.nodeRight, self.nodeRight.nodeRight).simplify()).simplify()
            node_lr = Add(Sub(self.nodeLeft.nodeLeft, self.nodeRight.nodeRight).simplify(), Sub(self.nodeLeft.nodeRight, self.nodeRight.nodeLeft).simplify()).simplify()
            if ( len(node_ll.toString()) <= len(node_lr.toString()) ):
                return node_ll
            else:
                return node_lr
        return self

    def toFunction(self):
        return "({}-{})".format(self.nodeLeft.toFunction(), self.nodeRight.toFunction())

    def toString(self):
        return "({}-{})".format(self.nodeLeft.toString(), self.nodeRight.toString())

    def getDerivative(self):
        u = self.nodeLeft.getDerivative()
        v = self.nodeRight.getDerivative()
        if ( u == None and v == None):
            return None
        if ( u == None ):
            return Mul(Number(data="-1"),v)    
        if ( v == None ):
            return u
        node = Sub(u, Mul(Number(data="-1"),v))
        return node

class Div(Notation):
    """ / notation """
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(Div, self).__init__(nodeLeft, nodeRight)
        self.data = '/'

    def simplify(self):
        # Update the node left and right
        self.nodeLeft = self.nodeLeft.simplify()
        self.nodeRight = self.nodeRight.simplify()

        # Simplify rules
        # 0/f(x)
        if ( self.nodeLeft.toString() == '0' ):
            return Number(data='0')
        # f(x)/0
        if ( self.nodeRight.toString() == '0'):
            raise Exception("Divive for 0")
        # f(x)/1
        if ( self.nodeRight.data == '0' ):
            return self.nodeLeft
        # n/n
        if ( type(self.nodeLeft) == Number and
                type(self.nodeRight) == Number ):
            return Number(data=str(float(self.nodeLeft.data.replace(',','.'))/float(self.nodeRight.data.replace(',','.'))).replace(".0",""))
        if ( ( type(self.nodeLeft) == N and
                type(self.nodeRight) == N ) or
                ( type(self.nodeLeft) == R and
                    type(self.nodeRight) == R ) ):
            return Number(data=str(float(self.nodeLeft.nodeLeft.data.replace(',','.'))/float(self.nodeRight.nodeLeft.data.replace(',','.'))).replace(".0",""))
        # f(x)^a/f(x)^b
        if ( type(self.nodeLeft) == Pow and
                type(self.nodeRight) == Pow and
                self.nodeLeft.nodeLeft.toString() == self.nodeRight.nodeLeft.toString() ):
            node = Sub(self.nodeLeft.nodeRight, self.nodeRight.nodeRight).simplify()
            return Pow(self.nodeRight, node)
        # f(x)^a/f(x)
        if ( type(self.nodeLeft) == Pow and
                self.nodeLeft.nodeLeft.toString() == self.nodeRight.toString() ):
            node = Sub(self.nodeLeft.nodeRight, N(Number(data="1"))).simplify()
            return Pow(self.nodeRight, node)
        # f(x)/f(x)^a
        if ( type(self.nodeRight) == Pow and
                self.nodeLeft.toString() == self.nodeRight.nodeLeft.toString() ):
            node = Sub(N(Number(data="1")), self.nodeRight.nodeRight).simplify()
            return Pow(self.nodeRight, node)
        # f(x)/f(x)
        if ( self.nodeLeft.toString() == self.nodeRight.toString() ):
            return Number(data='1')
        return self

    def toFunction(self):
        return "({}/{})".format(self.nodeLeft.toFunction(), self.nodeRight.toFunction())

    def toString(self):
        return "({}/{})".format(self.nodeLeft.toString(), self.nodeRight.toString())

    def getDerivative(self):
        u = self.nodeLeft.getDerivative()
        v = self.nodeRight.getDerivative()
        print(type(u), type(v))
        if ( u == None and v == None):
            return None
        if ( u == None ):
            return Div(Mul(Number(data="-1"), Mul(v, self.nodeLeft)), Pow(self.nodeRight, Number(data="2")))
        if ( v == None ):
            return u
        node = Div(Sub(Mul(u, self.nodeRight), Mul(v, self.nodeLeft)), Pow(self.nodeRight, Number(data="2")))
        return node 

class Pow(Notation):
    """ ^ notation """
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(Pow, self).__init__(nodeLeft, nodeRight)
        self.data = '^'

    def simplify(self):
        # update node left and right
        self.nodeLeft = self.nodeLeft.simplify()
        self.nodeRight = self.nodeRight.simplify()
        
        # simplify rules
        # f(x)^1
        if ( self.nodeRight.data == '1' ):
            return self.nodeLeft
        # f(x)^0 or 0^f(x)
        if ( self.nodeRight.data == '0' or
                self. nodeLeft.data == '1' ):
            return Number(data='1')
        return self
        
    def toFunction(self):
        return "({}**{})".format(self.nodeLeft.toFunction(), self.nodeRight.toFunction())
    
    def toString(self):
        return "({}^{})".format(self.nodeLeft.toString(), self.nodeRight.toString())

    def getDerivative(self):
        #l^r
        u = self.nodeLeft.getDerivative()
        v = self.nodeRight.getDerivative()
        if ( u == None and v == None ):
            return None
        if ( u == None ):
            node = Mul(Mul(v,l(self.nodeLeft)),Pow(self.nodeLeft, v))
            return node
        if ( v == None ):
            node = Mul(self.nodeRight, Pow(self.nodeLeft, Sub(self.nodeRight,Number(data="1"))))
            return node
        node = Add(Mul(Mul(Pow(self.nodeLeft, self.nodeRight),v),Ln(self.nodeLeft)),Mul(Mul(Pow(self.nodeLeft,Sub(self.nodeRight, self.Number(data="1"))),self.nodeRight),u))
        return node

class S(Notation):
    """ sin notation """
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(S, self).__init__(nodeLeft, nodeRight)
        self.data = 's'

    def simplify(self):
        self.nodeLeft = self.nodeLeft.simplify()
        return self

    def toFunction(self):
        return "numpy.sin({})".format(self.nodeLeft.toFunction())

    def toString(self):
        return "sin({})".format(self.nodeLeft.toString())

    def getDerivative(self):
        u = self.nodeLeft.getDerivative()
        if ( u == None ):
            return None
        node = Mul(u,C(self.nodeLeft))
        return node

class C(Notation):
    """ Cos notation """
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(C, self).__init__(nodeLeft, nodeRight)
        self.data = 'c'

    def simplify(self):
        self.nodeLeft = self.nodeLeft.simplify()
        return self

    def toFunction(self):
        return "numpy.cos({})".format(self.nodeLeft.toFunction())

    def toString(self):
        return "cos({})".format(self.nodeLeft.toString())

    def getDerivative(self):
        u = self.nodeLeft.getDerivative()
        if ( u == None ):
            return None
        node = Mul(u, Mul(Number(data="-1"), S(self.nodeLeft)))
        return node

class E(Notation):
    """ exp notation """
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(E, self).__init__(nodeLeft, nodeRight)
        self.data = 'e'

    def simplify(self):
        self.nodeLeft = self.nodeLeft.simplify()
        return self

    def toFunction(self):
        return "(numpy.e**{})".format(self.nodeLeft.toFunction())

    def toString(self):
        return "(e^{})".format(self.nodeLeft.toString())

    def getDerivative(self):
        u = self.nodeLeft.getDerivative()
        if( u == None ):
            return None
        node = Mul(u, E(self.nodeLeft))
        return node

class Ln(Notation):
    """ ln notation """
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(Ln, self).__init__(nodeLeft, nodeRight)
        self.data = 'l'

    def simplify(self):
        self.nodeLeft = self.nodeLeft.simplify()
        return self

    def toFunction(self):
        return "numpy.log({})".format(self.nodeLeft.toFunction())

    def toString(self):
        return "ln({})".format(self.nodeLeft.toString())

    def getDerivative(self):
        u = self.nodeLeft.getDerivative()
        if( u == None ):
            return None
        node = Div(u, self.nodeLeft)
        return node

class Fac(Notation):
    """ factorial notation """
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(Fac, self).__init__(nodeLeft, nodeRight)
        self.data = '!'

    def simplify(self):
        self.nodeLeft = self.nodeLeft.simplify()
        return self

    def toFunction(self):
        return "numpy.math.factorial({})".format(self.nodeLeft.toFunction())

    def toString(self):
        return "{}!".format(self.nodeLeft.toString())

    def getDerivative(self):
        u = self.nodeLeft.getDerivative()
        if ( u == None ):
            return None
        raise Exception("There is no derivative for f(x)!")
 
class P(Notation):
    def __init__(self, nodeLeft=None, nodeRight=None):
        super(P, self).__init__(nodeLeft, nodeRight)
        self.data = 'p'

    def toFunction(self):
        return "numpy.pi"

    def toString(self):
        return "pi"