#!/usr/bin/python3

import os.path
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPolygon
from PyQt5.QtWidgets import QWidget
import random
import math
import configparser
import json

""" .ini file looks like this:
[default]
user = 1
radius = 50 75 100 125
repetitions = 5
amount = 20

.json file looks like this:
{"user": 1, "radius": [50, 75, 100, 125], "repetitions" : 5, "amount": 20}
"""


class ExperimentModel(object):
    # init all necessary variables
    def __init__(self, user_id, radius, repetitions, amount):
        self.timer = QtCore.QTime()
        self.user_id = user_id
        self.radius = radius
        self.repetitions = repetitions
        self.amount = amount
        self.start_pointer = ()
        self.conditions = (1, 2, 3)
        self.forms = []
        # possibilities = list(itertools.product(radius, amount))
        for i in self.conditions:
            for y in range(repetitions):
                curr_rad = random.choice(radius)
                self.forms.append((i, curr_rad, amount))
        random.shuffle(self.forms)
        self.cycle = 0
        # self.mouse_moving = False
        sys.stdout.write("timestamp (ISO); user_id; condition; radius; amount; completion_time (ms); "
                         "start_pointer_x, start_pointer_y, end_pointer_x, end_pointer_y, error \n")

    # returns the current state. Includes condition, radius and amount of forms
    def current_state(self):
        if self.cycle >= len(self.forms):
            return None
        else:
            return self.forms[self.cycle]

    # sets coordinates for the starting position of the cursor
    def set_start_pointer(self, position):
        self.start_pointer = position

    # registers the click and if it is correct
    def register_click(self, target_pos, click_pos):
        dist = math.sqrt((target_pos[0] - click_pos[0]) * (target_pos[0] - click_pos[0]) +
                         (target_pos[1] - click_pos[1]) * (target_pos[1] - click_pos[1]))
        if dist > self.current_state()[1]:
            # click_offset = (target_pos[0] - click_pos[0], target_pos[1] - click_pos[1])
            error = False
        else:
            # click_offset = (target_pos[0] - click_pos[0], target_pos[1] - click_pos[1])
            error = True
        self.log_experiment(self.stop_measurement(), error, self.start_pointer, click_pos)
        self.cycle += 1

    # logs all necessary information to stdout
    def log_experiment(self, time, error, start_pointer, end_pointer):
        conditions, radius, amount = self.current_state()
        timestamp = QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)
        sys.stdout.write("%s; %s; %d; %d; %d; %d; %d; %d; %d; %d; %s \n" % (timestamp, self.user_id, conditions,
                                                                            radius, amount, time, start_pointer[0],
                                                                            start_pointer[1], end_pointer[0],
                                                                            end_pointer[1], error))

    # start time measurement
    def start_measurement(self):
        # if not self.mouse_moving:
        self.timer.start()
        # self.mouse_moving = True

    # stops time measurement
    def stop_measurement(self):
        # if self.mouse_moving:
        elapsed = self.timer.elapsed()
        # self.mouse_moving = False
        return elapsed

    # def timestamp(self):
    #    return QtCore.QDateTime.currentDateTime().toString(QtCore.Qt.ISODate)


class ExperimentTest(QtWidgets.QWidget):
    # init all necessary variables
    def __init__(self, model):
        super().__init__()
        self.model = model
        # self.start_pos = (100, 100)
        self.target_x = 0
        self.target_y = 0
        # colors: green, red, yellow
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

    # when the mouse is pressed, register a click in the model and update to new condition
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.model.register_click((self.target_x, self.target_y), (event.x(), event.y()))
            self.update()

    # def mouseMoveEvent(self, event):
    #    if (abs(event.x() - self.start_pos[0]) > 5) or (abs(event.y() - self.start_pos[1]) > 5):
    #        self.model.start_measurement()

    # paintEvent gets starting position of the cursor and draws the instruction and forms
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        start_position = (QWidget.mapFromGlobal(self, QtGui.QCursor.pos()).x(),
                          QWidget.mapFromGlobal(self, QtGui.QCursor.pos()).y())
        self.model.set_start_pointer(start_position)
        self.draw_forms(qp)
        self.draw_text(event, qp)
        qp.end()

    # draws the instruction
    def draw_text(self, event, qp):
        # qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 32))
        self.text = "Click on the BLUE CIRCLE"
        qp.drawText(event.rect(), QtCore.Qt.AlignLeft, self.text)

    # draws the different forms according to condition
    def draw_forms(self, qp):
        self.model.start_measurement()
        if self.model.current_state() is not None:
            conditions, radius, amount = self.model.current_state()
        else:
            sys.stderr.write("Finished!")
            sys.exit(1)
        if conditions == 1:
            self.draw_first_cond(qp, amount, radius)
        elif conditions == 2:
            self.draw_second_cond(qp, amount, radius)
        elif conditions == 3:
            self.draw_third_cond(qp, amount, radius)

    # draws the first condition with circles without color except the target
    def draw_first_cond(self, qp, amount, radius):
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

    # draws the second condition with circles in multiple colors
    def draw_second_cond(self, qp, amount, radius):
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

    # draws the third condition with multiple different forms and colors
    def draw_third_cond(self, qp, amount, radius):
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
                        QPoint(x - radius*2, y - radius),
                        QPoint(x - radius, y - radius*2),
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
    # values = get_setup_values(sys.argv[1])
    model = ExperimentModel(*get_setup_values(sys.argv[1]))
    experiment = ExperimentTest(model)
    sys.exit(app.exec_())


def get_setup_values(filename):
    name, extension = os.path.splitext(filename)
    user_id = 0
    radius = []
    repetitions = 0
    amount = 0
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
