import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6.QtGui import QIcon
from login import Ui_Form as LoginUI
from signup import Ui_Form as SignupUI


ACC_FILE = "acc.json"

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = LoginUI()
        self.ui.setupUi(self)

        self.ui.label_6.setStyleSheet("image: url(icons/working.png);")
        # Gán sự kiện cho các nút
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pBsignup.clicked.connect(self.open_signup)
        self.ui.pBeye.clicked.connect(self.toggle_password_visibility)  # Gán sự kiện cho pBeye
        # Nhấn Enter khi ở Username → chuyển xuống Password
        self.ui.lineEdit.returnPressed.connect(self.focus_on_password)

        # Nhấn Enter khi ở Password → click vào Login
        self.ui.lineEdit_2.returnPressed.connect(self.ui.pushButton.click)
        # Mặc định ẩn mật khẩu
        self.password_visible = False
        self.ui.lineEdit_2.setEchoMode(self.ui.lineEdit_2.EchoMode.Password)
        self.ui.pBeye.setIcon(QIcon("icons/hide.png"))

    def focus_on_password(self):
        """Chuyển focus từ username xuống password khi nhấn Enter"""
        self.ui.lineEdit_2.setFocus()

    def toggle_password_visibility(self):
        """Hiện/Ẩn mật khẩu khi nhấn vào pBeye"""
        if self.password_visible:
            self.ui.lineEdit_2.setEchoMode(self.ui.lineEdit_2.EchoMode.Password)
            self.ui.pBeye.setIcon(QIcon("icons/hide.png"))
        else:
            self.ui.lineEdit_2.setEchoMode(self.ui.lineEdit_2.EchoMode.Normal)
            self.ui.pBeye.setIcon(QIcon("icons/view.png"))
        self.password_visible = not self.password_visible

    def login(self):
        """Xử lý đăng nhập"""
        username = self.ui.lineEdit.text().strip()
        password = self.ui.lineEdit_2.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            with open(ACC_FILE, "r") as file:
                accounts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            accounts = {}

        if username in accounts and accounts[username] == password:
            QMessageBox.information(self, "Thành công", "Đăng nhập thành công!")

            from main import MainApp
            self.main_window = MainApp(username)
            self.main_window.show()

            self.close()
        else:
            QMessageBox.warning(self, "Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")



    def open_signup(self):
        """Mở giao diện đăng ký"""
        self.signup_window = SignupWindow()
        self.signup_window.show()
        self.close()

class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = SignupUI()
        self.ui.setupUi(self)

        # Gán sự kiện
        self.ui.label_6.setStyleSheet("image: url(icons/working.png);")
        self.ui.pushButton.clicked.connect(self.signup)
        self.ui.pushButton_2.clicked.connect(self.toggle_password_visibility)  # Gán sự kiện cho pushButton_2
        # Nhấn Enter khi ở Username → Chuyển xuống Password
        self.ui.lineEdit.returnPressed.connect(self.focus_on_password)

        # Nhấn Enter khi ở Password → Click vào Đăng ký
        self.ui.lineEdit_2.returnPressed.connect(self.ui.pushButton.click)
        # Mặc định ẩn mật khẩu
        self.password_visible = False
        self.ui.lineEdit_2.setEchoMode(self.ui.lineEdit_2.EchoMode.Password)
        self.ui.pushButton_2.setIcon(QIcon("icons/hide.png"))

    def focus_on_password(self):
        """Chuyển focus từ username xuống password khi nhấn Enter"""
        self.ui.lineEdit_2.setFocus()

    def toggle_password_visibility(self):
        """Hiện/Ẩn mật khẩu khi nhấn vào pushButton_2"""
        if self.password_visible:
            self.ui.lineEdit_2.setEchoMode(self.ui.lineEdit_2.EchoMode.Password)
            self.ui.pushButton_2.setIcon(QIcon("icons/hide.png"))
        else:
            self.ui.lineEdit_2.setEchoMode(self.ui.lineEdit_2.EchoMode.Normal)
            self.ui.pushButton_2.setIcon(QIcon("icons/view.png"))
        self.password_visible = not self.password_visible

    def signup(self):
        """Xử lý đăng ký"""
        username = self.ui.lineEdit.text().strip()
        password = self.ui.lineEdit_2.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            with open(ACC_FILE, "r") as file:
                accounts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            accounts = {}

        if username in accounts:
            QMessageBox.warning(self, "Lỗi", "Tài khoản đã tồn tại!")
            return

        accounts[username] = password
        with open(ACC_FILE, "w") as file:
            json.dump(accounts, file, indent=4)

        QMessageBox.information(self, "Thành công", "Đăng ký thành công!")
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
