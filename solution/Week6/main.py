#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from statistics import Poisson, Exponential
from tkinter import *
from tkinter import messagebox

import matplotlib
import numpy as np
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure
from math import sqrt

matplotlib.use('TkAgg')

class MainForm:
    def __init__(self):
        # Global var
        self.poisson = Poisson()
        self.exponential = Exponential()

        self.sInterval = 10
        self.sEvent = 100000
        self.sLamda = 0.5

        self.font = { 'family': 'serif',
            'color':  'darkred',
            'weight': 'normal',
            'size': 16,
        }

        # UI design
        self.GUI()

        # Event Handler
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
        self.canvas.mpl_connect("key_press_event", self.on_key_hover)

    def poissonPlot(self):
        self.clearPlot()

        try:
            lam = int(self.pLamda.get())
        except Exception as e:
            messagebox.showerror("Error", "Somethings gone wrong, please check your lamda again")
            print(str(e))
            return

        _hist, _plot = self.poisson.histogramPlot(lam)

        # With formular
        self.a.plot(_plot[0], _plot[1], color="#0000FF")

        # With random
        self.a.bar(_hist[0], _hist[1], color="#FFA500")

        
        self.a.text(lam*10, 0.12, "mean: {}".format(self.poisson.mean), fontdict=self.font)
        self.a.text(lam*10, 0.11, "variance: {}".format(self.poisson.variance), fontdict=self.font)
        self.a.text(lam*10, 0.1, "standard deviation: {}".format(sqrt(self.poisson.variance)), fontdict=self.font)
        self.canvas.draw()

    def exponentialPlot(self):
        self.clearPlot()

        try:
            lam = float(self.eLamda.get())
        except Exception as e:
            messagebox.showerror("Error", "Somethings gone wrong, please check your lamda again")
            print(str(e))
            return

        _hist, _plot = self.exponential.histogramPlot(lam)

        # With formular
        self.a.plot(_plot[0], _plot[1], color="#0000FF")
        # With random
        self.a.bar(_hist[0], _hist[1], color="#FFA500")

        self.a.text(50, 0.12, "mean: {}".format(self.exponential.mean), fontdict=self.font)
        self.a.text(50, 0.11, "variance: {}".format(self.exponential.variance), fontdict=self.font)
        self.a.text(50, 0.1, "standard deviation: {}".format(sqrt(self.exponential.variance)), fontdict=self.font)

        self.canvas.draw()

    def provePlot(self):
        self.clearPlot()
        # ex_mean = 0
        tmp = 0
        count = 0
        data = []
        counts = np.zeros(100)
        for i in range(self.sEvent):
            tmp += self.exponential.random(self.sLamda)
            # tmp += np.random.exponential(self.sLamda)
            count += 1
            if( tmp >= self.sInterval ):
                data.append(count)
                try:
                    counts[count] += 1
                except:
                    pass
                tmp -= self.sInterval
                count = 0

        data_len = len(data)

        mean = sum(data)/data_len
        variance = 0
        for i in data:
            variance += ((i-mean)**2)
        variance /= data_len

        _d = (min(data)+max(data))/100
        self.a.plot(range(100), [self.poisson.pmf((self.sLamda)*self.sInterval, i) for i in range(100)], color="orange")
        self.a.bar(range(100), [count/data_len for count in counts], color="blue")
        self.a.text(80, 0.02, "mean: {}".format(mean), fontdict=self.font)
        self.a.text(80, 0.01, "variance: {}".format(variance), fontdict=self.font)
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
        ###Poisson
        poissonFrame = Frame(botFrame, bd=2, relief="raise")
        poissonFrame.pack(side=LEFT, fill=BOTH, expand=True)
        # Iteration
        Label(poissonFrame, text = "Iteration").grid(row=0, column=0, padx=2)
        pInteration = StringVar()
        pInteration.set(str(self.poisson.iteration))
        pInteration.trace("w", lambda name, index, mode, sv=pInteration : self.pIteration_changed(sv))
        Entry(poissonFrame, textvariable=pInteration, width=8).grid(row=0, column=1, padx=2)
        # Sequence
        Label(poissonFrame, text = "Sequence").grid(row=1, column=0, padx=2)
        pSequence = StringVar()
        pSequence.set(str(self.poisson.sequence))
        pSequence.trace("w", lambda name, index, mode, sv=pSequence : self.pSequence_changed(sv))
        Entry(poissonFrame, textvariable=pSequence, width=8).grid(row=1, column=1, padx=2)
        # Lamda
        Label(poissonFrame, text = "Lamda").grid(row=2, column=0, padx=2)
        self.pLamda = StringVar()
        Entry(poissonFrame, textvariable=self.pLamda, width=8).grid(row=2, column=1, padx=2)
        # Button
        Button(poissonFrame, text="Poisson", command=self.poissonPlot, width=10).grid(row=0, column=2, rowspan=3, padx=2)

        ### Exponential
        exponentialFrame = Frame(botFrame, bd=2, relief="raise")
        exponentialFrame.pack(side=LEFT, fill=BOTH, expand=True)
        # Iteration
        Label(exponentialFrame, text = "Iteration").grid(row=0, column=0, padx=2)
        eInteration = StringVar()
        eInteration.set(str(self.exponential.iteration))
        eInteration.trace("w", lambda name, index, mode, sv=eInteration : self.eIteration_changed(sv))
        Entry(exponentialFrame, textvariable=eInteration, width=8).grid(row=0, column=1, padx=2)
        # Lamda
        Label(exponentialFrame, text = "Lamda").grid(row=1, column=0, padx=2)
        self.eLamda = StringVar()
        Entry(exponentialFrame, textvariable=self.eLamda, width=8).grid(row=1, column=1, padx=2)
        # Button
        Button(exponentialFrame, text="Exponential", command=self.exponentialPlot, width=10).grid(row=0, column=2, rowspan=2, padx=2)
        
        ###Simulate
        simulateFrame = Frame(botFrame, bd=2, relief="raise")
        simulateFrame.pack(side=LEFT, fill=BOTH, expand=True)
        # Interval
        Label(simulateFrame, text = "Interval").grid(row=0, column=0, padx=2)
        sInterval = StringVar()
        sInterval.set(str(self.sInterval))
        sInterval.trace("w", lambda name, index, mode, sv=sInterval : self.sInterval_changed(sv))
        Entry(simulateFrame, textvariable=sInterval, width=8).grid(row=0, column=1, padx=2)
        # Event
        Label(simulateFrame, text = "Event").grid(row=1, column=0, padx=2)
        sEvent = StringVar()
        sEvent.set(str(self.sEvent))
        sEvent.trace("w", lambda name, index, mode, sv=sEvent : self.sEvent_changed(sv))
        Entry(simulateFrame, textvariable=sEvent, width=8).grid(row=1, column=1, padx=2)
        # Lamda
        Label(simulateFrame, text = "Lamda").grid(row=2, column=0, padx=2)
        sLamda = StringVar()
        sLamda.set(str(self.sLamda))
        sLamda.trace("w", lambda name, index, mode, sv=sLamda : self.sLamda_changed(sv))
        Entry(simulateFrame, textvariable=sLamda, width=8).grid(row=2, column=1, padx=2)
        Button(simulateFrame, text="Prove", command=self.provePlot, width=10).grid(row=0, column=3, rowspan=3, padx=2)

        #endregion
        # ==========================================================================

#region Event
    def sInterval_changed(self, sv):
        self.sInterval = int(sv.get())

    def sLamda_changed(self, sv):
        self.sLamda = int(sv.get())

    def sEvent_changed(self, sv):
        self.sEvent = int(sv.get())

    def eIteration_changed(self, sv):
        self.exponential.iteration = int(sv.get())

    def pIteration_changed(self, sv):
        self.poisson.iteration = int(sv.get())

    def pSequence_changed(self, sv):
        self.statistic.sequence = int(sv.get())

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
