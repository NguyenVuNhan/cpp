import notation

class Parse:
    def __init__(self, func):
        #Static id for each node
        self.i = 1
        self.func = func.replace(' ', '')+')'
        self.root = self.parse().simplify()
        
        self.function = self.root.toFunction()
        self.function_da = "None"
        self.function_dd = "None"

        self.str_function = self.root.toString()
        self.str_function_da = "None"
        self.str_function_dd = "None"
        """
            Derivative
        """
        # Analyticaly
        self.derivative = self.root.getDerivative()
        print(self.derivative)
        if ( self.derivative != None ):
            self.derivative = self.derivative.simplify()
            self.function_da = self.derivative.toFunction()
        self.str_function_da = self.derivative.toString()
        # Newton's difference quotient
        self.func = func.replace(' ', '').replace("x","+(x,h)")
        print(self.func)
        self.func = "/(-({},{}),h)".format(self.func, func)
        self.differenceQuotion = self.parse().simplify()
        self.function_dd = self.differenceQuotion.toFunction()
        self.str_function_dd = self.differenceQuotion.toString()


    def parse(self, root=None):
        node = self.getNode()
        node.id = self.i
        self.i += 1
        
        if ( type(node) != notation.Number and type(node) != notation.X and type(node) != notation.H ):
            self.func = self.func[2:]               #remove notation and (
            node.nodeLeft = self.parse(node)
            if(self.func[0] == ','):                #Check if it has the right side
                self.func = self.func[1:]
                node.nodeRight = self.parse(node)
            self.func = self.func[1:]               #remove )

        elif ( type(node) == notation.Number ):
            while ( self.func[0] != ',' and
                    self.func[0] != ')' ):
                node.data += self.func[0]
                self.func = self.func[1:]

        elif ( type(node) == notation.X ):
            self.func = self.func[1:]

        elif ( type(node) == notation.H ):
            self.func = self.func[1:]

        return node
    
    def getNode(self):
        node = notation.Number()
        # print(':'+self.func+':')
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
        elif ( self.func[0:2] == "p(" ):
            node = notation.P()
        elif ( self.func[0] == 'x' ):
            node = notation.X()
        elif ( self.func[0] == 'h' ):
            node = notation.H()

        return node

# p = Parse("^(x,2)")
# print(p.derivative.toString())
# print(p.differenceQuotion.toString())
# # newroot.toString()