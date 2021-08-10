"""
##################################################
Orchestrates the running of the FLIR camera for
LIBS experiments. Depends on camcapture.py and
Disp_images.py for capture and display of images
respectively.
##################################################
# Author:   Liam Droog
# Email:    droog@ualberta.ca
# Year:     2021
# Version:  V.1.0.0
##################################################
"""
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
        self.image_directory = os.getcwd()

        self.file_extension = 'png' # add a dropdown to select!

        self.imgdirEntry = tk.Entry(master=self.window, width=50)
        self.imgdirEntry.insert(0, 'C:\\Users\\Liam Droog\\Desktop\\controlTest\\Images')
        self.imgdirEntry.grid(row=0, column=3, columnspan=2, sticky='ew')

        self.dirLbl = tk.Label(master=self.window, text='Full path of image image_directory:')
        self.dirLbl.grid(row=0, column=0, columnspan=2, sticky='ew')

        self.setDirBtn = tk.Button(master=self.window, text='Set', command=self.setTargetDirectory)
        self.setDirBtn.grid(row=0, column=5, rowspan=2, sticky='nsew')

        self.browseDirBtn = tk.Button(master=self.window, text='Browse', command=lambda: self.browse_for_dir(self.imgdirEntry))
        self.browseDirBtn.grid(row=0, column=6, sticky='ew')

        self.spectradirEntry = tk.Entry(master=self.window, width=50)
        self.spectradirEntry.insert(0, 'C:\\Users\\Liam Droog\\Desktop\\controlTest\\Spectra')
        self.spectradirEntry.grid(row=1, column=3, columnspan=2, sticky='ew')

        self.dirLbl = tk.Label(master=self.window, text='Full path of spectra image_directory:')
        self.dirLbl.grid(row=1, column=0, columnspan=2, sticky='ew')

        self.browseDirBtn = tk.Button(master=self.window, text='Browse', command=lambda: self.browse_for_dir(self.spectradirEntry))
        self.browseDirBtn.grid(row=1, column=6, sticky='ew')

        self.checkFiles = tk.Checkbutton(master=self.window, text='Parse for existing files')
        self.checkFiles.grid(row=2, column=0, columnspan=2, sticky='w')

        self.startnumcheck = tk.Checkbutton(master=self.window, text='Restart numbering')
        self.startnumcheck.grid(row=3, column=0, columnspan=2, sticky='w')

        self.startFileAt = tk.Entry(master=self.window)
        self.startFileAt.grid(row=4, column=1, sticky='w')

        self.startFileAtLbl = tk.Label(master=self.window, text='Start at:')
        self.startFileAtLbl.grid(row=4, column=0, sticky='w')

        self.startCaptureButton = tk.Button(master=self.window, text='Start Camera', command=self.runCamera)
        self.startCaptureButton.grid(row=5, column=0, columnspan=2, sticky='nsew')

        self.stahpCaptureButton = tk.Button(master=self.window, text='Stop Camera', command=self.stopCamera)
        self.stahpCaptureButton.grid(row=6, column=0, columnspan=2, sticky='nsew')

        self.launchImageViewbtn = tk.Button(master=self.window, text='Launch Viewer',
                                            command=lambda: imageViewer(self.image_directory, self.spectra_directory, self.file_extension, self.window))

        # IMAGE MEME
        try:
            self.image = Image.open('C:\\Users\\Liam Droog\\Desktop\\catcamera.jpg')
            factor = 0.4
            self.image = self.image.resize((int(self.image.size[0] * factor), int(self.image.size[1] * factor)),
                                           Image.ANTIALIAS)
            self.tkimage = ImageTk.PhotoImage(self.image)
            self.label = tk.Label(master=self.window, image=self.tkimage)
            self.label.image = self.tkimage
            self.label.grid(row=4, column=3, columnspan=5, rowspan=10)
        except:
            pass

        self.launchImageViewbtn.grid(row=7, column=0, columnspan=2, sticky='nsew')
        self.window.protocol('WM_DELETE_WINDOW', self._onClosing)
        self.startCaptureButton.config(state=tk.DISABLED)
        self.stahpCaptureButton.config(state=tk.DISABLED)
        self.launchImageViewbtn.config(state=tk.DISABLED)
        self.window.mainloop()

    def setTargetDirectory(self):
        """
        Sets the target directory for both images and spectras
        :return:
        """
        img_ipt = self.imgdirEntry.get()
        spec_ipt = self.spectradirEntry.get()
        if os.path.exists(img_ipt) and os.path.exists(spec_ipt) and img_ipt != spec_ipt:
            print('Valid input. Setting target image_directory...')
            self.setDirBtn.config(bg='green')
            self.image_directory = img_ipt
            self.spectra_directory = spec_ipt
            self.startCaptureButton.config(state=tk.ACTIVE)
            self.stahpCaptureButton.config(state=tk.ACTIVE)
            self.launchImageViewbtn.config(state=tk.ACTIVE)

        else:
            self.imgdirEntry.config(bg='Red')
            self.window.after(500, lambda: self.imgdirEntry.config(bg='white'))
            print('Invalid input, Try again :(')

    def showImageViewer(self):
        self.imageview = imageViewer(self.image_directory, self.spectra_directory, self.file_extension, self.window)

    def setFilePrefix(self):
        pass

    def browse_for_dir(self, tgt):
        tgt.delete(0, tk.END)
        tgt.insert(0, filedialog.askdirectory())

    def runCamera(self):
        self.process = mp.Process(target=camMain, args=(self.image_directory, self.file_extension))   # args for image_directory, start number from above inputs.
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
