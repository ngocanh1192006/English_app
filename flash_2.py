from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt6 import uic
import sys
from pymongo import MongoClient


class FlashcardContent(QMainWindow):
    def __init__(self, topic_id):
        super().__init__()
        uic.loadUi("flash.ui", self)

        # Kết nối MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["eng_app"]
        collection = db["vocabulary"]

        # Truy vấn chủ đề flashcard theo topic_id
        topic = collection.find_one({"_id": topic_id})

        if topic:
            self.cards = topic["cards"]
        else:
            self.cards = [{"front": "Không có dữ liệu", "back": ""}]

        self.current_index = 0
        self.is_front = True  # Biến trạng thái mặt thẻ
        self.show_card()

        # Gán sự kiện cho nút
        self.pushButton_2.clicked.connect(self.next_card)  # Nút Next
        self.pushButton.clicked.connect(self.prev_card)  # Nút Back
        self.label_2.mousePressEvent = self.flip_card  # Lật thẻ bằng cách click vào thẻ

    def show_card(self):
        """Hiển thị nội dung của thẻ"""
        if self.is_front:
            self.label_2.setText(self.cards[self.current_index]["front"])
        else:
            self.label_2.setText(self.cards[self.current_index]["back"])

    def next_card(self):
        """Chuyển sang thẻ flashcard tiếp theo"""
        self.current_index += 1
        if self.current_index >= len(self.cards):
            self.current_index = 0  # Quay lại đầu danh sách
        self.is_front = True  # Mặc định hiển thị mặt trước khi chuyển thẻ
        self.show_card()

    def prev_card(self):
        """Quay lại thẻ flashcard trước đó"""
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.cards) - 1  # Quay lại cuối danh sách
        self.is_front = True  # Mặc định hiển thị mặt trước khi chuyển thẻ
        self.show_card()

    def flip_card(self, event):
        """Lật flashcard để xem nghĩa"""
        self.is_front = not self.is_front
        self.show_card()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlashcardContent(topic_id=1)  # Chạy thử với topic_id mẫu
    window.show()
    sys.exit(app.exec())