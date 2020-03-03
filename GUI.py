import tkinter as TKR
from tkinter import filedialog
import subprocess

class Example(TKR.Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("File dialog")
        self.pack(fill=TKR.BOTH,expand=1)
        
        self.btn1 = TKR.Button(self, text="Video",
                                command=self.onChoose)
        self.btn1.place(x=35,y=50)
        
        self.btn2 = TKR.Button(self, text="Cam",
                                command=self.onCam)
        self.btn2.place(x=37,y=100)
        
        self.btn3 = TKR.Button(self, text="Exit",
                                command=self.onExit)
        self.btn3.place(x=37,y=150)
        
        # self.txt = TKR.Text(self)
        # self.txt.pack(fill=TKR.BOTH,expand=1)
        
    def onChoose(self):
        
        ftypes = [('MP4/mp4','*.mp4'),
                    ('AVI/avi','*avi'),
                    ('All Types','*')]
        dlg = TKR.filedialog.askopenfilename(title="Select File",filetypes=ftypes)
        
        self.readFile(dlg)
    
    def readFile(self, filename):
        # print(filename)
        P = subprocess.Popen(['python','Program.py','-v',filename])
        # pass
    
    def onCam(self):
        P = subprocess.Popen(['python','Program.py'])
        pass
    
    def onExit(self):
        exit()


def main():
    root = TKR.Tk()
    ex = Example()
    root.geometry("100x200+100+100")
    root.mainloop()
    
if __name__ == '__main__':
    main()
