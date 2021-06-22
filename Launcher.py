"""
##################################################
Instantiates and launches GUI for controlling
the 2 axis stage
##################################################
# Author:   Liam Droog
# Email:    droog@ualberta.ca
# Year:     2021
# Version:  V.1.0.0
##################################################
"""

import tkinter as tk
from StageClass import LIBS_2AxisStage
import serial.tools.list_ports
import os


class StageLauncher:
    def __init__(self):
        # Stuff for launching stage
        self.window = tk.Tk(className='/Launcher')
        self.stage = None
        self.cfg_file = 'Config/stageconfig.cfg'

        # configure grid for widget layout
        self.grid = [5, 2]
        self.rowarr = list(i for i in range(self.grid[0]))
        self.colarr = list(i for i in range(self.grid[1]))
        self.window.rowconfigure(self.rowarr, minsize=0, weight=1)
        self.window.columnconfigure(self.colarr, minsize=0, weight=1)

        self.screenwidth = int(self.window.winfo_screenwidth() * 0.2)
        self.screenheight = int(self.window.winfo_screenheight() * 0.15)
        self.window.geometry(
            '%dx%d+%d+%d' % (self.screenwidth, self.screenheight, self.window.winfo_screenwidth() / 3,
                             self.window.winfo_screenheight() / 5))

        self.stagelabel = tk.Label(master=self.window, text='Stage Control Launcher')
        self.stagelabel.grid(row=0, column=0, columnspan=2, sticky='ew')

        # stage gui launch btn
        self.start_stage_btn = tk.Button(master=self.window, text='Launch Stage Control',
                                         command=self.__startStage)
        self.start_stage_btn.grid(row=4, column=0, columnspan=2, sticky='nsew')

        # Com port
        # Only list com port that has the grbl doohicky connected to it
        self.comlist = [comport.device for comport in serial.tools.list_ports.comports() if 'USB-SERIAL CH340' in comport.description]
        self.comval = tk.StringVar(self.window)
        self.comval.set('Select Com Port')
        self.comlabel = tk.Label(master=self.window, text='COM Port:')
        self.comlabel.grid(row=1, column=0, sticky='news')

        # ensure we actually have a comport
        if len(self.comlist) == 0:
            self.com = tk.OptionMenu(self.window, tk.StringVar(self.window, 'No suitable ports detected'), [])
            self.com.configure(state='disabled')
        else:
            self.com = tk.OptionMenu(self.window, self.comval, *self.comlist)
        self.com.grid(row=1, column=1, sticky='ew')

        # baud
        # most likely 115200 but who am I to limit you?
        baudlist = [9600, 115200]
        self.baudval = tk.IntVar(self.window)
        self.baudval.set('115200')
        self.baudlabel = tk.Label(master=self.window, text='Baud Rate: ')
        self.baudlabel.grid(row=2, column=0, sticky='ew')
        self.baud = tk.OptionMenu(self.window, self.baudval, *baudlist)
        self.baud.grid(row=2, column=1, sticky='ew')

        # startup file
        self.filelabel = tk.Label(master=self.window, text='Startup File: ')
        self.filelabel.grid(row=3, column=0, sticky='ew')
        self.startfile = tk.Entry(master=self.window)
        self.startfile.insert(0, 'Config/startup.txt')
        self.startfile.grid(row=3, column=1, sticky='ew')

        # run a function on closing to clean up & close properly
        self.window.protocol("WM_DELETE_WINDOW", self.__onclosing)

        # pull prior config data and update options accordingly
        self.getConfig()

        # L O O P
        self.window.mainloop()

    def __onclosing(self):
        # save config data
        self.saveConfig()
        # yeet the window
        self.window.destroy()

    def __startStage(self):
        try:
            # ensure that user has *actually* selected a com port
            if self.comval.get() == 'Select Com Port':
                raise Exception
            # start the stage
            self.stage = LIBS_2AxisStage(self.comval.get(), self.baudval.get(), self.startfile.get()).start()

        except Exception as e:
            self.stagelabel.config(text='Could not start stage', fg='Red')
            print(e)
            self.window.after(5000, lambda: self.stagelabel.config(text='Stage Control Launcher', fg='Black'))

    def getConfig(self):
        if os.path.exists(self.cfg_file):
            with open(self.cfg_file, 'r') as f:
                for i in f:
                    i = i.rstrip().split(':')
                    if i[0] == 'com':
                        if i[1] in self.comlist:
                            self.comval.set(i[1])
                    elif i[0] == 'baud':
                        self.baudval.set(int(i[1]))
                    elif i[0] == 'startfile':
                        self.startfile.delete(0, tk.END)
                        self.startfile.insert(0, i[1])

    def saveConfig(self):
        with open(self.cfg_file, 'w+') as f:
            if self.comval.get()[:3] == 'COM':
                f.write('com:' + str(self.comval.get()) + '\n')
            f.write('baud:' + str(self.baudval.get()) + '\n')
            f.write('startfile:' + str(self.startfile.get()))

if __name__ == '__main__':
    StageLauncher()
