#!/usr/bin/env python3

import numpy                # Numeric solving
import matplotlib           # Plot
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tkinter import *       # UI
from pygraphviz import *    # Tree
from webbrowser import open_new_tab

from urllib.request import urlretrieve
from PIL import ImageTk, Image
import os

from parse import Parse
from matrix import Matrix
import notation

class MainForm:
    def __init__(self):
        self.root = Tk()
        self.root.title("Plot")
        self.root.attributes("-zoomed", True)
        self.title = "Calculus"

        #################################################################
        # User congfig area
        #################################################################
        
        # Global config
        self.getVectorMethod = "Gaussian"
        self.getMcLaurinSeriesMethod = "Analytically"
        # Justify the plot
        self.left = -50
        self.right = 50
        self.seq = 1000
        self.thresshole = 500

        #################################################################
        # End user config area
        #################################################################
        
        # Plot function
        self.parse = None
        self.option = "root"
        self.inputChanged = False

        # Get root information
        self.root.update()
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        self.__DPI = 110.0  # Average DPI for most monitor
        self.root.geometry("{}x{}".format(self.width, self.height))
        
        # Matrix
        self.matrix = Matrix()
        self.saveSetPoint = False

        # Loading GUI
        self.GUI()

        # Event Handler
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
    
    def graph(self):
        self.parse_func()

        # Root
        f = open("calculus.dot", 'w+')
        f.write("graph "+self.title+" {\n")
        f.write('\tnode [ fontname = "Arial"]\n')
        self.parse.root.toGraph(-1, f)
        f.write('}')
        f.close()

        G = AGraph("calculus.dot")
        G.draw("calculus.png", prog='dot')

        # Derivative analyticaly
        f = open("derivative.dot", 'w+')
        f.write("graph derivative {\n")
        f.write('\tnode [ fontname = "Arial"]\n')
        if( self.parse.derivative != None):
            self.parse.derivative.toGraph(-1, f)
        f.write('}')
        f.close()
        
        G = AGraph("derivative.dot")
        G.draw("derivative.png", prog='dot')
        messagebox.showinfo("Info", "Success")

    def plot(self):
        self.parse_func()

        # Plot
        self.a.set_title(self.title, fontsize=16)
        
        if ( self.option == "root" ):
            t = numpy.linspace(self.left, self.right, (numpy.abs(self.right)+numpy.abs(self.left))*self.seq + 1)
            self.a.plot(t, self.function(t, self.parse.function, h=0.0000000001), color='red')
            title = self.parse.str_function

        elif ( self.option == "da" ):
            t = numpy.linspace(self.left, self.right, (numpy.abs(self.right)+numpy.abs(self.left))*self.seq + 1)
            self.a.plot(t, self.function(t, self.parse.function_da, h=0.0000000001), color='blue')
            title = self.parse.str_function_da

        elif ( self.option == "dq" ):
            t = numpy.linspace(self.left, self.right, (numpy.abs(self.right)+numpy.abs(self.left))*self.seq + 1)
            self.a.plot(t, self.function(t, self.parse.function_dq, h=0.0000000001), color='orange')
            title = self.parse.str_function_dq

        elif ( self.option == "fill" ):
            t = numpy.linspace(int(self.left_bound.get()), int(self.right_bound.get()), (numpy.abs(int(self.left_bound.get()))+numpy.abs(int(self.right_bound.get())))*self.seq + 1)
            self.a.fill_between(t, 0, self.function(t, self.parse.function), color="green")
            title = "Area: {}".format(self.lbl_riemann)

        elif ( self.option == "McLaurin" ):
            vector = self.getMcLaurinVector(0, depth=int(self.depth_input.get()), method=self.getMcLaurinSeriesMethod)
            mclaurrin = "{}".format(vector[0])
            for i in range(1,len(vector)):
                mclaurrin += "+{}*x^{}".format(vector[i], i)

            t = numpy.linspace(self.left, self.right, (numpy.abs(self.right)+numpy.abs(self.left))*self.seq + 1)
            y = numpy.zeros(len(t))            # allocate y with float elements
            for i in range(len(t)):
                try:
                    y[i] = vector[0]
                    for j in range(1,len(vector)):
                        y[i] += vector[j]*t[i]**j
                except Exception as ex:
                    y[i] = numpy.NAN

            self.a.plot(t, y, color='yellow')
            title = mclaurrin
        self.a.set_title(title, fontsize=8)  
        self.canvas.draw()        

    def parse_func (self):
        if( self.inputChanged ):
            try:
                print(self.input.get())
                self.parse = Parse(self.input.get().replace(" ", ""))
            except Exception as e:
                messagebox.showerror("Error", "Somethings gone wrong, please check your input again")
                print(e)
                return
            self.lbl_function.set(self.parse.str_function)
            self.lbl_derivative.set(self.parse.str_function_da)
            self.lbl_derivative_dq.set(self.parse.str_function_dq)
            try:
                self.lbl_riemann.set(self.parse.getRiemannIntegrals(float(self.left_bound.get()), float(self.right_bound.get())))
            except Exception as e:
                messagebox.showerror("Error", "Somethings gone wrong, please check your input again")
                print(e)
                return
            self.inputChanged = False
    
    def function(self, t, str_func, h=0.0000000001):
        y = numpy.zeros(len(t))            # allocate y with float elements
        for i in range(len(t)):
            x = t[i]
            try:
                y[i] = eval(str_func)
                if ( abs(y[i]) > self.thresshole ):
                    y[i] = numpy.NAN
                    pass
            except Exception as ex:
                print(ex)
                y[i] = numpy.NAN
        return y

    def clearPlot(self):
        self.a.clear()
        self.a.grid(True)
        self.a.set_title("Calculus", fontsize=16)
        self.canvas.draw()

    def setPlotFunction(self, option="linear", func="0"):
        self.option = option

    def getMcLaurinSeries(self, x, x0, depth=1, h=0.000001):
        S = eval(self.parse.function)
        for i in range(1, depth):
            S += (self.parse.getDifferenceQuotion(x, depth=i, h=h)*((x0-x)**i))/numpy.math.factorial(i)
        return S

    def getMcLaurinVector(self, x, depth=1, method="Newton"):
        depth += 1
        if( method == "Newton" ):
            vector = []
            try:
                vector.append(eval(self.parse.function))
            except Exception as ex:
                messagebox.showerror("Error!", "Invalid function. Please check your input again!")
                print(ex)
                return []

            for i in range(1, depth):
                try:
                    vector.append(self.parse.getDifferenceQuotion(x, depth=i)/numpy.math.factorial(i))
                except Exception as ex:
                    messagebox.showerror("Error!", "Invalid derivative at depth {}. Please try other function!".format({i}))
                    print(ex)
                    return []
            return vector
        elif( method == "Analytically" ):
            vector = []
            derivative = self.parse.root
            try:
                vector.append(eval(derivative.toFunction()))
            except Exception as ex:
                messagebox.showerror("Error!", "Invalid function. Please check your input again!")
                print(ex)
                return []

            for i in range(1, depth):
                derivative = derivative.getDerivative()
                derivative = derivative.simplify() if derivative != None else notation.Number(data="0")
                try:
                    vector.append(eval(derivative.toFunction())/numpy.math.factorial(i))
                except Exception as ex:
                    messagebox.showerror("Error!", "Invalid derivative at depth {}. Please try other function!".format({i}))
                    print(ex)
                    return []
            return vector

        return []
            
    def setRecordSetpointMode(self, option=False):
        self.saveSetPoint = option

        if ( option == False ):
            if ( self.matrix.setPointLen == 0 ):
                messagebox.showerror("Set point is empty")
                return
            # Plot
            v = self.matrix.getVector(method=self.getVectorMethod)

            if(v == []):
                messagebox.showerror("Error", "Your setpoints is not continuos")
                self.matrix.refresh()
                return

            t = numpy.linspace(self.left, self.right, (numpy.abs(self.right)+numpy.abs(self.left))*self.seq + 1)
            y = numpy.zeros(len(t))            # allocate y with float elements
            for i in range(len(t)):
                for j in range(len(v)):
                    y[i] += v[j]*(t[i]**j)

            self.lbl_recordSetpoint.set("Setpoint record tunred off")
    
            poly = "{:.4f}".format(round(v[0], 4))
            if(self.matrix.setPointLen >= 2):
                poly += " + {:.4f}*x".format(round(v[1], 4))
                for i in range(2, self.matrix.setPointLen):
                    poly += " + {:.4f}*x^{}".format(round(v[i], 4), i)
                    if (i%4 == 0):
                        poly += "\n"

            self.a.set_title(poly, fontsize=8)
            self.matrix.refresh()
            self.a.plot(t, y, color='blue')
            self.canvas.draw()
        else:
            self.lbl_recordSetpoint.set("Setpoint record tunred on")

    def showSetPoint(self):
        points = self.matrix.setPoint
        message = "x\ty\n"
        for tmpMsg in points:
            message += "{:.4f}\t{:.4f}\n".format(tmpMsg[0], tmpMsg[1])
        messagebox.showinfo("Setpoint", message)

    def showPicture(self, imgDir=None):
        self.parse_func()

        if ( imgDir != None ):
            img = mpimg.imread(imgDir)
        else:
            url = "https://www.graphsketch.com/render.php?\
            eqn1_color=1&\
            eqn1_eqn={}&\
            x_min={}&x_max={}&\
            y_min={}&y_max={}&\
            x_tick=1&y_tick=1&\
            x_label_freq=5&\
            y_label_freq=5&\
            do_grid=0&\
            do_grid=1&\
            bold_labeled_lines=0&\
            bold_labeled_lines=1&\
            line_width=4&\
            image_w=850&\
            image_h=525".format(self.parse.str_function, self.left, self.right, self.left, self.right).replace(" ","")
            try:
                urlretrieve(url, filename="tmp.png")
                img = mpimg.imread('tmp.png')
                os.remove("tmp.png")
            except Exception as e:
                messagebox.showerror("Error", "Somethings gone wrong, please try again later")
                print(e)
                return

        open_new_tab(url.replace("render.php?", "?"))
        plt.imshow(img)
        plt.show()

    def GUI(self):
        # ==========================================================================
        # Top Frame
        # ==========================================================================
        self.bottomFrame = Frame(self.root, width=self.width, bd = 2, relief = "raise")
        self.bottomFrame.pack(side=TOP, fill=BOTH, expand = True)
        """
            Ploting
        """
        # Figure
        fig = Figure(figsize=(self.width/self.__DPI, self.height/self.__DPI-1))
        self.a = fig.add_subplot(111)  
        self.a.set_title("Calculus", fontsize=16)
        self.a.set_ylabel("Y", fontsize=14)
        self.a.set_xlabel("X", fontsize=14)  
        self.a.axhline(linewidth=1, color='black')    
        self.a.axvline(linewidth=1, color='black')    
        self.a.plot([], [], color='red')
        self.a.grid(True)
        self.canvas = FigureCanvasTkAgg(fig, master=self.bottomFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=5)
        # Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.bottomFrame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()

        # ==========================================================================
        # Bottom Frame
        # ==========================================================================
        self.topFrame = Frame(self.root, width=self.width, bd = 2, relief = "raise")
        self.topFrame.pack(side=TOP, fill=BOTH, expand = True)
        
        """
            Top Left
        """
        self.topFrameLeft = Frame(self.topFrame, width=self.width/2)
        self.topFrameLeft.pack(side=LEFT, expand = True)
        ### Left
        self.frameLeft_Lpanel = Frame(self.topFrameLeft)
        self.frameLeft_Lpanel.pack(side = LEFT, expand = True)
        self.frameLeft_Lpanel.grid_propagate(1)
        # Label
        self.lbl_function = StringVar()
        self.lbl_function.set("None")
        self.lbl_derivative = StringVar()
        self.lbl_derivative.set("None")
        self.lbl_derivative_dq = StringVar()
        self.lbl_derivative_dq.set("None")
        self.lbl_riemann = StringVar()
        self.lbl_riemann.set("None")
        Label(self.frameLeft_Lpanel, text = "Input").grid(row=0, column=0, sticky=W, padx=2)
        Label(self.frameLeft_Lpanel, text = "Function:").grid(row=1, column=0, sticky=W, padx=2)
        Label(self.frameLeft_Lpanel, textvariable = self.lbl_function, width=60).grid(row=1, column=1, columnspan=2, sticky=W, padx=2)
        Label(self.frameLeft_Lpanel, text = "Derivative:").grid(row=2, column=0, sticky=W, padx=2)
        Label(self.frameLeft_Lpanel, textvariable = self.lbl_derivative, width=60).grid(row=2, column=1, columnspan=2, sticky=W, padx=2)
        Label(self.frameLeft_Lpanel, text = "Difference quotion:").grid(row=3, column=0, sticky=W, padx=2)
        Label(self.frameLeft_Lpanel, textvariable = self.lbl_derivative_dq, width=60).grid(row=3, column=1, columnspan=2, sticky=W, padx=2)
        Label(self.frameLeft_Lpanel, text = "Riemann quotion:").grid(row=4, column=0, sticky=W, padx=2)
        Label(self.frameLeft_Lpanel, textvariable = self.lbl_riemann, width=60).grid(row=4, column=1, columnspan=2, sticky=W, padx=2)
        # Input field
        self.input = Entry(self.frameLeft_Lpanel, width=30)
        self.input.grid(row=0, column=1, sticky=W, padx=2)
        self.input.bind("<Button-1>", self.input_changed)
        # Button
        Button(self.frameLeft_Lpanel, text="Parse", command=self.parse_func).grid(row=0, column=2,sticky=W, padx=2)
        
        ###Right
        self.frameLeft_Rpanel = Frame(self.topFrameLeft)
        self.frameLeft_Rpanel.pack(side=LEFT, expand = True)
        # Label
        self.lbl_recordSetpoint = StringVar()
        self.lbl_recordSetpoint.set("Off")
        Label(self.frameLeft_Rpanel, text = "Polynomio").grid(row=0, column=0, columnspan=1, sticky=W, padx=2)
        Label(self.frameLeft_Rpanel, textvariable = self.lbl_recordSetpoint).grid(row=0, column=1, columnspan=2, sticky=W, padx=2)
        self.lbl_polynomial = StringVar()
        self.lbl_polynomial.set("")
        Label(self.frameLeft_Rpanel, textvariable = self.lbl_polynomial).grid(row=2, column=0, columnspan=3, sticky=W, padx=2)
        # Button
        Button(self.frameLeft_Rpanel, text="Show setpoint", command=self.showSetPoint).grid(row=1, column=0, padx=2)
        Button(self.frameLeft_Rpanel, text="Record setpoint", command=lambda: self.setRecordSetpointMode(option=True)).grid(row=1, column=1, padx=2)
        Button(self.frameLeft_Rpanel, text="Get polynomial", command=lambda:self.setRecordSetpointMode(option=False)).grid(row=1, column=2, padx=2)

        """
            Top Right
        """
        self.topFrameRight = Frame(self.topFrame, width=self.width/2)
        self.topFrameRight.pack(side=LEFT, expand = True)
        ### Right
        self.frameRightOption = Frame(self.topFrameRight)
        self.frameRightOption.pack(side = LEFT, expand = True)
        #Button
        Button(self.frameRightOption, text="Plot", command=self.plot).grid(row=0, column=0, columnspan=1, rowspan=5, padx=2)
        # Input
        self.left_bound = Entry(self.frameRightOption, width=5)
        self.left_bound.insert(0, self.left)
        self.left_bound.grid(row=3, column=2, sticky=W, padx=2)
        self.right_bound = Entry(self.frameRightOption, width=5)
        self.right_bound.insert(0, self.right)
        self.right_bound.grid(row=3, column=3, sticky=W, padx=2)
        self.a_input = Entry(self.frameRightOption, width=5)
        self.a_input.insert(0, "0")
        self.a_input.grid(row=4, column=2, sticky=W, padx=2)
        self.depth_input = Entry(self.frameRightOption, width=5)
        self.depth_input.insert(0, "8")
        self.depth_input.grid(row=4, column=3, sticky=W, padx=2)
        # Ratio button
        v = IntVar()
        Radiobutton(self.frameRightOption, 
                    text="Parsed function", 
                    padx=2, pady=2, 
                    command=lambda: self.setPlotFunction(option="root"),
                    variable=v, 
                    value=0).grid(row=0, column=1, padx=2, sticky=W)
        Radiobutton(self.frameRightOption, 
                    text="Function derivative", 
                    padx=2, pady=2, 
                    command=lambda: self.setPlotFunction(option="da"),
                    variable=v, 
                    value=1).grid(row=1, column=1, padx=2, sticky=W)
        Radiobutton(self.frameRightOption, 
                    text="Function diferrence quotion", 
                    padx=2, pady=2, 
                    command=lambda: self.setPlotFunction(option="dq"),
                    variable=v, 
                    value=2).grid(row=2, column=1, padx=2, sticky=W)
        Radiobutton(self.frameRightOption, 
                    text="Riemann integrals", 
                    padx=2, pady=2, 
                    command=lambda: self.setPlotFunction(option="fill"),
                    variable=v, 
                    value=3).grid(row=3, column=1, padx=2, sticky=W)
        Radiobutton(self.frameRightOption, 
                    text="Mc Laurin series", 
                    padx=2, pady=2, 
                    command=lambda: self.setPlotFunction(option="McLaurin"),
                    variable=v, 
                    value=4).grid(row=4, column=1, padx=2, sticky=W)
        ### Left
        self.frameRightButton = Frame(self.topFrameRight)
        self.frameRightButton.pack(side = LEFT, expand = True, padx=50)
        # Button
        Button(self.frameRightButton, text="Export Graph", command=self.graph, width=12).grid(row=0, column=0, padx=2, sticky=E)
        Button(self.frameRightButton, text="Clean Canvas", command=self.clearPlot, width=12).grid(row=1, column=0, padx=2, sticky=E)
        Button(self.frameRightButton, text="Validate", command=self.showPicture, width=12).grid(row=2, column=0, padx=2, sticky=E)

    #region Event
    def input_changed(self, event):
        self.inputChanged = True

    def canvas_on_key_hover(self, event):
        key_press_handler(event, self.canvas, self.toolbar)

    def canvas_on_click(self, event):
        if ( self.saveSetPoint == True):
            self.matrix.addSetPoint(float(event.xdata), float(event.ydata))
            self.a.plot(event.xdata, event.ydata, 'rs', color="black")
            self.canvas.draw()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.root.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)
        return "break"

    #endregion

if __name__ == '__main__':
    form = MainForm()
    form.canvas.mpl_connect("key_press_event", form.canvas_on_key_hover)
    form.canvas.mpl_connect("button_press_event", form.canvas_on_click)
    form.root.mainloop()