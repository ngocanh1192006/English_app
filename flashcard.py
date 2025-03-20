import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from database import get_flashcards  # Import database

# Import file giao diện từ Qt Designer (nếu file tên 4.ui -> phải dùng pyuic6 để chuyển thành 4.py)
from ui_4 import Ui_MainWindow

class FlashcardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Lấy dữ liệu từ MongoDB
        self.flashcards = get_flashcards()
        self.current_index = 0  # Chỉ mục của flashcard hiện tại
        self.show_flashcard()  # Hiển thị flashcard đầu tiên

        # Kết nối các nút với hàm xử lý
        self.ui.pushButton.clicked.connect(self.previous_card)  # Nút Back
        self.ui.pushButton_2.clicked.connect(self.next_card)  # Nút Next
        self.ui.pushButton_3.clicked.connect(self.flip_card)  # Nút Flip (nếu có)

    def show_flashcard(self):
        """Hiển thị nội dung flashcard hiện tại"""
        if self.flashcards:
            flashcard = self.flashcards[self.current_index]
            self.ui.label.setText(flashcard["term"])  # Mặt trước
            self.ui.label_2.setText("")  # Ẩn mặt sau khi load

    def next_card(self):
        """Chuyển sang flashcard tiếp theo"""
        if self.flashcards:
            self.current_index = (self.current_index + 1) % len(self.flashcards)
            self.show_flashcard()

    def previous_card(self):
        """Quay lại flashcard trước"""
        if self.flashcards:
            self.current_index = (self.current_index - 1) % len(self.flashcards)
            self.show_flashcard()

    def flip_card(self):
        """Lật flashcard"""
        if self.flashcards:
            flashcard = self.flashcards[self.current_index]
            current_text = self.ui.label_2.text()
            if current_text:  # Nếu mặt sau đang hiển thị, ẩn đi
                self.ui.label_2.setText("")
            else:
                self.ui.label_2.setText(flashcard["definition"])  # Hiển thị mặt sau

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlashcardApp()
    window.show()
    sys.exit(app.exec())
