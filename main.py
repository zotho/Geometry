#!/usr/bin/env python2.7
# -*- coding: utf-8

import tkinter


class Point3():
    # for future (can add new coordinate)
    dict_coord = {'x': 0, 'y': 1, 'z': 2}

    def __init__(self, coords3):
        self.coords3 = coords3[:len(self.dict_coord)]

    # x = p['x']
    def __getitem__(self, index):
        return self.coords3[self.dict_coord[index]]

    # p['x'] = x
    def __setitem__(self, index, value):
        self.coords3[self.dict_coord[index]] = value


class Line3():
    # for future (can add new coordinate)
    dict_coord = {'x': 0, 'y': 1, 'z': 2}

    def __init__(self, *args, **kwargs):
        if kwargs.get('arr_points3', None) is None:
            self.points3 = kwargs.get('arr_points3')[:2]
        elif(kwargs.get('xy0', None) is None and
             kwargs.get('xy1', None) is None):
            self.points3 = [Point3(xy) for xy in
                            [kwargs.get('xy0'), kwargs.get('xy1')]]
        else:
            print("Error! Bad argument:{} {}".format(args, kwargs))

    # x0 = l['x0']
    def __getitem__(self, index):
        return self.points3[int(index[1])][self.dict_coord[index[0]]]

    # l['x0'] = x0
    def __setitem__(self, index, value):
        self.points3[int(index[1])][self.dict_coord[index[0]]] = value


class Poly3():
    # for future (can add new coordinate)
    dict_coord = {'x': 0, 'y': 1, 'z': 2}

    def __init__(self, *args, **kwargs):
        if kwargs.get('arr_points3', None) is None:
            arr_points3 = kwargs.get('arr_points3', None)
            self.lines3 = [Line3(arr_points3[i - 1], arr_points3[i]) for i
                           in range(1, len(arr_points3))]
        elif kwargs.get('arr_xy', None) is None:
            arr_xy = kwargs.get('arr_xy', None)
            self.lines3 = [Line3(arr_xy[i - 1], arr_xy[i]) for i
                           in range(1, len(arr_xy))]
        else:
            print("Error! Bad argument:{} {}".format(args, kwargs))


"""
class Geom3():
    figures3 = []
    points3 = []

    def __init__(self):
        pass

    def create_line3(self, points):
"""


class Geom_Canvas():
    figures = []

    def __init__(self, canvas):
        canv = self.canv = canvas
        self.width = canv['width']
        self.height = canv['height']

        self.methods = {'line': canv.create_line,
                        'polygon': canv.create_polygon,
                        'rectangle': canv.create_rectangle,
                        'oval': canv.create_oval}

        # self.create([100, 200, 300, 400], method=self.canv.create_line)
        self.draw()

    def create(self, coords, options={}, method=None):
        if method is None:
            method = self.methods['line']
        fig = self.canv.create_line(coords, options)
        self.figures.append(fig)
        return fig

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

        geom_canv = self.geometry_canvas = Geom_Canvas(canv)

        a = geom_canv.create([100, 150, 400, 600], {'tag': 'line', 'fill': '#ffffff', 'activefill': '#00ff00',
                             'width': 20})
        geom_canv.canv.itemconfig(a, {'fill': '#ff0000'})

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
