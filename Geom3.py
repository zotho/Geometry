#!/usr/bin/env python2.7
# -*- coding: utf-8


class Point3():
    # for future (can add new coordinate)
    dict_coord = {'x': 0, 'y': 1, 'z': 2}

    def __init__(self, coords3):
        self.coords3 = coords3[:len(self.dict_coord)]

    def __str__(self):
        return "point[{}]".format(reduce(lambda x, y: '{},{}'.format(x, y), self.coords3))

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
        # print("Line argument:{} {}".format(args, kwargs))
        if not kwargs.get('arr_points3', None) is None:
            self.points3 = kwargs.get('arr_points3')[:2]
        elif not(kwargs.get('xy0', None) is None and
                 kwargs.get('xy1', None) is None):
            self.points3 = [Point3(xy) for xy in
                            [kwargs.get('xy0'), kwargs.get('xy1')]]
        else:
            print("Error! Bad argument:{} {}".format(args, kwargs))

    def __str__(self):
        return "line: {}, {}".format(self.points3[0],self.points3[1])

    # x0 = l['x0']
    def __getitem__(self, index):
        return self.points3[int(index[1])][index[0]]

    # l['x0'] = x0
    def __setitem__(self, index, value):
        self.points3[int(index[1])][index[0]] = value


class Poly3():
    # for future (can add new coordinate)
    dict_coord = {'x': 0, 'y': 1, 'z': 2}

    def __init__(self, *args, **kwargs):
        # print("Line argument:{} {}".format(args, kwargs))
        if not (kwargs.get('arr_points3', None) is None):
            arr_points3 = kwargs.get('arr_points3', None)
            self.lines3 = [Line3(arr_points3=[arr_points3[i - 1],
                                              arr_points3[i]]) for i
                           in range(1, len(arr_points3))]
        elif not (kwargs.get('arr_xy', None) is None):
            arr_xy = kwargs.get('arr_xy', None)
            self.lines3 = [Line3(xy0=arr_xy[i - 1], xy1=arr_xy[i]) for i
                           in range(1, len(arr_xy))]
        else:
            print("Error! Bad argument:{} {}".format(args, kwargs))

    def __str__(self):
        pass

    # TODO: __getitem__ __setitem__ __str__


"""
#TODO
class Geom3():
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
    l1 = Line3(arr_points3=[p1, p2])
    l2 = Line3(arr_points3=[p2, p3])
    l3 = Line3(xy0=[8, 7, 6], xy1=[5, 4, 3])
    for l in [l1, l2, l3]:
        print(l)
    poly = Poly3(arr_points3=[p1, p2, p3])
