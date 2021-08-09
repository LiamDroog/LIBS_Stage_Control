import tkinter as tk
from tkinter import font, ttk
import os
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import numpy as np
import gc
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class imageViewer:
    def __init__(self, image_target_dir, spectra_target_dir, file_extension, master=None):
        # self.window = tk.Tk(className='\Image Viewer')

        # instatiate master window
        # below is all gui setup
        self.window = tk.Toplevel(master=master)
        self.canvasframe = tk.Frame(master=self.window)
        self.canvas = tk.Canvas(master=self.canvasframe, width=1000, height=800)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.scrollbar = ttk.Scrollbar(master=self.window, orient='vertical', command=self.canvas.yview)
        self.scrollFrame = ttk.Frame(master=self.canvas)
        self.scrollFrame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0,0), window=self.scrollFrame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.image_target_dir = image_target_dir
        self.spectra_target_dir = spectra_target_dir
        self.file_ext = file_extension
        self.current_display = None
        self.img_dir_list = []
        self.spectra_dir_list = []
        self.iter = 0
        print('sending to poll image_directory')
        self.pollDirectory()
        # run self.onClosing when we close the window to ensure proper cleanup
        self.window.protocol('WM_DELETE_WINDOW', self.onClosing)
        # L O O P
        self.window.mainloop()

    def pollDirectory(self):
        # Make sure cwd is the same as the target wd
        if not os.getcwd() == self.image_target_dir:
            os.chdir(self.image_target_dir)
        try:
            # get a lits of all files in image_directory
            self.img_dir_list = sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime)
            # set current top image to the most recently modified file in the image_directory
            if not self.current_display or self.current_display != self.img_dir_list[-1]:
                self.current_display = self.img_dir_list[-1]

            os.chdir(self.spectra_target_dir)
            self.spectra_dir_list = sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime)

            self.update_image(self.img_dir_list, self.spectra_dir_list)

        except Exception as e:
            print(e)
        finally:
            gc.collect()
            self.window.after(1000, self.pollDirectory)


        # if [i for i in os.listdir(self.image_target_dir) if i[-3:] == self.file_ext]:
        #     present_shots = [int(i[:-4].split('-')[-1]) for i in os.listdir(self.image_target_dir) if i[-3:] == self.file_ext]
        #     present_shots.sort(key=lambda x: os.path.getmtime(x))
        #     print(present_shots)

    def stop(self):
        self.window.destroy()

    def old_update_image(self):
        # deprecated, only displays one image :(
        font = tk.font.Font(family='Helvetica', size=36, weight='bold')
        self.header = tk.Label(master=self.scrollFrame, text=self.current_display.split('\\')[-1], font=font)
        self.header.grid(row=0, column=0, columnspan=2)
        # self.imageFrame = tk.Frame(master=self.window)
        self.image = Image.open(self.current_display)
        factor = 0.5
        self.image = self.image.resize((int(self.image.size[0] * factor), int(self.image.size[1] * factor)),
                                       Image.ANTIALIAS)
        self.tkimage = ImageTk.PhotoImage(self.image)

        # imgvw = ScrollableImage(self.window, image=self.tkimage, scrollbarwidth=12,
        #                    width=400, height=400)
        # imgvw.grid(row=0, column=0)
        self.label = tk.Label(master=self.scrollFrame, image=self.tkimage)
        self.label.image = self.tkimage
        self.label.grid(row=1, column=0, columnspan=2)

        self.canvasframe.grid(row=0, column=0)
        self.canvas.grid(row=0, column=0, sticky='nesw')
        self.scrollbar.grid(row=0, column=1, sticky='nse')


    def _on_mousewheel(self, event):
        # scroll on command
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_image(self, img_dir_list, spectra_dir_list):

        # init font
        font = tk.font.Font(family='Helvetica', size=16, weight='bold')
        # get 5 most recent files and reverse list so that the most recent is index 0
        self.img_dir_list = img_dir_list[-5:]
        self.img_dir_list.reverse()
        self.spectra_dir_list = spectra_dir_list[-5:]
        self.spectra_dir_list.reverse()

        for j, i in enumerate(self.img_dir_list):
            os.chdir(self.image_target_dir)
            # put it into a frame and pack it nicely
            self.rtnFrame = tk.Frame(master=self.scrollFrame, borderwidth=3, relief='groove')
            self.imgframe = tk.Frame(master=self.rtnFrame)
            self.specframe = tk.Frame(master=self.rtnFrame)

            # for image of sample
            self.sample_header = tk.Label(master=self.imgframe, text=i.split('\\')[-1], font=font)
            self.sample_header.grid(row=0, column=0, columnspan=2)
            # self.imageFrame = tk.Frame(master=self.window)
            self.sample_image = Image.open(i)
            factor = 0.35
            self.sample_image = self.sample_image.resize((int(self.sample_image.size[0] * factor), int(self.sample_image.size[1] * factor)),
                                           Image.ANTIALIAS)
            self.sample_tkimage = ImageTk.PhotoImage(self.sample_image)

            self.sample_label = tk.Label(master=self.imgframe, image=self.sample_tkimage)
            self.sample_label.image = self.sample_tkimage
            self.sample_label.grid(row=1, column=0, columnspan=2)

            # for spectra of sample. NEEDS REWORK FOR SPECRA EH

            os.chdir(self.spectra_target_dir)

            self.spec_header = tk.Label(master=self.specframe, text=self.spectra_dir_list[j].split('\\')[-1], font=font)
            self.spec_header.grid(row=0, column=0, columnspan=2)
            self.dat = np.loadtxt(spectra_dir_list[j], dtype=float, delimiter=';')
            # we need to have the plot shit in here!
            self.figure = plt.Figure(figsize=(5,4), dpi=100)
            self.ax = self.figure.add_subplot(111)
            self.ax.plot(self.dat[:,0], self.dat[:,1])
            self.lineplot = FigureCanvasTkAgg(self.figure, self.specframe)
            self.lineplot.get_tk_widget().grid(row=1, column=0, columnspan=2)



            # self.spec_image = Image.open('C:\\Users\\Liam Droog\\Desktop\\spectra.png')
            # factor = 0.25
            # self.spec_image = self.spec_image.resize((int(self.spec_image.size[0] * factor), int(self.spec_image.size[1] * factor)),
            #                                Image.ANTIALIAS)
            # self.spec_tkimage = ImageTk.PhotoImage(self.spec_image)
            #
            # self.spec_label = tk.Label(master=specframe, image=self.spec_tkimage)
            # self.spec_label.image = self.spec_tkimage
            # self.spec_label.grid(row=1, column=0, columnspan=2)

            self.imgframe.grid(row=0, column=1)
            self.specframe.grid(row=0, column=0)
            self.rtnFrame.grid(row=j, column=0)

        self.canvasframe.grid(row=0, column=0)
        self.canvas.grid(row=0, column=0, sticky='nesw')
        self.scrollbar.grid(row=0, column=1, sticky='nse')

    def mouse_scroll(self, evt):
        if evt.state == 0 :
            # self.cnvs.yview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.cnvs.yview_scroll(int(-1*(evt.delta/120)), 'units') # For windows
        if evt.state == 1:
            # self.cnvs.xview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.cnvs.xview_scroll(int(-1*(evt.delta/120)), 'units') # For windows

    def onClosing(self):
        self.window.destroy()
if __name__ == '__main__':
    # imageViewer('C:\\Users\\Liam Droog\\Desktop\\controlTest\\Images', 'bmp')
    pass
