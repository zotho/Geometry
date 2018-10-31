#!/usr/bin/env python2.7
# -*- coding: utf-8

import Tkinter as tkinter
from Geom3 import *


class Geom_Canvas():
    figures = []

    def __init__(self, canvas):
        self.figures = []
        canv = self.canv = canvas
        self.width = int(canv['width'])
        self.height = int(canv['height'])

        self.methods = {'line': canv.create_line,
                        'polygon': canv.create_polygon,
                        'rectangle': canv.create_rectangle,
                        'oval': canv.create_oval}

        self.geom = Geom3()
        self.X = Point3([1,0,0])
        self.Y = Point3([0,1,0])
        self.Z = Point3([0,0,1])
        self.tZ = Point3([0,0,1])
        self.g = Geom3()
        self.g.add(self.tZ)
        self.pX = self.width
        self.pY = self.height
        self.proj1 = Proj2(self.X, self.Z, self.geom)
        # self.create([100, 200, 300, 400], method=self.canv.create_line)
        self.draw()

    # coords: [[x,y,z],[x,y,z]]
    def create(self, coords, options={}, method=None):
        if method is None:
            method = self.methods['line']
        self.geom.add(Line3(coords[0],coords[1]))
        self.proj1.update()
        coords = self.proj1.geom2.figures3[-1].points3[0].coords3 + self.proj1.geom2.figures3[-1].points3[1].coords3
        coords = [i[0]+i[1] for i in zip(coords, [self.pX,self.pY]*2)]
        fig = method(coords, options)
        #print(self.proj1.geom2.figures3[-1].points3[0].coords3 +
        #                self.proj1.geom2.figures3[-1].points3[1].coords3)
        self.figures.append(fig)
        self.draw()
        return fig

    def rotate(self, key):
        # print "rotated"
        import math
        if key=='w':
            self.g.rotate(1,2,math.pi/12)
        elif key == 'e':
            self.g.rotate(0,2,math.pi/12)
        elif key == 'r':
            self.g.rotate (0, 1, math.pi / 12)
        self.proj1.update(vec_rot_point3=self.tZ)
        for fig in zip(self.figures,self.proj1.geom2.figures3):
            coords = fig[1].points3[0].coords3 + fig[1].points3[1].coords3
            coords = [int(i[0] + i[1]) for i in zip (coords, [self.pX, self.pY] * 2)]
            # print coords
            self.canv.coords(fig[0], coords[0],coords[1],coords[2],coords[3])
        self.draw()

    def draw(self):
        self.canv.update_idletasks()
        self.canv.update()


class App():
    def __init__(self):
        root = self.root = tkinter.Tk()
        root.title('Geometry')
        # make the top right close button minimize (iconify) the main window
        # root.protocol("WM_DELETE_WINDOW", root.iconify)
        # make Esc and q exit the program
        root.bind('<Escape>', self.close_window)
        root.bind('<q>', self.close_window)
        # close window by exit button
        root.protocol("WM_DELETE_WINDOW",
                      lambda: self.close_window(event=None))
        root.bind("<Destroy>", self.destroy_window)

        w = 800  # width for the Tk root
        h = 600  # height for the Tk root
        # get screen width and height
        ws = root.winfo_screenwidth()  # width of the screen
        hs = root.winfo_screenheight()  # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        root.geometry('{}x{}+{}+{}'.format(w, h, x, y))
        root.minsize(w / 2 + 70, h / 2)
        # root.resizable (False, False)

        # Frames
        f_canvas = self.f_canvas = tkinter.Frame(root)
        f_buttons = self.f_buttons = tkinter.Frame(root)

        f_canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        f_buttons.pack(side=tkinter.LEFT, anchor=tkinter.NE)

        # Wigets
        lab1 = self.lab1 = tkinter.Label(
            f_buttons, {'width': 5, 'height': 1, 'bg': 'yellow', 'text': '1'})
        lab1.pack(anchor=tkinter.NE, side=tkinter.TOP)
        lab2 = self.lab2 = tkinter.Label(
            f_buttons, {'width': 5, 'height': 1, 'bg': 'red', 'text': '2'})
        lab2.pack(anchor=tkinter.NE, side=tkinter.TOP)

        canv = self.canvas = tkinter.Canvas(
            f_canvas, {'bg': 'white'})

        # Canvas
        self.geom_canv = self.geometry_canvas = Geom_Canvas(canv)

        a = self.geom_canv.create([[100, -150, 0], [40, -60, 0]],
                             {'tag': 'line', 'fill': '#ff0000',
                              'activefill': '#00ff00', 'width': 5})
        b = self.geom_canv.create([[40, -60, 0], [200, 100, 100]],
                             {'tag': 'line', 'fill': '#ff0000',
                              'activefill': '#00ff00', 'width': 5})
        c = self.geom_canv.create ([[200, 100, 100], [100, -150, 0]],
                              {'tag': 'line', 'fill': '#ff0000',
                               'activefill': '#00ff00', 'width': 5})
        #geom_canv.canv.itemconfig(a, {'fill': '#ff0000'})
        root.bind ('w',  lambda event: self.geom_canv.rotate('w'))
        root.bind ('e', lambda event: self.geom_canv.rotate ('e'))
        root.bind ('r', lambda event: self.geom_canv.rotate ('r'))


        canv.pack(expand=1, fill=tkinter.BOTH)

        root.update_idletasks()

        root.mainloop()

    def close_window(self, event):
        try:
            # ask
            self.root.destroy()
        except tkinter.TclError:
            pass

    def destroy_window(self, event):
        # any
        self.root.destroy()


if __name__ == "__main__":
    app = App()
