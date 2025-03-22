import sys
import json
from PyQt6 import QtWidgets, QtCore
from access import Ui_MainWindow as AccessUI
from Run_app import LoginWindow  # Đăng nhập
from giaodien import Ui_MainWindow as MainUI  # Giao diện chính
from grammar_ex import GrammarApp  # Bài tập grammar 1
from grammar2_ex import GrammarAppV2  # Bài tập grammar 2
from flashcard1_ex import FlashcardApp as Flashcard1
from flashcard2_ex import FlashcardApp as Flashcard2
from flashcard3_ex import FlashcardApp as Flashcard3


class SplashScreen(QtWidgets.QMainWindow, AccessUI):
    def __init__(self):
        super().__init__()
        self.login_window = None
        self.setupUi(self)
        self.show()
        QtCore.QTimer.singleShot(2000, self.open_login)  # Hiển thị logo 3 giây

    def open_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

class MainApp(QtWidgets.QMainWindow):
    def __init__(self, username="Guest"):
        super().__init__()
        self.ui = MainUI()
        self.ui.setupUi(self)
        # Hiển thị tên người dùng
