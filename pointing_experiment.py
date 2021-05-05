#!/usr/bin/python3

import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import random
import time
import pandas as pd
from datetime import datetime


class Experiment(QtWidgets.QWidget):
    # init all necessary variables
    def __init__(self):
        super().__init__()
        self.init_ui()

    # init UI
    def init_ui(self):
        self.showMaximized()
        self.setWindowTitle('Color Test')
        # widget should accept focus by click and tab key
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    # variable is never used, class automatically registers itself for Qt main loop:
    experiment = Experiment()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
