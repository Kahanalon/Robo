#!/usr/bin/env python3

import importlib
import os
import CGALPY_add_dlls
import math
import basic_gui_example

os.add_dll_directory("C:/Users/Alon/Documents/Robot/FDML-Build/src/libs/fdml/Release")
import fdmlpy
import argparse
import CGALPY_kerEpec_aos2ArrSeg_bso2_pol2 as CGALPY

front_first = 1
back_first = 7
front_second = 2
back_second = 6
front_third = math.sqrt(2)
back_third = 2*math.sqrt(2)
front_fourth = math.sqrt(2)
back_fourth = 2*math.sqrt(2)


def readable_dir(prospective_dir):
    # Determine whether the given directory exists and readable
    parser = argparse.ArgumentParser(description='Self locate.')
    if not os.path.isdir(prospective_dir):
        parser.error("The directory{} does not exist!".format(prospective_dir))
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        parser.error(
            "The directory {} is not a readable dir!".format(prospective_dir))


def read_polygon(inp, library):
    # CGALPY = importlib.import_module(library)
    Polygon = CGALPY.Pol2.Polygon_2
    pgn = Polygon()
    Ker = fdmlpy.Ker
    Point = Ker.Point_2
    n = int(inp.readline())
    for i in range(n):
        line = inp.readline()
        lst = line.split()
        p = Point(float(lst[0]), float(lst[1]))
        pgn.push_back(p)
    return pgn


def read_polygon_with_holes(inp, library):
    # CGALPY = importlib.import_module(library)
    Polygon_with_holes_2 = CGALPY.Pol2.Polygon_with_holes_2
    boundary = read_polygon(inp, library)
    pgnwh = Polygon_with_holes_2(boundary)
    n = int(inp.readline())
    for i in range(n):
        pgnwh.add_hole(read_polygon(inp, library))
    return pgnwh


def main():
    parser = argparse.ArgumentParser(description='Self locate.')
    parser.add_argument('filename', metavar="filename", nargs='?',
                        help='the input file name', default='./locate_pgn.txt')
    parser.add_argument('--input-path', type=readable_dir, nargs='*',
                        dest="input_paths", default='./')
    parser.add_argument('--library', default='CGALPY', dest="library")
    args = parser.parse_args()
    input_path = args.input_paths

    filename = args.filename
    fullname = None
    for path in args.input_paths:
        tmp = os.path.join(path, filename)
        if os.path.exists(tmp):
            fullname = tmp
            break

    if not fullname:
        parser.error("The file %s cannot be found!" % filename)
        exit(-1)

    lib = args.library
    print('Library name:', lib)
    # CGALPY = importlib.import_module(lib)

    Locator = fdmlpy.Locator
    Ker = fdmlpy.Ker
    Point = Ker.Point_2
    FT = Ker.FT
    l = Locator()
    Polygon = CGALPY.Pol2.Polygon_2
    Polygon_with_holes_2 = CGALPY.Pol2.Polygon_with_holes_2

    with open(fullname, 'r') as inp:
        pgnwh = read_polygon_with_holes(inp, lib)
        print(pgnwh)

        l.init(pgnwh)
        res_first = l.query2(FT(front_first), FT(back_first))
        res_second = l.query2(FT(front_second), FT(back_second))
        res_third = l.query2(FT(front_third), FT(back_third))
        res_fourth = l.query2(FT(front_fourth), FT(back_fourth))
        gui = basic_gui_example.run_gui(filename, res_first, res_second, res_third, res_fourth)

        # basic_gui_example.GUITest.(filename,res_first,res_second)
        # res = l.query1(FT(1))
        # print(type(res[0][0]))
        # print(f"q1: {res[0][0]}")
        # print(pgns)

        PS = CGALPY.Bso2.Polygon_set_2
        ps = PS()
        l = []
        for r in res:
            pgn = Polygon()
            it = r[0].vertices()
            last = next(it)
            first = last
            for p in it:
                if p != last:
                    pgn.push_back(p)
                    last = p
                if first != last:
                    pgn.push_back(first)
            l.append(pgn)
        ps.insert(l, [])
        arr = ps.arrangement()
        # print(arr.number_of_vertices(),
        #       arr.number_of_halfedges(), arr.number_of_faces())


def run_efi(dis0, dis180, dis90, dis270, dis45, dis225, dis135, dis315):
    global front_first, back_first, front_second, back_second, front_third, back_third, front_fourth, back_fourth
    front_first = dis0
    back_first = dis180
    front_second = dis90  # check rotation direction
    back_second = dis270
    front_third = dis45
    back_third = dis225
    front_fourth = dis135
    front_fourth = dis315

    main()


if __name__ == "__main__":
    main()
