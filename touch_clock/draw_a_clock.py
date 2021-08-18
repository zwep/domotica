import PyQt5.QtGui
import PyQt5.QtGui as QtGui
import PyQt5.QtCore
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets
import PyQt5.QtWidgets as QtWidgets
import sys


class MyWidget(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 600, 600)
        painter_obj = self.draw_circle(None)

        # Create menu shortcuts...
        exit_action = self.get_action(icon_name='exit.png',
                                      action_name='&Exit',
                                      shortcut='Ctrl+Q',
                                      connect=PyQt5.QtWidgets.qApp.quit,
                                      description='Exit application')
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(exit_action)


        self.setCentralWidget(painter_obj)

    def draw_circle(self, event):
        painter = QtGui.QPainter(self)
        painter.begin(self)
        # painter.setPen(QtGui.QPen(QtGui.Qt.green,  8, QtGui.Qt.DashLine))
        painter.drawEllipse(40, 40, 400, 400)
        return painter

    def get_action(self, icon_name, action_name, shortcut, description, connect=None):
        qt_action = PyQt5.QtWidgets.QAction(PyQt5.QtGui.QIcon(icon_name), action_name, self)
        qt_action.setShortcut(shortcut)
        qt_action.setStatusTip(description)
        if connect is not None:
            qt_action.triggered.connect(connect)

        return qt_action



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    # app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())