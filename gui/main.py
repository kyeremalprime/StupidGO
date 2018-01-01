from tkinter import *
from PIL import Image, ImageTk
import types

global current_size
current_size = {'width': 0.0, 'height': 0.0}

class main(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.original = Image.open('src/wood.png')
        self.image = ImageTk.PhotoImage(self.original)
        self.original_black = Image.open('src/black.png')
        self.black = ImageTk.PhotoImage(self.original_black)
        self.original_white = Image.open('src/white.png')
        self.white = ImageTk.PhotoImage(self.original_white)
        self.display = Canvas(self, bd=0, highlightthickness=0)
        self.display.grid(row=0, sticky=W+E+N+S)

        self.pack(fill=BOTH, expand=1)
        self.display.bind("<Button-1>", self.play)
        self.bind("<Configure>", self.resize)

    def play(self, event):
        global current_size

        LENGTH = 1254.0
        BORDER = 69.0
        GAP = 62.0
        blank = (max(current_size['width'], current_size['height']) - min(current_size['width'], current_size['height'])) / 2.0
        relborder = (BORDER / (LENGTH*1.0)) * min(current_size['width'], current_size['height'])
        relgap = (GAP / (LENGTH*1.0)) * min(current_size['width'], current_size['height'])
        tx = float(event.x) - relborder
        ty = float(event.y) - relborder
        if (current_size['width'] >= current_size['height']):
            tx -= blank
        else:
            ty -= blank
        tx = round(float(tx) / (relgap*1.0))
        ty = round(float(ty) / (relgap*1.0))
        size = (int(relgap), int(relgap))
        resized = self.original.resize(size, Image.ANTIALIAS)
        self.black = ImageTk.PhotoImage(resized)

        if (current_size['width'] >= current_size['height']):
            self.display.create_image(blank+relborder+tx*relgap - (relgap/2.0), relborder+ty*relgap - (relgap/2.0), image=self.black, anchor=NW, tags="PIECE")
        else:
            self.display.create_image(relborder+tx*relgap - (relgap/2.0), blank+relborder+ty*relgap - (relgap/2.0), image=self.black, anchor=NW, tags="PIECE")

    def resize(self, event):
        global current_size

        LENGTH = 1254.0
        BORDER = 69.0
        GAP = 62.0
        current_size['width'] = event.width
        current_size['height'] = event.height
        size = (min(event.width, event.height), min(event.width, event.height))
        relborder = (BORDER / (LENGTH*1.0)) * min(event.width, event.height)
        relgap = (GAP / (LENGTH*1.0)) * min(event.width, event.height)
        blank = (max(event.width, event.height) - min(event.width, event.height)) / 2.0
        resized = self.original.resize(size, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        self.display.delete("LINE")
        self.display.delete("IMG")
        if (event.width >= event.height):
            self.display.create_image((event.width-event.height) / 2.0, 0, image=self.image, anchor=NW, tags="IMG")
            for i in range(1, 18):
                self.display.create_line(blank+relborder+i*relgap, relborder, blank+relborder+i*relgap, relborder+18*relgap, fill="#564F3D", tags="LINE")
                self.display.create_line(blank+relborder, relborder+i*relgap, blank+relborder+18*relgap, relborder+i*relgap, fill="#564F3D", tags="LINE")
            self.display.create_line(blank+relborder, relborder, blank+relborder, relborder+18*relgap, fill="#000000", tags="LINE")
            self.display.create_line(blank+relborder+18*relgap, relborder, blank+relborder+18*relgap, relborder+18*relgap, fill="#000000", tags="LINE")
            self.display.create_line(blank+relborder, relborder, blank+relborder+18*relgap, relborder, fill="#000000", tags="LINE")
            self.display.create_line(blank+relborder, relborder+18*relgap, blank+relborder+18*relgap, relborder+18*relgap, fill="#000000", tags="LINE")
            for i in range(0, 3):
                for j in range(0, 3):
                    tx = relborder+3*relgap + 6*i*relgap
                    ty = relborder+3*relgap + 6*j*relgap
                    for k in range(-1, 2):
                        self.display.create_line(blank+tx+k, ty-1, blank+tx+k, ty+1, fill="#000000", tags="LINE")
                        self.display.create_line(blank+tx-1, ty+k, blank+tx+1, ty+k, fill="#000000", tags="LINE")
        else:
            self.display.create_image(0, (event.height-event.width) / 2.0, image=self.image, anchor=NW, tags="IMG")
            for i in range(1, 18):
                self.display.create_line(relborder+i*relgap, blank+relborder, relborder+i*relgap, blank+relborder+18*relgap, fill="#564F3D", tags="LINE")
                self.display.create_line(relborder, blank+relborder+i*relgap, relborder+18*relgap, blank+relborder+i*relgap, fill="#564F3D", tags="LINE")
            self.display.create_line(relborder, blank+relborder, relborder, blank+relborder+18*relgap, fill="#000000", tags="LINE")
            self.display.create_line(relborder+18*relgap, blank+relborder, relborder+18*relgap, blank+relborder+18*relgap, fill="#000000", tags="LINE")
            self.display.create_line(relborder, blank+relborder, relborder+18*relgap, blank+relborder, fill="#000000", tags="LINE")
            self.display.create_line(relborder, blank+relborder+18*relgap, relborder+18*relgap, blank+relborder+18*relgap, fill="#000000", tags="LINE")
            for i in range(0, 3):
                for j in range(0, 3):
                    tx = relborder+3*relgap + 6*i*relgap
                    ty = relborder+3*relgap + 6*j*relgap
                    for k in range(-1, 2):
                        self.display.create_line(tx+k, blank+ty-1, tx+k, blank+ty+1, fill="#000000", tags="LINE")
                        self.display.create_line(tx-1, blank+ty+k, tx+1, blank+ty+k, fill="#000000", tags="LINE")


root = Tk()
root.title("StupidGO")
root.geometry('%dx%d+150+50' % (627, 627))

app = main(root)
app.mainloop()

root.destroy()
 
