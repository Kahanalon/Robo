"""
This is a minimal example that demonstrates usage of all different Qt GUI objects
that are available on this framework.
"""

import sys
import re

sys.path.append('./src/')

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog

from discopygal.gui.gui import GUI


class GUITest(GUI):
    def setupUi(self, path):
        #########################
        # Setup the Qt UI layout
        #########################
        # Resize the main window and set the stylesheet (CSS)
        MainWindow = self.mainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("QMainWindow { background-color : rgb(54, 57, 63); color : rgb(220, 221, 222); }\n"
                                 "QLabel { background-color : rgb(54, 57, 63); color : rgb(220, 221, 222); }")

        # Add a graphics widget to the main window
        self.graphicsView = QtWidgets.QGraphicsView(self.mainWindow)
        self.graphicsView.setEnabled(True)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 780, 580))
        self.graphicsView.setObjectName("graphicsView")

        # Zoom out a bit
        self.zoom = 40

        #########################
        # RMP Gui Zoo
        #########################
        # self.add_text("RText", 0.0, 4.0, 1)
        # self.add_text("This is some text", -2.0, 3.0, 1)

        # self.add_text("RPolygon", 4.0, 4.0, 1)
        # points = [(0.0, 0.0), (0.0, 2.0), (1.0, 1.0), (2.0, 2.0), (2.0, 0.0)]
        # self.add_polygon(list(map(lambda p: (p[0], p[1]), points)), QtCore.Qt.transparent)

        # self.add_text("RSegment", 0.0, 0.0, 1)
        # todo create func create grid (n)
        def create_grid(n):
            for i in range(1, n):
                self.add_segment(i, -100, i, 100, line_color=QtCore.Qt.gray)
                self.add_segment(-100, i, 100, i, line_color=QtCore.Qt.gray)
                self.add_segment(-i, -100, -i, 100, line_color=QtCore.Qt.gray)
                self.add_segment(-100, -i, 100, -i, line_color=QtCore.Qt.gray)
                self.add_segment(i+.5, -100, i+.5, 100, line_color=QtCore.Qt.gray, opacity=0.4)
                self.add_segment(-100, i+.5, 100, i+.5, line_color=QtCore.Qt.gray, opacity=0.4)
                self.add_segment(-i+.5, -100, -i+.5, 100, line_color=QtCore.Qt.gray, opacity=0.4)
                self.add_segment(-100, -i+.5, 100, -i+.5, line_color=QtCore.Qt.gray, opacity=0.4)

            self.add_segment(0, -100, 0, 100)
            self.add_segment(-100, 0, 100, 0)
            self.add_segment(0.5, -100, 0.5, 100, line_color=QtCore.Qt.gray, opacity=0.4)
            self.add_segment(-100, 0.5, 100, 0.5, line_color=QtCore.Qt.gray, opacity=0.4)

        # todo create room list[list]
        def create_poly(points, line_color):
            n = len(points)
            for i in range(1, n):
                self.add_segment(int(points[i - 1][0]), int(points[i - 1][1]), int(points[i][0]), int(points[i][1]),
                                 line_color)
            self.add_segment(int(points[0][0]), int(points[0][1]), int(points[n - 1][0]), int(points[n - 1][1]),
                             line_color)

        def create_room(path, n):
            create_grid(n)
            with open(path, 'r') as f:
                num = f.readline()[0]
                points = []
                for i in range(int(num)):
                    point = f.readline()
                    rr = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", point)
                    points.append(rr)
                create_poly(points, QtCore.Qt.red)
                holes = int(f.readline()[0])
                for i in range(int(holes)):
                    num = f.readline()[0]
                    points = []
                    for i in range(int(num)):
                        point = f.readline()
                        rr = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", point)
                        points.append(rr)
                    create_poly(points, QtCore.Qt.red)

        def draw_answer(answer, line_color):
            for ans in answer:
                points = []
                if len(ans[2]) == 0:
                    continue
                if len(ans[2]) == 1:
                    self.add_disc(0.1, ans[2][0], ans[2][1])
                for p in ans[2]:
                    points.append(p[0], p[1])
                create_poly(points, line_color)



        def show_answer(path, res1, res2):
            app = QtWidgets.QApplication(sys.argv)
            gui = GUITest()
            gui.set_program_name("RMP GUI Zoo")
            gui.mainWindow.show()
            create_room(path)
            draw_answer(res1, QtCore.Qt.blue)
            draw_answer(res2, QtCore.Qt.green)
            sys.exit(app.exec_())

        create_room(path, 100)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = GUITest()
    gui.set_program_name("RMP GUI Zoo")
    gui.mainWindow.show()
    sys.exit(app.exec_())
else:
    app = QtWidgets.QApplication(sys.argv)
    gui = GUITest()
    gui.set_program_name("RMP GUI Zoo")
    gui.mainWindow.show()
    sys.exit(app.exec_())
