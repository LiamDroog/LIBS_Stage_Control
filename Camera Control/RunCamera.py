import os.path
import os
import sys
import keyboard
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import tkinter as tk
from tkinter import filedialog
import multiprocessing as mp
from CamCapture import main as camMain
from Disp_Images import imageViewer
from PIL import Image, ImageTk

class runcam:
    def __init__(self):
        self.window = tk.Tk(className='\Camera Setup')
        self.directory = os.getcwd()

        self.file_extension = 'png' # add a dropdown to select!

        self.dirEntry = tk.Entry(master=self.window, width=50)
        self.dirEntry.insert(0, 'C:\\Users\\Liam Droog\\Desktop\\controlTest\\Images')
        self.dirEntry.grid(row=0, column=3, columnspan=2, sticky='ew')

        self.dirLbl = tk.Label(master=self.window, text='Full path of directory:')
        self.dirLbl.grid(row=0, column=0, columnspan=2, sticky='ew')

        self.setDirBtn = tk.Button(master=self.window, text='Set', command=self.setTargetDirectory)
        self.setDirBtn.grid(row=0, column=5, sticky='ew')

        self.browseDirBtn = tk.Button(master=self.window, text='Browse', command=self.browse_for_dir)
        self.browseDirBtn.grid(row=0, column=6, sticky='ew')

        self.checkFiles = tk.Checkbutton(master=self.window, text='Parse for existing files')
        self.checkFiles.grid(row=1, column=0, columnspan=2, sticky='w')

        self.startnumcheck = tk.Checkbutton(master=self.window, text='Restart numbering')
        self.startnumcheck.grid(row=2, column=0, columnspan=2, sticky='w')

        self.startFileAt = tk.Entry(master=self.window)
        self.startFileAt.grid(row=3, column=1, sticky='w')

        self.startFileAtLbl = tk.Label(master=self.window, text='Start at:')
        self.startFileAtLbl.grid(row=3, column=0, sticky='w')

        self.startCaptureButton = tk.Button(master=self.window, text='Start Camera', command=self.runCamera)
        self.startCaptureButton.grid(row=4, column=0, columnspan=2, sticky='nsew')

        self.stahpCaptureButton = tk.Button(master=self.window, text='Stop Camera', command=self.stopCamera)
        self.stahpCaptureButton.grid(row=5, column=0, columnspan=2, sticky='nsew')

        self.launchImageViewbtn = tk.Button(master=self.window, text='Launch Viewer',
                                            command=lambda: imageViewer(self.directory, self.file_extension, self.window))

        # IMAGE MEME
        self.image = Image.open('C:\\Users\\Liam Droog\\Desktop\\catcamera.png')
        factor = 0.2
        self.image = self.image.resize((int(self.image.size[0] * factor), int(self.image.size[1] * factor)),
                                       Image.ANTIALIAS)
        self.tkimage = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(master=self.window, image=self.tkimage)
        self.label.image = self.tkimage
        self.label.grid(row=1, column=3, columnspan=5, rowspan=10)


        self.launchImageViewbtn.grid(row=6, column=0, columnspan=2, sticky='nsew')
        self.window.protocol('WM_DELETE_WINDOW', self._onClosing)
        self.startCaptureButton.config(state=tk.DISABLED)
        self.stahpCaptureButton.config(state=tk.DISABLED)
        self.launchImageViewbtn.config(state=tk.DISABLED)
        self.window.mainloop()

    def setTargetDirectory(self):
        ipt = self.dirEntry.get()
        if os.path.exists(ipt):
            print('Valid input. Setting target directory...')
            self.setDirBtn.config(bg='green')
            self.directory = ipt
            self.startCaptureButton.config(state=tk.ACTIVE)
            self.stahpCaptureButton.config(state=tk.ACTIVE)
            self.launchImageViewbtn.config(state=tk.ACTIVE)

        else:
            print('Invalid input, Try again :(')

    def showImageViewer(self):
        self.imageview = imageViewer(self.directory, self.file_extension, self.window)

    def setFilePrefix(self):
        pass

    def browse_for_dir(self):
        self.dirEntry.delete(0, tk.END)
        self.dirEntry.insert(0, filedialog.askdirectory())

    def runCamera(self):
        self.process = mp.Process(target=camMain, args=(self.directory, self.file_extension))   # args for directory, start number from above inputs.
        self.process.start()

    def stopCamera(self):
        try:
            keyboard.press('esc')
            self.process.join()
            keyboard.release('esc')
            self.imageview.stop()

        except:
            print('Failed to stop camera. Run!')

    def parseDirectory(self):
        pass

    def _onClosing(self):
        try:
            # I don't like this implementation, but it works. I foresee issues in the future. Avoid this in the future.
            keyboard.press('esc')
            self.process.join()
            keyboard.release('esc')
        except:
            pass
        finally:
            self.window.destroy()


if __name__ == '__main__':
    # imageViewer('C:\\Users\\Liam Droog\\Desktop\\controlTest\\Images', 'bmp')
    runcam()
