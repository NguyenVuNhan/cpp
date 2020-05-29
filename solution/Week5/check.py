from tkinter import *
from tkinter import messagebox
from urllib.request import urlretrieve
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure, Toplevel
import matplotlib.image as mpimg
# import matplotlib.pyplot as plt
import os

class validateTk:
    def __init__(self, imgDir=None, func="x", xMin=-10, xMax=10, yMin=-10, yMax=10):
        self.root = Tk()

        self.width = 850
        self.height = 525
        if ( imgDir != None ):
            img = mpimg.imread(imgDir)
            pass
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
            image_w={}&\
            image_h={}".format(func, xMin, xMax, yMin, yMax, self.width, self.height).replace(" ","")
            try:
                urlretrieve(url, filename="tmp.png")
                img = mpimg.imread('tmp.png')
                os.remove("tmp.png")
                pass
            except:
                messagebox.showerror("Error", "Somethings gone wrong, please try again later")
                return

        fig = Figure(figsize=(self.width, self.height))
        top = Toplevel(root)
        self.a = fig.add_subplot(111)
        self.a.set_title("Calculus", fontsize=16)
        self.a.set_ylabel("Y", fontsize=14)
        self.a.set_xlabel("X", fontsize=14)  
        self.a.imshow(img)
        # self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        # self.canvas.draw()
        # self.canvas.get_tk_widget().pack(pady=5)

if __name__ == '__main__':
    form = validateTk()
    form.root.mainloop()
