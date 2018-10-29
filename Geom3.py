#!/usr/bin/env python2.7
# -*- coding: utf-8

# python3
from functools import reduce
import types

'''
Shape3
    Point3  self.coords3
    Line3   self.points3
    Poly3   self.lines3

TODO
Shape3
    Point3  self.coords3
    Poly3   self.points3
        Line3   self.points3
'''


class Shape3():
    # for future (can add new coordinate)
    dict_coord = {'x': 0, 'y': 1, 'z': 2}

    error_args_message = "Error! Bad argument:args={args}\
                          kwargs={kwargs} for {nam}"


class Point3(Shape3):
    name = 'point'

    def __init__(self, coords3):
        if len(coords3) >= len(self.dict_coord):
            self.coords3 = coords3[:len(self.dict_coord)]
        else:
            self.error_args_message.format(
                args=coords3, kwargs='', nam=self.name)

    def __str__(self):
        return "{}({})".format(
            self.name, str(reduce(lambda x, y: '{},{}'.format(x, y),
                                  self.coords3)))

    # x = p['x']
    def __getitem__(self, index):
        return self.coords3[self.dict_coord[index]]

    # p['x'] = x
    def __setitem__(self, index, value):
        self.coords3[self.dict_coord[index]] = value


class Line3(Shape3):
    name = 'line'

    def __init__(self, *args, **kwargs):
        # print("Line argument:{} {}".format(args, kwargs))

        # Line3(arr_points3=[p1,p2])
        if not kwargs.get('arr_points3', None) is None:
            self.points3 = kwargs.get('arr_points3')

        # Line3(xy0=[x0,y0],xy1=[x1,y1])
        elif not(kwargs.get('xy0', None) is None and
                 kwargs.get('xy1', None) is None):
            self.points3 = [Point3(xy) for xy in
                            [kwargs.get('xy0'), kwargs.get('xy1')]]

        # Line3(p1,p2)
        # Line3([x0,y0],[x1,y1])
        elif len(args) == 2:
            if isinstance(args[0], Point3) and isinstance(args[1], Point3):
                self.points3 = args
            elif isinstance(
                    args[0], types.ListType) and isinstance(
                    args[1], types.ListType):
                self.points3 = [Point3(args[i]) for i in [0, 1]]
            else:
                print(self.error_args_message.format(
                    args=args, kwargs=kwargs, nam=self.name))
        else:
            print(self.error_args_message.format(
                args=args, kwargs=kwargs, nam=self.name))

    def __iter__(self):
        return iter(self.points3)

    def __str__(self):
        return "{}({},\n{tab}{})".format(
            self.name, self.points3[0], self.points3[1],
            tab=' ' * (len(self.name) + 1))

    # x0 = l['x0']
    def __getitem__(self, index):
        return self.points3[int(index[1])][index[0]]

    # l['x0'] = x0
    def __setitem__(self, index, value):
        self.points3[int(index[1])][index[0]] = value


class Poly3(Shape3):
    name = 'poly'

    def __init__(self, *args, **kwargs):
        # print("Line argument:{} {}".format(args, kwargs))

        # Poly3(arr_points3=[p1,p2,p3, ])
        if not (kwargs.get('arr_points3', None) is None):
            arr_points3 = kwargs.get('arr_points3', None)
            self.lines3 = [Line3(arr_points3=[arr_points3[i - 1],
                                              arr_points3[i]]) for i
                           in range(1, len(arr_points3))]

        # Poly3(arr_xy=[[x0,y0,z0],[x1,y1,z1],[x2,y2,z2], ])
        elif not (kwargs.get('arr_xy', None) is None):
            arr_xy = kwargs.get('arr_xy', None)
            self.lines3 = [Line3(xy0=arr_xy[i - 1], xy1=arr_xy[i]) for i
                           in range(1, len(arr_xy))]

        # Poly3(p1,p2,p3, )
        elif len(args) >= 2:
            # check for same types
            if (filter(lambda x: not isinstance(
                    x, Point3), args)) == ():
                self.lines3 = [Line3(arr_points3=[args[i - 1],
                                                  args[i]]) for i
                               in range(1, len(args))]
            else:
                print(self.error_args_message.format(
                    args=args, kwargs=kwargs, nam=self.name))
        else:
            print(self.error_args_message.format(
                args=args, kwargs=kwargs, nam=self.name))

    # ??? iter points or iter lines ???
    def __iter__(self):
        return iter(self.lines3)

    # add tab after each newline
    def __str__(self):
        st = str(reduce(lambda x, y: '{},\n{}'.format(
            str(x), str(y)), self.lines3))
        st = st.replace('\n', '\n' + ' ' * (len(self.name) + 1))
        st = "{}({})".format(self.name, st)
        return st
        return "{}({})".format(
            self.name,
            str(reduce(lambda x, y: '{},\n{}'.format(
                       str(x), str(y)),
                       self.lines3).replace(
                '\n', '\n' + ' ' * (len(self.name) + 1))))

    # TODO: __getitem__ __setitem__


"""
# TODO
class Geom3(Shape3):
    figures3 = []
    points3 = []

    def __init__(self):
        pass

    def create_line3(self, points):
"""

# TODO  Projection with matrix!
#       Rotation with matrix

if __name__ == '__main__':
    p1 = Point3([1, 2, 3])
    p2 = Point3([4, 5, 6])
    p3 = Point3([5, 6, 7])
    """
    l1 = Line3(arr_points3=[p1, p2])
    l2 = Line3(arr_points3=[p2, p3])
    l3 = Line3(xy0=[8, 7, 6], xy1=[5, 4, 3])
    poly1 = Poly3(arr_points3=[p1, p2, p3])
    """
    p1['x'] = 50
    poly2 = Poly3(p1, p2)
    print(poly2)
