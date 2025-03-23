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
        self.username = username
        self.ui.lblname.setText(self.username)

        # Cấu hình các nút mở bài tập
        self.ui.pBtense.clicked.connect(lambda: self.open_window(GrammarApp))
        self.ui.pBstruc.clicked.connect(lambda: self.open_window(GrammarAppV2))
        self.ui.pBdaily.clicked.connect(lambda: self.open_window(Flashcard1))
        self.ui.pBcommu.clicked.connect(lambda: self.open_window(Flashcard2))
        self.ui.pBidoms.clicked.connect(lambda: self.open_window(Flashcard3))
        # Cấu hình điểm số và tiến độ
        self.score = 0
        self.percentage = 0
        self.load_progress()
        self.update_ui()
    def open_window(self, window_class):
        """Mở cửa sổ bài tập"""
        self.new_window = window_class(self)
        self.new_window.show()
        self.close()
    def update_score_1(self, total_correct_answer_1, percentage_1):
        self.total_correct_answer_1 = total_correct_answer_1
        self.percentage_1 = percentage_1
        self.total_score()

    def update_score_2(self, total_correct_answer_2, percentage_2):
        self.total_correct_answer_2 = total_correct_answer_2
        self.percentage_2 = percentage_2
        self.total_score()

    def total_score(self):
        """Cộng dồn số câu đúng và cập nhật tiến độ"""
        if not hasattr(self, 'total_correct_answer_1'):
            self.total_correct_answer_1 = 0
        if not hasattr(self, 'total_correct_answer_2'):
            self.total_correct_answer_2 = 0
        if not hasattr(self, 'percentage_1'):
            self.percentage_1 = 0
        if not hasattr(self, 'percentage_2'):
            self.percentage_2 = 0

        # Cộng dồn số câu đúng vào tổng số câu đúng
        self.total_correct_answers += self.total_correct_answer_1 + self.total_correct_answer_2

        if self.total_correct_answers > 0:
            self.score = self.total_correct_answers  # Cập nhật tổng điểm dựa trên số câu đúng
        else:
            self.score = 0

        if self.percentage_1 > 0:
            self.percentage += self.percentage_1

        if self.percentage_2 > 0:
            self.percentage += self.percentage_2

        # Lưu tiến độ mới
        self.save_progress()

        # Cập nhật giao diện
        self.update_ui()

    def save_progress(self):
        """Lưu điểm số, tiến độ và tổng số câu đúng vào file progress.json"""
        progress_data = {
            "username": self.username,
            "score": self.score,
            "percentage": self.percentage,
            "total_correct_answers": self.total_correct_answers  # Lưu tổng số câu đúng
        }

        with open("progress.json", "w") as file:
            json.dump(progress_data, file, indent=4)

    def load_progress(self):
        """Tải điểm số, tiến độ và tổng số câu đúng từ file progress.json"""
        try:
            with open("progress.json", "r") as file:
                progress_data = json.load(file)

            # Chỉ cập nhật nếu username khớp
            if progress_data["username"] == self.username:
                self.score = progress_data["score"]
                self.percentage = progress_data["percentage"]
                self.total_correct_answers = progress_data.get("total_correct_answers",
                                                               0)  # Lấy dữ liệu cũ hoặc mặc định 0

        except (FileNotFoundError, json.JSONDecodeError):
            self.score = 0
            self.percentage = 0
            self.total_correct_answers = 0  # Khởi tạo nếu không có file

        # Cập nhật giao diện
        self.update_ui()

    def update_ui(self):
        """Cập nhật giao diện khi tải tiến độ hoặc khi điểm số thay đổi"""
        self.ui.lblscore.setText(f"Total: {self.score}/115 | Accuracy: {self.percentage:.2f}%")
        self.ui.progressBar.setValue(int(self.percentage))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec())
