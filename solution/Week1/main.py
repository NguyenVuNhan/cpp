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
        
        # Get root information
        self.root.update()
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        self.__DPI = 110.0  # Average DPI for most monitor
        
        #Loading GUI
        self.GUI()

        # Event Handler
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
    
    def graph(self):
        self.parse = Parse(self.input.get())
        fn = self.title + '.dot'

        try:
            print(self.parse.function)
        except:
            messagebox.showerror("Error", "Somethings gone wrong, please check your input again")
            return
        
        f = open(fn, 'w+')
        f.write("graph calculus {\n")
        f.write('\tnode [ fontname = "Arial"]\n')
        self.parse.root.toGraph(-1, f)
        f.write('}')
        f.close()

        G = AGraph(fn)
        G.draw('test.png', prog='dot')
        messagebox.showinfo("Info", "Success")

    def plot (self):
        self.parse = Parse(self.input.get())
        try:
            print(self.parse.function)
        except:
            messagebox.showerror("Error", "Somethings gone wrong, please check your input again")
            return
        t = numpy.linspace(self.left, self.right, (self.right-self.left)*self.seq+1)
        y = numpy.zeros(len(t))            # allocate y with float elements
        thresshole = 100
        for i in range(len(t)):
            x = t[i]
            try:
                y[i] = eval(self.parse.function)
                if((y[i-1] + y[i])/2 > thresshole):
                    y[i-1] = numpy.nan
                    y[i] = numpy.nan
            except:
                y[i] = numpy.nan
                pass

        self.a.clear()
        self.a.set_title(self.title, fontsize=16)
        self.a.plot(t, y, color='red')
        self.canvas.draw()
    
    def on_key_hover(event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, canvas, toolbar)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.root.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)
        return "break"

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
        Label(self.topFrameLeft, text = "Input").grid(row=0, column=0, sticky=W, padx=2)
        # Input field
        self.input = Entry(self.topFrameLeft, width=30)
        self.input.grid(row=0, column=1, sticky=W, padx=2)
        # Button
        Button(self.topFrameLeft, text="Parse", command=self.plot).grid(row=0, column=2, sticky=W, padx=2)
        
        """
            Top Right
        """
        self.topFrameRight = Frame(self.topFrame, width=self.width/2)
        self.topFrameRight.pack(side=LEFT, expand = True)
        # Button
        self.btnGraph = Button(self.topFrameRight, text="Export Graph", command=self.graph)
        self.btnGraph.pack()

        #==========================================================================
        # Bottom Frame
        #==========================================================================
        self.bottomFrame = Frame(self.root, width=self.width, bd = 2, relief = "raise")
        self.bottomFrame.pack(side=TOP, fill=BOTH, expand = True)
        """
            Ploting
        """
        # Justify the plot
        self.left = -10
        self.right = 10
        self.seq = 1000
        # Figure
        fig = Figure(figsize=(self.width/self.__DPI, self.height/self.__DPI))
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
