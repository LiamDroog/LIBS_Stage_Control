import tkinter as tk
from tkinter import font, ttk
import os
from PIL import ImageTk, Image
class imageViewer:
    def __init__(self, target_dir, file_extension, master=None):
        # self.window = tk.Tk(className='\Image Viewer')
        self.window = tk.Toplevel(master=master)

        self.canvasframe = tk.Frame(master=self.window)
        self.canvas = tk.Canvas(master=self.canvasframe, width=660, height=800)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.scrollbar = ttk.Scrollbar(master=self.window, orient='vertical', command=self.canvas.yview)
        self.scrollFrame =ttk.Frame(master=self.canvas)
        self.scrollFrame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0,0), window=self.scrollFrame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)


        # self.imgframe = tk.Frame(master=self.window)
        # self.imgframe.grid(row=0, column=0)
        # self.canvas = tk.Canvas(self.imgframe, bg='#FFFFFF', width=300, height=300, scrollregion=(0, 0, 1000, 1000))
        # self.vbar = tk.Scrollbar(self.imgframe, orient=tk.VERTICAL)
        # self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        # self.vbar.config(command=self.canvas.yview)
        # self.canvas.config(width=1000, height=1000)
        # self.canvas.config(yscrollcommand=self.vbar.set)
        # self.canvas.pack(side=tk.LEFT, expand=True) #, fill=tk.BOTH)
        self.targetDir = target_dir
        self.file_ext = file_extension
        self.current_display = None
        self.dir_list = []
        self.iter = 0
        print('sending to poll directory')
        self.pollDirectory()

        self.window.mainloop()

    def pollDirectory(self):

        if not os.getcwd() == self.targetDir:
            os.chdir(self.targetDir)
        try:
            self.dir_list = sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime)

            if not self.current_display or self.current_display != self.dir_list[-1]:
                self.current_display = self.dir_list[-1]
            self.update_image(self.dir_list)

            # display image yeet

            print(self.current_display)
            # self.iter += 1
            # if self.iter % 5 == 0:
            #     self.iter = 0
            #     self.update_image()
            #     print('Updating images based on iterations')
        except Exception as e:
            print(e)
        finally:
            self.window.after(1000, self.pollDirectory)


        # if [i for i in os.listdir(self.targetDir) if i[-3:] == self.file_ext]:
        #     present_shots = [int(i[:-4].split('-')[-1]) for i in os.listdir(self.targetDir) if i[-3:] == self.file_ext]
        #     present_shots.sort(key=lambda x: os.path.getmtime(x))
        #     print(present_shots)

    def stop(self):
        self.window.destroy()

    def old_update_image(self):

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
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_image(self, dir_list):

        font = tk.font.Font(family='Helvetica', size=16, weight='bold')
        dir_list = dir_list[-5:]
        dir_list.reverse()
        for j, i in enumerate(dir_list):
            self.rtnFrame = tk.Frame(master=self.scrollFrame, borderwidth=3, relief='groove')
            imgframe = tk.Frame(master=self.rtnFrame)
            specframe = tk.Frame(master=self.rtnFrame)

            # for image of sample
            self.sample_header = tk.Label(master=imgframe, text=i.split('\\')[-1], font=font)
            self.sample_header.grid(row=0, column=0, columnspan=2)
            # self.imageFrame = tk.Frame(master=self.window)
            self.sample_image = Image.open(i)
            factor = 0.25
            self.sample_image = self.sample_image.resize((int(self.sample_image.size[0] * factor), int(self.sample_image.size[1] * factor)),
                                           Image.ANTIALIAS)
            self.sample_tkimage = ImageTk.PhotoImage(self.sample_image)

            self.sample_label = tk.Label(master=imgframe, image=self.sample_tkimage)
            self.sample_label.image = self.sample_tkimage
            self.sample_label.grid(row=1, column=0, columnspan=2)


            # for spectra of sample. NEEDS REWORK FOR SPECRA EH
            self.spec_header = tk.Label(master=specframe, text=i.split('\\')[-1], font=font)
            self.spec_header.grid(row=0, column=0, columnspan=2)
            # self.imageFrame = tk.Frame(master=self.window)
            self.spec_image = Image.open(i)
            factor = 0.25
            self.spec_image = self.spec_image.resize((int(self.spec_image.size[0] * factor), int(self.spec_image.size[1] * factor)),
                                           Image.ANTIALIAS)
            self.spec_tkimage = ImageTk.PhotoImage(self.spec_image)

            self.spec_label = tk.Label(master=specframe, image=self.sample_tkimage)
            self.spec_label.image = self.spec_tkimage
            self.spec_label.grid(row=1, column=0, columnspan=2)

            imgframe.grid(row=0, column=1)
            specframe.grid(row=0, column=0)
            self.rtnFrame.grid(row=j, column=0)

        self.canvasframe.grid(row=0, column=0)
        self.canvas.grid(row=0, column=0, sticky='nesw')
        self.scrollbar.grid(row=0, column=1, sticky='nse')


            # self.frame = tk.Frame(master=self.window)

            # self.frame.grid(row=2, column=0, columnspan=5, rowspan=5)

class ScrollableImage(tk.Frame):
    def __init__(self, master=None, **kw):
        self.image = kw.pop('image', None)
        sw = kw.pop('scrollbarwidth', 10)
        super(ScrollableImage, self).__init__(master=master, **kw)
        self.cnvs = tk.Canvas(self, highlightthickness=0, **kw)
        self.cnvs.create_image(0, 0, anchor='nw', image=self.image)
        # Vertical and Horizontal scrollbars
        self.v_scroll = tk.Scrollbar(self, orient='vertical', width=sw)
        self.h_scroll = tk.Scrollbar(self, orient='horizontal', width=sw)
        # Grid and configure weight.
        self.cnvs.grid(row=0, column=0,  sticky='nsew')
        self.h_scroll.grid(row=1, column=0, sticky='ew')
        self.v_scroll.grid(row=0, column=1, sticky='ns')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Set the scrollbars to the canvas
        self.cnvs.config(xscrollcommand=self.h_scroll.set,
                           yscrollcommand=self.v_scroll.set)
        # Set canvas view to the scrollbars
        self.v_scroll.config(command=self.cnvs.yview)
        self.h_scroll.config(command=self.cnvs.xview)
        # Assign the region to be scrolled
        self.cnvs.config(scrollregion=self.cnvs.bbox('all'))
        self.cnvs.bind_class(self.cnvs, "<MouseWheel>", self.mouse_scroll)

    def mouse_scroll(self, evt):
        if evt.state == 0 :
            # self.cnvs.yview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.cnvs.yview_scroll(int(-1*(evt.delta/120)), 'units') # For windows
        if evt.state == 1:
            # self.cnvs.xview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.cnvs.xview_scroll(int(-1*(evt.delta/120)), 'units') # For windows


if __name__ == '__main__':
    imageViewer('C:\\Users\\Liam Droog\\Desktop\\controlTest\\Images', 'bmp')


