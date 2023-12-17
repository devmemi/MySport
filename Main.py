# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 11:08:45 2023

@author: USUARIO
"""

import math
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize  

import sys
import os
import locale

from InterfaceClass import *
from AuxiliarFunctions import *


def main():   
    Config=ReadConfig()
    app = QtWidgets.QApplication(sys.argv)
    MapaWindow = MainWindow(parent=None, DataStorageType = Config[0], nUserKey = 1)
    app.exec_()



if __name__ == "__main__":
    def run_app():
        main()
    run_app()
    