from PyQt6.QtWidgets import QApplication,QMainWindow,QMessageBox
from login import Ui_Form
from main import Ui_MainWindow
import json
import sys
import os
user_file = "acc.json"
class MainApp(QMainWindow):# Kế thừa từ QMainWindow
    def __init__(self):
        super().__init__()
        self.login_ui = Ui_Form()  # Giao diện đăng nhập
        self.main_window = QMainWindow()  # Cửa sổ chính (main)
        self.load_login()
    def load_login(self):
        self.login_ui.setupUi(self) # Thiết lập giao diện
        self.login_ui.pushButton.clicked.connect(self.login)
        self.show()
    def load_main(self):
        self.main_ui = Ui_MainWindow()  # Giao diện Main
        self.main_ui.setupUi(self.main_window)  # Thiết lập giao diện Main
        self.main_window.show()  # Hiển thị cửa sổ chính

    def load_users(self):
        """ Đọc danh sách người dùng từ file JSON """
        if not os.path.exists(user_file):  # Nếu file không tồn tại
            with open(user_file, "w", encoding="utf-8") as file:
                json.dump({"users": []}, file, indent=4)  # Tạo file với danh sách rỗng
            return []
        try:
            with open(user_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                if "users" in data:
                    return data["users"]
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Trả về danh sách rỗng khi file không tồn tại hoặc bị lỗi

    def save_users(self, users):
        with open(user_file, "w", encoding="utf-8") as file:
            json.dump({"users": users}, file, indent=4)

    def login(self):
            username = self.login_ui.lineEdit.text().strip()
            password = self.login_ui.lineEdit_2.text().strip()

            if username == '' or password == '':
                QMessageBox.information(self, "Notification", "Please enter both username and password")
                return
            if "uel.edu.vn" not in password:
                QMessageBox.warning(self, "Error login", "Password must have 'uel.edu.vn'.")
                return
            users = self.load_users()
            password_owner = None
            for user in users:
                if password in user["passwords"]:
                    password_owner = user
                    break
            if password_owner:
                # Nếu password đã có nhưng username khác => Lỗi
                if password_owner["username"] != username:
                    QMessageBox.warning(self, "Error", "This password is already linked to another username!")
                    return
                else:
                    QMessageBox.information(self, "Success", "Login successful! Welcome back.")
                    return
            # Nếu password chưa tồn tại, kiểm tra username, thì khi một username đăng nhập với một mật khẩu mới, hệ thống sẽ lưu mật khẩu đó. Khi đó, lần sau họ sẽ đăng nhập được bằng mật khẩu mới.
            existing_user = None
            for user in users:
                if user["username"] == username:
                    existing_user = user
                    break

            if existing_user:
                existing_user["passwords"].append(password)  # Thêm mật khẩu mới cho username cũ
                self.save_users(users)
                QMessageBox.information(self, "Success", "New password added for existing user!")
            else:
                users.append({"username": username, "passwords": [password]})  # Tạo tài khoản mới
                self.save_users(users)
                QMessageBox.information(self, "Success", "New account created and logged in!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    sys.exit(app.exec())
