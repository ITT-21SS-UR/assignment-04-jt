#!/usr/bin/python3
import os.path
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint
import random
import math
import configparser
import json

from PyQt5.QtGui import QPolygon
from PyQt5.QtWidgets import QWidget


class ExperimentModel(object):
    # init all necessary variables
    def __init__(self, user_id, radius, repetitions, amount):
        self.timer = QtCore.QTime()
        self.start_pointer = ()
        self.user_id = user_id
        self.radius = radius
        self.repetitions = repetitions
        self.amount = amount
        self.conditions = (1, 2, 3)
        self.targets = []
        # possibilities = list(itertools.product(radius, amount))
        for i in self.conditions:
            for y in range(repetitions):
                curr_rad = random.choice(radius)
                self.targets.append((i, curr_rad, amount))
        random.shuffle(self.targets)
        self.through = 0
        self.mouse_moving = False
        sys.stdout.write("timestamp (ISO); user_id; condition; radius; amount; completion_time (ms); "
                         "start_pointer_x, start_pointer_y, end_pointer_x, end_pointer_y, error \n")

    def current_target(self):
        if self.through >= len(self.targets):
            return None
        else:
            return self.targets[self.through]

    def set_start_pointer(self, position):
        self.start_pointer = position

    def register_click(self, target_pos, click_pos):
        dist = math.sqrt((target_pos[0] - click_pos[0]) * (target_pos[0] - click_pos[0]) +
                         (target_pos[1] - click_pos[1]) * (target_pos[1] - click_pos[1]))
        if dist > self.current_target()[1]:
            # click_offset = (target_pos[0] - click_pos[0], target_pos[1] - click_pos[1])
            error = False
            # self.start_pointer
            self.log_time(self.stop_measurement(), error, self.start_pointer, click_pos)
        else:
            QtGui.QCursor.pos()
            # click_offset = (target_pos[0] - click_pos[0], target_pos[1] - click_pos[1])
            error = True
            self.log_time(self.stop_measurement(), error, self.start_pointer, click_pos)
        self.through += 1

    def log_time(self, time, error, start_pointer, end_pointer):
        conditions, radius, amount = self.current_target()
        sys.stdout.write("%s; %s; %d; %d; %d; %d; %d; %d; %d; %d; %s \n" % (self.timestamp(), self.user_id, conditions,
                                                                            radius, amount, time, start_pointer[0],
                                                                            start_pointer[1], end_pointer[0],
                                                                            end_pointer[1], error))

    def start_measurement(self):
        if not self.mouse_moving:
            self.timer.start()
            self.mouse_moving = True

    def stop_measurement(self):
        if self.mouse_moving:
            elapsed = self.timer.elapsed()
            self.mouse_moving = False
            return elapsed

    def timestamp(self):
        return QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)


class ExperimentTest(QtWidgets.QWidget):
    # init all necessary variables
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.start_pos = (100, 100)
        self.target_x = 0
        self.target_y = 0
        self.colors = [(60, 168, 50), (168, 50, 50), (255, 215, 0)]
        self.forms = ['rect', 'triangle', 'circle']
        self.init_ui()

    # init UI
    def init_ui(self):
        self.showMaximized()
        self.setWindowTitle('Click Test')
        # widget should accept focus by click and tab key
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMouseTracking(True)
        self.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.model.register_click((self.target_x, self.target_y), (event.x(), event.y()))
            self.update()

    #def mouseMoveEvent(self, event):
    #    if (abs(event.x() - self.start_pos[0]) > 5) or (abs(event.y() - self.start_pos[1]) > 5):
    #        self.model.start_measurement()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        position = (QWidget.mapFromGlobal(self, QtGui.QCursor.pos()).x(),
                    QWidget.mapFromGlobal(self, QtGui.QCursor.pos()).y())
        self.model.set_start_pointer(position)
        self.draw_target(event, qp)
        self.draw_text(event, qp)
        qp.end()

    def draw_text(self, event, qp):
        # qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 32))
        self.text = "Click on the BLUE CIRCLE"
        qp.drawText(event.rect(), QtCore.Qt.AlignLeft, self.text)

    def draw_target(self, event, qp):
        self.model.start_measurement()
        if self.model.current_target() is not None:
            conditions, radius, amount = self.model.current_target()
        else:
            sys.stderr.write("no targets left...")
            sys.exit(1)
        if conditions == 1:
            target = random.randrange(0, amount)
            for i in range(amount):
                x = random.randrange(100, 1800, 20)
                y = random.randrange(100, 800, 20)
                qp.setPen(Qt.SolidLine)
                if i == target:
                    self.target_x = x
                    self.target_y = y
                    qp.setBrush(QtGui.QColor(54, 50, 168))
                else:
                    qp.setBrush(QtGui.QColor(0, 0, 0, 0))
                qp.drawEllipse(x - radius, y - radius, radius, radius)
        elif conditions == 2:
            target = random.randrange(0, amount)
            for i in range(amount):
                color = random.choice(self.colors)
                x = random.randrange(100, 1800, 20)
                y = random.randrange(100, 800, 20)
                qp.setPen(Qt.SolidLine)
                if i == target:
                    self.target_x = x
                    self.target_y = y
                    qp.setBrush(QtGui.QColor(54, 50, 168))
                else:
                    qp.setBrush(QtGui.QColor(color[0], color[1], color[2]))
                qp.drawEllipse(x - radius, y - radius, radius, radius)
        elif conditions == 3:
            target = random.randrange(0, amount)
            for i in range(amount):
                color = random.choice(self.colors)
                form = random.choice(self.forms)
                x = random.randrange(100, 1800, 20)
                y = random.randrange(100, 800, 20)
                qp.setPen(Qt.SolidLine)
                if i == target:
                    self.target_x = x
                    self.target_y = y
                    qp.setBrush(QtGui.QColor(54, 50, 168))
                    qp.drawEllipse(x - radius, y - radius, radius, radius)
                else:
                    qp.setBrush(QtGui.QColor(color[0], color[1], color[2]))
                    if form == 'rect':
                        qp.drawRect(x - radius, y - radius, radius, radius)
                    elif form == 'triangle':
                        points = [
                            QPoint(x - radius, y - radius),
                            QPoint(x - radius + 10, y - radius + 100),
                            QPoint(x - radius + 100, y - radius + 10),
                        ]
                        poly = QPolygon(points)
                        qp.drawPolygon(poly)
                    elif form == 'circle':
                        qp.drawEllipse(x - radius, y - radius, radius, radius)


def main():
    app = QtWidgets.QApplication(sys.argv)
    if len(sys.argv) < 2:
        sys.stderr.write("No file given")
        sys.exit(1)
    values = get_setup_values(sys.argv[1])
    model = ExperimentModel(*get_setup_values(sys.argv[1]))
    experiment = ExperimentTest(model)
    sys.exit(app.exec_())


def get_setup_values(filename):
    name, extension = os.path.splitext(filename)
    if extension == '.ini':
        config = configparser.ConfigParser()
        config.read(filename)
        user_id = config['default']['user']
        radius = []
        rad = (config['default']['radius']).split()
        for i in rad:
            radius.append(int(i))
        repetitions = int(config['default']['repetitions'])
        amount = int(config['default']['amount'])
    elif extension == '.json':
        json_file = json.loads(open(filename).readline())
        user_id = json_file['user']
        radius = json_file['radius']
        repetitions = json_file['repetitions']
        amount = json_file['amount']
    return user_id, radius, repetitions, amount


if __name__ == '__main__':
    main()
