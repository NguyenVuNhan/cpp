import notation
import numpy

class Parse:
    def __init__(self, func):
        #Static id for each node
        self.i = 1
        self.func = func.replace(' ', '')
        self.root = self.parse()
        print(self.root.toString())
        self.root = self.root.simplify()
        self.function = self.root.toFunction()
        self.function_da = "0"
        self.function_dq = "0"
        self.str_function = self.root.toString()
        self.str_function_da = "0"
        self.str_function_dq = "0"
        """
            Derivative
        """
        # Analyticaly
        self.derivative = self.root.getDerivative()
        if ( self.derivative.toString() != "0" ):
            self.derivative = self.derivative.simplify()
            self.function_da = self.derivative.toFunction()
            self.str_function_da = self.derivative.toString()

        # Newton's difference quotient
        self.function_dq = "((({})-({}))/h)".format(self.function, self.function.replace("x","(x+h)"))
        self.str_function_dq = "((({})-({}))/h)".format(self.str_function, self.str_function.replace("x","(x+h)"))

    def getDifferenceQuotion(self, x, depth=1, h=0.0000001):
        if( depth == 1 ):
            return eval(self.function_dq)
        return (self.getDifferenceQuotion(x+h, depth=(depth-1), h=h)-self.getDifferenceQuotion(x, depth=(depth-1), h=h))/h

    def getRiemannIntegrals(self, left, right):
        delta = ( (right-left) / 1000)   # width
        j = abs( (right-left) / delta)   # cal time in float
        i = int(j)                  # cal time in int

        n = 0       # Counter
        A = 0.0     # Area
        x = left

        while n < i:
            delta_A = float(eval(self.function)) * delta
            x += delta
            A += delta_A
            n = n+1
            
        return format(A, ".5f") # 5 decimal digit

    def parse(self, root=None):
        node = self.getNode()
        if ( type(node) != notation.Number 
                and type(node) != notation.X 
                and type(node) != notation.P ):
            self.func = self.func[2:]               #remove notation and (
            node.nodeLeft = self.parse(node)
            if(self.func[0] == ','):                #Check if it has the right side
                self.func = self.func[1:]
                node.nodeRight = self.parse(node)
            self.func = self.func[1:]               #remove )

        elif ( type(node) == notation.Number ):
            while ( self.func[0] != ',' and self.func[0] != ')' ):
                node.data += self.func[0]
                self.func = self.func[1:]
        else:
            self.func = self.func[1:]
        return node
    
    def getNode(self):
        node = notation.Number()
        if ( self.func[0:2] == "n(" ):
            node = notation.N()
        elif ( self.func[0:2] == "r(" ):
            node = notation.R()
        elif ( self.func[0:2] == "+(" ):
            node = notation.Add()
        elif ( self.func[0:2] == "*(" ):
            node = notation.Mul()
        elif ( self.func[0:2] == "-(" ):
            node = notation.Sub()
        elif ( self.func[0:2] == "/(" ):
            node = notation.Div()
        elif ( self.func[0:2] == "^(" ):
            node = notation.Pow()
        elif ( self.func[0:2] == "s(" ):
            node = notation.S()
        elif ( self.func[0:2] == "c(" ):
            node = notation.C()
        elif ( self.func[0:2] == "e(" ):
            node = notation.E()
        elif ( self.func[0:2] == "l(" ):
            node = notation.Ln()
        elif ( self.func[0:2] == "!(" ):
            node = notation.Fac()
        elif ( self.func[0:1] == "p" ):
            node = notation.P()
        elif ( self.func[0:1] == 'x' ):
            node = notation.X()
        elif( self.func[0] == ',' or self.func[0] == ')'):
            node = None
        return node

if __name__ == "__main__":
    parse = Parse("/(1,^(+(x,3),3)))")
    print(parse.function)
    print(parse.function_da)
    print(parse.function_dq)
    print(parse.str_function)
    print(parse.str_function_da)
    print(parse.str_function_dq)