#!/usr/bin/env python2.7
# -*- coding: utf-8

# python3
from functools import reduce
import types

'''
Shape3
    Point3  self.coords3    self.points3
    Line3                   self.points3
    Poly3   self.lines3     self.points3
    Geom3   self.figures3   self.points3
        Proj3   self.Point3

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

    # Point3([x,y,z])
    def __init__(self, coords3):
        if len(coords3) >= len(self.dict_coord):
            self.coords3 = coords3[:len(self.dict_coord)]
        else:
            self.error_args_message.format(
                args=coords3, kwargs='', nam=self.name)

        self.points3 = [self]

    def __str__(self):
        return "{}({})".format(
            self.name, str(reduce(lambda x, y: '{}, {}'.format(x, y),
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

        # Line3(xy0=[x0,y0,z0],xy1=[x1,y1,z1])
        elif not(kwargs.get('xy0', None) is None and
                 kwargs.get('xy1', None) is None):
            self.points3 = [Point3(xy) for xy in
                            [kwargs.get('xy0'), kwargs.get('xy1')]]

        # Line3(p1,p2)
        # Line3([x0,y0,z0],[x1,y1,z1])
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

        self.points3 = [line.points3[0] for line in
                        self.lines3] + [line.points3[1] for line in
                                        [self.lines3[-1]]]

    # ??? iter points or iter lines ???
    def __iter__(self):
        return iter(self.points3)

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


class Geom3(Shape3):
    name = 'geom'
    arr_types = [Point3, Line3, Poly3]

    figures3 = []
    points3 = []

    def __init__(self):
        pass

    def __str__(self):
        def st(y):
            if len(y) == 0:
                return ''
            elif len(y) == 1:
                return str(y[0])
            else:
                return reduce(lambda a, b: '{}\n{}'.format(a, b), y)

        def tab(n, s):
            return s.replace('\n', '\n' + ' ' * (len(n) + 1))

        arr_str = ['figures', 'points']
        return tab(self.name, '{}(\n{}:{}\n{}:{}\n)'.format(
            self.name, arr_str[0], tab(arr_str[0], '\n' + st(self.figures3)),
            arr_str[1], tab(arr_str[1], '\n' + st(self.points3))))

    def add(self, obj):
        for tp in self.arr_types:
            if isinstance(obj, tp):
                self.figures3.append(obj)
                for p in obj.points3:
                    if filter(lambda x: p is x, self.points3) == []:
                        self.points3.append(p)

    def delete(self, obj):
        for tp in self.arr_types:
            if isinstance(obj, tp):
                if obj in self.figures3:
                    # TODO Delete points also!
                    self.figures3.remove(obj)

    def copy(self, geom_source3, is_append=False):
        def num_in_points_arr(point):
            for i in range(len(geom_source3.points3)):
                if point is geom_source3.points3[i]:
                    return i
        if not is_append:
            self.figures3 = []
            self.points3 = []
        n_points = len(self.points3)
        for p in geom_source3.points3:
            self.points3.append(Point3(p.coords3[:]))
        for f in geom_source3.figures3:
            for tp in self.arr_types:
                if isinstance(f, tp):
                    if tp == Point3:
                        self.figures3.append(
                            self.points3[num_in_points_arr(f) + n_points])
                    else:
                        self.figures3.append(tp(
                            arr_points3=[
                                self.points3[n_points +
                                             num_in_points_arr(p)] for
                                p in f.points3]))

    # Rotate points in plane by normal_vec1 & normal_vec2 by angle
    def rotate(self, nv1, nv2, ang):
        from math import sin, cos
        rot2 = [[cos, lambda x: -sin(x)], [sin, cos]]

        l_mat_rot = [[(lambda x: 0, lambda x: 1)[i == j]
                      for j in range(len(self.dict_coord))]
                     for i in range(len(self.dict_coord))]

        for i in zip([nv1, nv2], [0, 1]):
            for j in zip([nv1, nv2], [0, 1]):
                l_mat_rot[i[0]][j[0]] = rot2[i[1]][j[1]]

        mat_rot = [[lam(ang) for lam in st] for st in l_mat_rot]

        def matmult(a, b, func=lambda x, y: x * y):
            zip_b = zip(*b)
            # uncomment next line if python 3 :
            # zip_b = list(zip_b)
            return [[sum(func(ele_a, ele_b) for ele_a, ele_b in
                         zip(row_a, col_b))
                     for col_b in zip_b] for row_a in a]

        for p in self.points3:
            p.coords3 = matmult([p.coords3], mat_rot)


class Proj2(Geom3):
    name = 'proj'

    def __init__(self, vec_point3, vec_rot_point3, geom_source3):
        self.geom2 = Geom3()
        self.geom2.dict_coord = {'x': 0, 'y': 1}

        self.geom_source3 = Geom3()
        self.geom_source3.copy(geom_source3)

        from math import sqrt

        # Normalise
        vec_point3_c = [vec_point3.coords3[:], vec_rot_point3.coords3[:]]
        r_vec_point3 = [sqrt(sum([i * i for i in v])) for v in vec_point3_c]
        vec_point3_c = [[i / r_vec_point3[j]
                         for i in vec_point3_c[j]] for j in [0, 1]]

        # TODO check vec* are orts (ang = pi/2)

        self.vec_point3 = Point3(vec_point3_c[0])
        self.vec_rot_point3 = Point3(vec_point3_c[1])

        self.geom_source3.add(self.vec_point3)
        self.geom_source3.add(self.vec_rot_point3)

        """
        |y
        |
        .z_____x

        vec_point3 =        [0,0,1]
        vec_rot_point3 =    [1,0,0]

        """

        # Rotation: vec_rot_point['z'] -> 0
        Xxz = self.vec_rot_point3['x']
        Zxz = self.vec_rot_point3['z']
        from cmath import phase
        a1 = phase(complex(Xxz, -Zxz))
        self.geom_source3.rotate(0, 2, -a1)

        # Rotation: vec_rot_point['y'] -> 0
        Xxy = self.vec_rot_point3['x']
        Yxy = self.vec_rot_point3['y']
        a2 = phase(complex(Xxy, Yxy))
        self.geom_source3.rotate(0, 1, -a2)

        # Rotation: vec_point['y'] -> 0
        Yyz = self.vec_point3['y']
        Zyz = self.vec_point3['z']
        a3 = phase(complex(Zyz, Yyz))
        self.geom_source3.rotate(1, 2, -a3)
        # /Rotations

        self.geom_source3.delete(self.vec_point3)
        self.geom_source3.delete(self.vec_rot_point3)
        # TODO rotate


# TODO  Projection with matrix! -> by rotation
#       Rotation with matrix (+ around any point)


if __name__ == '__main__':
    p1 = Point3([1, 2, 3])
    p2 = Point3([4, 5, 6])
    p3 = Point3([5, 6, 7])
    """
    l1 = Line3(arr_points3=[p1, p2])
    l2 = Line3(arr_points3=[p2, p3])
    poly1 = Poly3(arr_points3=[p1, p2, p3])
    """
    l3 = Line3(xy0=[1, 2, 3], xy1=[5, 4, 3])
    p1['x'] = 1
    poly2 = Poly3(p1, p2, p3)
    # print(poly2)

    g = Geom3()
    g.add(poly2)
    g.add(p1)
    g.add(l3)
    g2 = Geom3()
    g2.copy(g)
    print(g)
    import math
    g.rotate(0, 1, math.pi)
    print(g)
    pz = Point3([0, 0, 1])
    px = Point3([1, 0, 0])
    prj = Proj2(pz, px, g)
