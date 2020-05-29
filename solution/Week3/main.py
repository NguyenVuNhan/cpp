import numpy
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from tkinter import *
from pygraphviz import *

from parse import Parse

class MainForm:
    def __init__(self):
        self.root = Tk()
        self.root.title("Plot")
        self.root.attributes("-zoomed", True)
        self.title = "Calculus"
        
        # Plot function
        self.parse = None
        self.plotFunction = ""
        self.isFill = False

        # Get root information
        self.root.update()
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        self.__DPI = 110.0  # Average DPI for most monitor
        
        # Justify the plot
        self.left = -10
        self.right = 10
        self.seq = 20
        self.thresshole = 500

        # Loading GUI
        self.GUI()

        # Event Handler
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
    
    def graph(self):
        self.parse_func()
        
        f = open(fn, 'w+')
        f.write("graph "+self.title+" {\n")
        f.write('\tnode [ fontname = "Arial"]\n')
        self.parse.root.toGraph(-1, f)
        f.write('}')
        f.close()

        f = open(fn, 'w+')
        f.write("graph "+self.title+" derivative {\n")
        f.write('\tnode [ fontname = "Arial"]\n')
        self.parse.rootDerivative.toGraph(-1, f)
        f.write('}')
        f.close()

        G = AGraph(fn)
        G.draw('test.png', prog='dot')
        messagebox.showinfo("Info", "Success")

    def plot(self):
        self.parse_func()

        # Plot
        self.a.set_title(self.title, fontsize=16)
        
        if( not self.isFill ):
            t = numpy.linspace(self.left, self.right, (numpy.abs(self.right)+numpy.abs(self.left))*self.seq + 1)
            self.a.plot(t, self.function(t, self.plotFunction, h=0.0000000001), color='red')
        else:
            t = numpy.linspace(int(self.left_bound.get()), int(self.right_bound.get()), (numpy.abs(int(self.left_bound.get()))+numpy.abs(int(self.right_bound.get())))*self.seq + 1)
            print(self.parse.function)
            self.a.fill_between(t, 0, self.function(t, self.parse.function), color="green")

        self.canvas.draw()        

    def parse_func (self):
        try:
            self.parse = Parse(self.input.get())
        except Exception as e:
            messagebox.showerror("Error", "Somethings gone wrong, please check your input again")
            print(str(e))
            return

        self.lbl_function.set(self.parse.str_function)
        self.lbl_derivative.set(self.parse.str_function_da)
        self.lbl_derivative_dq.set(self.parse.str_function_dq)
        try:
            self.lbl_riemann.set(self.parse.getRiemannIntegrals(float(self.left_bound.get()), float(self.right_bound.get())))
        except Exception as e:
            messagebox.showerror("Error", "Somethings gone wrong, please check your input again")
            print(str(e))
            return

    
    def function(self, t, str_func, h=0.0000000001):
        print(str_func)
        y = numpy.zeros(len(t))            # allocate y with float elements
        for i in range(len(t)):
            x = t[i]
            try:
                y[i] = eval(str_func)
                lim = (y[i-1] + y[i])/2 + self.thresshole
                if( numpy.abs(y[i-1]) > lim and numpy.abs(y[i]) > lim ):
                    if ( y[i-1] > 0 ):
                        y[i-1] = numpy.PINF
                        y[i] = numpy.NINF
                    else:
                        y[i-1] = numpy.NINF
                        y[i] = numpy.PINF
            except:
                y[i] =  numpy.NAN
        return y

    def clearPlot(self):
        self.a.clear()
        self.a.grid(True)
        self.canvas.draw()

    def on_key_hover(self, event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, self.canvas, self.toolbar)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.root.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)
        return "break"

    def setPlotFunction(self, func):
        self.plotFunction = func
        print(self.plotFunction)
        isFill = False

    def riemannIntegrals(self):
        self.isFill = True

    def GUI(self):
         #==========================================================================
        # Top Frame
        #==========================================================================
        self.topFrame = Frame(self.root, width=self.width, bd = 2, relief = "raise")
        self.topFrame.pack(side=TOP, fill=BOTH, expand = True)
        
        """
            Top Left
        """
        self.topFrameLeft = Frame(self.topFrame, width=self.width/2)
        self.topFrameLeft.pack(side=LEFT, expand = True)
        # Label
        self.lbl_function = StringVar()
        self.lbl_function.set("None")
        self.lbl_derivative = StringVar()
        self.lbl_derivative.set("None")
        self.lbl_derivative_dq = StringVar()
        self.lbl_derivative_dq.set("None")
        self.lbl_riemann = StringVar()
        self.lbl_riemann.set("None")
        Label(self.topFrameLeft, text = "Input").grid(row=0, column=0, sticky=W, padx=2)
        Label(self.topFrameLeft, text = "Function:").grid(row=1, column=0, sticky=W, padx=2)
        Label(self.topFrameLeft, textvariable = self.lbl_function).grid(row=1, column=1, sticky=W, padx=2)
        Label(self.topFrameLeft, text = "Derivative:").grid(row=2, column=0, sticky=W, padx=2)
        Label(self.topFrameLeft, textvariable = self.lbl_derivative).grid(row=2, column=1, sticky=W, padx=2)
        Label(self.topFrameLeft, text = "Difference quotion:").grid(row=3, column=0, sticky=W, padx=2)
        Label(self.topFrameLeft, textvariable = self.lbl_derivative_dq).grid(row=3, column=1, sticky=W, padx=2)
        Label(self.topFrameLeft, text = "Riemann quotion:").grid(row=4, column=0, sticky=W, padx=2)
        Label(self.topFrameLeft, textvariable = self.lbl_riemann).grid(row=4, column=1, sticky=W, padx=2)
        # Input field
        self.input = Entry(self.topFrameLeft, width=30)
        self.input.grid(row=0, column=1, sticky=W, padx=2)
        # Button
        Button(self.topFrameLeft, text="Parse", command=self.parse_func).grid(row=0, column=2,sticky=W, padx=2)
        
        """
            Top Right
        """
        self.topFrameRight = Frame(self.topFrame, width=self.width/2)
        self.topFrameRight.pack(side=LEFT, expand = True)
        ### Right
        self.frameRightOption = Frame(self.topFrameRight)
        self.frameRightOption.pack(side = LEFT, expand = True)
        #Button
        Button(self.frameRightOption, text="Plot", command=self.plot).grid(row=0, column=0, columnspan=1, rowspan=4, padx=2)
        # Input
        self.left_bound = Entry(self.frameRightOption, width=5)
        self.left_bound.insert(0, self.left)
        self.left_bound.grid(row=3, column=2, sticky=W, padx=2)
        self.right_bound = Entry(self.frameRightOption, width=5)
        self.right_bound.insert(0, self.right)
        self.right_bound.grid(row=3, column=3, sticky=W, padx=2)
        # Ratio button
        v = IntVar()
        v.set(0)
        Radiobutton(self.frameRightOption, 
                    text="Parsed function", 
                    padx=2, pady=2, 
                    command=lambda: self.setPlotFunction( ("0" if (self.parse == None) else self.parse.function) ),
                    variable=v, 
                    value=0).grid(row=0, column=1, padx=2, sticky=W)
        Radiobutton(self.frameRightOption, 
                    text="Function derivative", 
                    padx=2, pady=2, 
                    command=lambda: self.setPlotFunction( ("0" if (self.parse == None) else self.parse.function_da) ),
                    variable=v, 
                    value=1).grid(row=1, column=1, padx=2, sticky=W)
        Radiobutton(self.frameRightOption, 
                    text="Function diferrence quotion", 
                    padx=2, pady=2, 
                    command=lambda: self.setPlotFunction( ("0" if (self.parse == None) else self.parse.function_dq) ),
                    variable=v, 
                    value=2).grid(row=2, column=1, padx=2, sticky=W)
        Radiobutton(self.frameRightOption, 
                    text="Riemann integrals", 
                    padx=2, pady=2, 
                    command=self.riemannIntegrals,
                    variable=v, 
                    value=3).grid(row=3, column=1, padx=2, sticky=W)

        ### Left
        self.frameRightButton = Frame(self.topFrameRight)
        self.frameRightButton.pack(side = LEFT, expand = True, padx=50)
        # Button
        Button(self.frameRightButton, text="Export Graph", command=self.graph).grid(row=0, column=0, padx=2, sticky=E)
        Button(self.frameRightButton, text="Clean Canvas", command=self.clearPlot).grid(row=0, column=1, padx=2, sticky=E)

        #==========================================================================
        # Bottom Frame
        #==========================================================================
        self.bottomFrame = Frame(self.root, width=self.width, bd = 2, relief = "raise")
        self.bottomFrame.pack(side=TOP, fill=BOTH, expand = True)
        """
            Ploting
        """
        # Figure
        fig = Figure(figsize=(self.width/self.__DPI, self.height/self.__DPI-1))
        self.a = fig.add_subplot(111)  
        self.a.set_title ("Calculus", fontsize=16)
        self.a.set_ylabel("Y", fontsize=14)
        self.a.set_xlabel("X", fontsize=14)      
        self.a.plot([], [], color='red')
        self.a.grid(True)
        self.canvas = FigureCanvasTkAgg(fig, master=self.bottomFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=5)
        # Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.bottomFrame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()

if __name__ == '__main__':
    form = MainForm()
    form.canvas.mpl_connect("key_press_event", form.on_key_hover)
    form.root.mainloop()