import sys
from PyQt6 import QtWidgets, QtCore
from access import Ui_MainWindow as AccessUI
from giaodien import Ui_MainWindow as MainUI

class SplashScreen(QtWidgets.QMainWindow, AccessUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        QtCore.QTimer.singleShot(3000, self.open_main_window)  # Hiển thị logo trong 5 giây

    def open_main_window(self):
        self.main_window = MainApp()
        self.main_window.show()
        self.close()

class MainApp(QtWidgets.QMainWindow, MainUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec())
