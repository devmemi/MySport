# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 16:16:29 2023

@author: USUARIO
"""

import math
import time

import os



from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys
import pandas as pd

from LoaderClass import *
from AuxiliarFunctions import *
from DataClass import *
#from .AndalusianPopulation_startup1 import *

import typing

from PyQt5.QtCore import Qt, QPoint, QRect, QSize
from PyQt5.QtWidgets import QWidget, QLayout, QLayoutItem, QStyle, QSizePolicy


class FlowLayout(QLayout):
    def __init__(self, parent: QWidget=None, margin: int=-1, hSpacing: int=-1, vSpacing: int=-1):
        super().__init__(parent)

        self.itemList = list()
        self.m_hSpace = hSpacing
        self.m_vSpace = vSpacing

        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        # copied for consistency, not sure this is needed or ever called
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item: QLayoutItem):
        self.itemList.append(item)

    def horizontalSpacing(self) -> int:
        if self.m_hSpace >= 0:
            return self.m_hSpace
        else:
            return self.smartSpacing(QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self) -> int:
        if self.m_vSpace >= 0:
            return self.m_vSpace
        else:
            return self.smartSpacing(QStyle.PM_LayoutVerticalSpacing)

    def count(self) -> int:
        return len(self.itemList)

    def itemAt(self, index: int) -> typing.Union[QLayoutItem, None]:
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        else:
            return None

    def takeAt(self, index: int) -> typing.Union[QLayoutItem, None]:
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        else:
            return None

    def expandingDirections(self) -> Qt.Orientations:
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect: QRect) -> None:
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margins = self.contentsMargins()
        size += QSize(margins.left() + margins.right(), margins.top() + margins.bottom())
        return size

    def smartSpacing(self, pm: QStyle.PixelMetric) -> int:
        parent = self.parent()
        if not parent:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()

    def doLayout(self, rect: QRect, testOnly: bool) -> int:
        left, top, right, bottom = self.getContentsMargins()
        effectiveRect = rect.adjusted(+left, +top, -right, -bottom)
        x = effectiveRect.x()
        y = effectiveRect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.horizontalSpacing()
            if spaceX == -1:
                spaceX = wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            spaceY = self.verticalSpacing()
            if spaceY == -1:
                spaceY = wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)

            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > effectiveRect.right() and lineHeight > 0:
                x = effectiveRect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
    
            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y() + bottom

class JFlowLayout(FlowLayout):
    # flow layout, similar to an HTML `<DIV>`
    # this is our "wrapper" to the `FlowLayout` sample Qt code we have implemented
    # we use it in place of where we used to use a `QHBoxLayout`
    # in order to make few outside-world changes, and revert to `QHBoxLayout`if we ever want to,
    # there are a couple of methods here which are available on a `QBoxLayout` but not on a `QLayout`
    # for which we provide a "lite-equivalent" which will suffice for our purposes

    def addLayout(self, layout: QLayout, stretch: int=0):
        # "equivalent" of `QBoxLayout.addLayout()`
        # we want to add sub-layouts (e.g. a `QVBoxLayout` holding a label above a widget)
        # there is some dispute as to how to do this/whether it is supported by `FlowLayout`
        # see my https://forum.qt.io/topic/104653/how-to-do-a-no-break-qhboxlayout
        # there is a suggestion that we should not add a sub-layout but rather enclose it in a `QWidget`
        # but since it seems to be working as I've done it below I'm elaving it at that for now...

        # suprisingly to me, we do not need to add the layout via `addChildLayout()`, that seems to make no difference
        # self.addChildLayout(layout)
        # all that seems to be reuqired is to add it onto the list via `addItem()`
        self.addItem(layout)

    def addStretch(self, stretch: int=0):
        # "equivalent" of `QBoxLayout.addStretch()`
        # we can't do stretches, we just arbitrarily put in a "spacer" to give a bit of a gap
        w = stretch * 20
        spacerItem = QtWidgets.QSpacerItem(w, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.addItem(spacerItem)



class InterfazDeCarga(QWidget):
    def __init__(self,parent,geometria):
        super().__init__()
        self.resize(200, 100);
        dlggLayout = QVBoxLayout(self)
        self.spinner=QtWaitingSpinner(self)
        dlggLayout.addWidget(self.spinner)
        self.setLayout(dlggLayout)
        self.spinner.start()
        #ventana_error(titulo="Importación finalizada",mensaje="Proceso de importación finalizado correctamente")
        
    def cerrar(self):
        self.spinner.stop()
        self.close()

class VentanaError(QDialog):
    def __init__(self,parent=None,titulo="ERROR",mensaje="Error!"):
        super().__init__()
        self.ventana_errores = QWidget(self)
        self.setWindowTitle(str(titulo))
        self.setGeometry(500, 400, 300, 150)
        vLayout = QVBoxLayout(self)
        self.ventana_errores.setLayout(vLayout)
        
        texto=QPlainTextEdit (str(mensaje))
        texto.setReadOnly(True)
        texto.setStyleSheet("background-color: transparent;")
        texto.setMaximumHeight(100)
        #texto.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        vLayout.addWidget(texto)
        vLayout.addStretch(1)

        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.accepted.connect(self.aceptar)
        self.buttonBox.rejected.connect(self.cerrar)
        vLayout.addWidget(self.buttonBox, alignment=Qt.AlignRight | Qt.AlignBottom)
        #vLayoutAux.addWidget(self.buttonBox)
        
    def cerrar(self):
        self.close()
    def aceptar(self):
        self.accept()



class CustomClickableWidget(QWidget):
    def __init__(self, icon_path, title, description, color):
        super().__init__()
        self.icon_path = icon_path
        self.title = title
        self.description = description
        self.colorHex = color
        self.colorRGB = tuple(int(self.colorHex[i:i+2], 16) for i in (0, 2, 4))
        self.is_hovered = False
        self.animation = None
        self.border_colorStatic = QColor(self.colorRGB[0],self.colorRGB[1],self.colorRGB[2])  # Initial border color
        self.border_colorEvent = QColor(0, 0, 255)  # Change border color to blue
        self.border_color = self.border_colorStatic
        self.setFixedSize(200, 100)
        
    def enterEvent(self, event):
        self.is_hovered = True
        self.border_color = self.border_colorEvent
        self.update()

    def leaveEvent(self, event):
        self.is_hovered = False
        self.border_color = self.border_colorStatic
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Determine the color based on hover state
        rect_color = QColor(200, 200, 200)

        # Draw a rounded rectangle with the updated border color
        path = QPainterPath()
        path.addRoundedRect(QRectF(1, 1, self.width() - 2, self.height() - 2), 10, 10)
        
        border_pen = QPen(self.border_color)
        border_pen.setWidth(5)
        painter.setPen(border_pen)
        painter.setBrush(rect_color)
        painter.drawPath(path)
        border_pen.setWidth(2)

        # Draw the icon
        icon = QPixmap(self.icon_path).scaled(30, 30)
        painter.drawPixmap(10, 10, icon)
        
        #Change color to Black for the text
        painter.setPen(QColor(0, 0, 0))
        
        # Draw the title
        painter.drawText(50, 20, self.title)

        # Draw the description
        painter.drawText(50, 40, self.description)

class DynamicGridLayoutExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # Set the initial number of columns based on the available width
        self.updateGridLayout()

        self.setWindowTitle('Dynamic GridLayout Example')
        self.setGeometry(100, 100, 600, 400)
        self.show()

    def updateGridLayout(self):
        # Clear existing widgets from the layout
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.takeAt(i)
            if item:
                item.widget().deleteLater()

        # Calculate the number of columns based on the available width
        screen_width = self.width()
        max_widget_width = 100  # Maximum width for each widget
        num_columns = max(1, screen_width // max_widget_width)

        # Add widgets to the layout
        for i in range(num_columns):
            label = QLabel(f'Widget {i + 1}')
            self.grid_layout.addWidget(label, 0, i)

    def resizeEvent(self, event):
        # Handle window resize event
        self.updateGridLayout()
        event.accept()

class MainWindow(QMainWindow):
    def __init__(self,parent=None,DataStorageType = 0, nUserKey = 0):
        super().__init__(parent)
        
        self.DataStorageType = DataStorageType    
        self.nUserKey = nUserKey    
        
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.setWindowTitle('Compete vs YOU')
        self.setGeometry(250, 180, 900, 700)
        self.main_widget = QtWidgets.QWidget(self)
        self.main_widget.setFocus(True)
        self.setCentralWidget(self.main_widget)
        self.current_row_width = 0
        self.max_row_width = 500  # Maximum width for a row
        
        self.dlgLayout = QVBoxLayout()
        self.main_widget.setLayout(self.dlgLayout)    
        
        self.tabwidget = QTabWidget()

        #####################################################################
        # Get data
        #####################################################################  
        
        self._createMenuBar()
        self._GetData()
        self._SportScreen()
        self.dlgLayout.addWidget(self.tabwidget, 0)
        self.setLayout(self.dlgLayout)
        self.show()
        
    def _GetData(self):
        if (self.DataStorageType == "0"):
            self.Data = DatabaseData(self.nUserKey)
        elif (self.DataStorageType == "1"):
            self.Data = ExcelData()
        else:
            print(self.DataStorageType)
            VentanaError(titulo="ERROR",mensaje="Data storage type is incorrect").exec()
    
    def _createMenuBar(self):
        menuBar = QMenuBar(self)        
        fileMenu = QMenu("&File",self)
        menuBar.addMenu(fileMenu)
        self.setMenuBar(menuBar)
    
    def _SportScreen(self):
        main_vbox = JFlowLayout()

        main_vbox.setContentsMargins(10, 10, 10, 10)

        # Create rows of widgets
        rows = [
            [("Icon1.png", "Title 1", "Description 1","00FFFF"), ("Icon2.png", "Title 2", "Description 2","00FFFF"),
            ("Icon3.png", "Title 3", "Description 3","00FFFF"), ("Icon4.png", "Title 4", "Description 4","00FFFF"),
            ("Icon5.png", "Title 5", "Description 5","00FFFF"), ("Icon6.png", "Title 6", "Description 6","00FFFF")]
        ]

        for row in rows:

            for icon_path, title, description, color in row:
                # Create and add a custom widget to the current row
                # Replace this with your own widget creation and addition logic
                widget = self._addCustomWidget(icon_path, title, description, color)
                main_vbox.addWidget(widget)

                # Add spacing (empty widgets) between items
#                spacer = QWidget()
#                spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#                hbox.addWidget(spacer)




        # Set the layout for the main window
#        self.setLayout(vbox)
        self.dlgLayout.addLayout(main_vbox)

    
    def _addCustomWidget(self, icon_path, title, description, color):
        # Create and add a custom widget
        widget = CustomClickableWidget(icon_path, title, description, color)
        widget.mousePressEvent = lambda event: self._customWidgetClicked(title)
        
        return widget



    def _customWidgetClicked(self, title):
        print("Custom widget clicked:", title)
    