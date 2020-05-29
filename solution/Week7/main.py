#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox

import matplotlib
import numpy as np
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.image as mpimg
from math import sqrt, log
from random import uniform

from graph import Graph

matplotlib.use('TkAgg')

class MainForm:
    def __init__(self):
        # Global var
        self.font = { 'family': 'serif',
            'color':  'darkred',
            'weight': 'normal',
            'size': 16,
        }

        # UI design
        self.GUI()

        self.__G = Graph()

        # Event Handler
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
        self.canvas.mpl_connect("key_press_event", self.on_key_hover)

    def generateGraph(self, n, p):
        self.__G.clear()
        for i in range(n):
            self.__G.add_vertex(i)
            for j in range(i+1, n):
                if ( uniform(0,1) < p ):
                    self.__G.add_edge(i, j)
                    self.__G.add_edge(j, i)

    def showGraph(self):
        n=int(self.edges.get())
        p=float(self.probality.get())
        self.generateGraph(n, p)

        self.clearPlot()
        self.__G.draw("network.png")
        connected = self.__G.isConnected()
        self.a.text(0,1, "Graph connected" if connected else "Graph not connected", fontdict=self.font)
        self.canvas.draw()
    
    def randomGraph(self, n, p):
        self.generateGraph(n, p)
        return self.__G.isConnected()

    def experimence(self):
        n=int(self.edges.get())
        m=int(self.event.get())

        self.clearPlot()
        a = []
        for p in np.linspace(0,1,101):
            count = 0
            for i in range(m):
                if(self.randomGraph(n, p)):
                    count += 1
            a.append(count)

        self.a.text(0, 0.9*m, "{}*ln({})={}".format(n, n, log(n)*n), fontdict=self.font)
        # self.a.plot(np.linspace(1/1000,1,1001), [i/log(i) for i in np.linspace(1/1000,1,1001)], color="orange")
        self.a.plot(np.linspace(0,1,101), a, color="blue")
        self.canvas.draw()

    def clearPlot(self):
        self.a.clear()
        self.a.grid(True)
        self.canvas.draw()

    def GUI(self):
        # ==========================================================================
        #region Preconfig
        # ==========================================================================
        self.root = Tk()
        self.root.title("Plot")
        self.root.attributes("-zoomed", True)
        title = "Statistic"

        # Get root information
        self.root.update()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        __DPI = 110.0  # Average DPI for most monitor

        #endregion
        # ==========================================================================
        
        # ==========================================================================
        #region Top Frame
        # ==========================================================================
        topFrame = Frame(self.root, width=width, bd=2, relief="raise")
        topFrame.pack(side=TOP, fill=BOTH, expand=True)
        """
            Ploting
        """
        #Figure
        fig = Figure(figsize=(width/__DPI, height/__DPI-1))
        self.a = fig.add_subplot(111)
        self.a.set_title("Calculus", fontsize=16)
        self.a.set_ylabel("Y", fontsize=14)
        self.a.set_xlabel("X", fontsize=14)
        self.a.plot([], [], color='red')
        self.a.grid(True)
        self.canvas = FigureCanvasTkAgg(fig, master=topFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(pady=5)
        # Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, topFrame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()

        #endregion
        # ==========================================================================

        # ==========================================================================
        #region Bottom Frame
        # ==========================================================================
        botFrame = Frame(self.root, width=width, bd=2, relief="raise")
        botFrame.pack(side=TOP, fill=BOTH, expand=True)
        """
            Option
        """
        frameCenter = Frame(botFrame)
        frameCenter.pack(side=TOP)
        # edges
        Label(frameCenter, text = "edges").grid(row=0, column=0, padx=2)
        self.edges = StringVar()
        self.edges.set("10")
        Entry(frameCenter, textvariable=self.edges, width=8).grid(row=0, column=1, padx=2)
        # probality
        Label(frameCenter, text = "probality").grid(row=1, column=0, padx=2)
        self.probality = StringVar()
        self.probality.set("0.5")
        Entry(frameCenter, textvariable=self.probality, width=8).grid(row=1, column=1, padx=2)
        # Events
        Label(frameCenter, text = "Experiments").grid(row=2, column=0, padx=2)
        self.event = StringVar()
        self.event.set("1000")
        Entry(frameCenter, textvariable=self.event, width=8).grid(row=2, column=1, padx=2)
        # Button
        Button(frameCenter, text="Open graph", command=self.showGraph, width=10).grid(row=0, column=2, rowspan=2, padx=2)
        Button(frameCenter, text="Experimence", command=self.experimence, width=10).grid(row=2, column=2, rowspan=2, padx=2)

        #endregion
        # ==========================================================================

#region Event
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
#endregion

if __name__ == '__main__':
    form = MainForm()
    form.root.mainloop()
