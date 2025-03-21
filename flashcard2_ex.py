import sys
import json
from PyQt6 import QtWidgets, QtGui, QtCore
from flashcard2 import Ui_MainWindow


class FlashcardApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_flashcards()
        self.comboBox.currentIndexChanged.connect(self.load_category)
        self.pushButton.clicked.connect(self.prev_card)
        self.pushButton_2.clicked.connect(self.next_card)
        self.label.mousePressEvent = self.flip_card  # Click vào màn hình để lật thẻ
        self.current_category = None
        self.current_index = 0
        self.cards = []
        self.showing_term = True  # Biến trạng thái để theo dõi mặt hiện tại của thẻ

    def load_flashcards(self):
        """ Load flashcard data from JSON file. """
        try:
            with open("flashcard2.json", "r", encoding="utf-8") as file:
                self.data = json.load(file)
                self.comboBox.clear()
                self.comboBox.addItems([category["name"] for category in self.data])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load flashcard1.json:\n{str(e)}")
            self.data = []

    def load_category(self):
        """ Load flashcards for the selected category. """
        self.current_category = self.comboBox.currentText()
        self.cards = next((c["cards"] for c in self.data if c["name"] == self.current_category), [])
        self.current_index = 0
        self.showing_term = True  # Đặt lại trạng thái khi chuyển danh mục
        self.update_card()

    def update_card(self):
        """ Display the current flashcard (always start with term). """
        if self.cards:
            term = self.cards[self.current_index]["term"]
            self.label.setText(term)
            self.showing_term = True  # Reset về mặt term mỗi khi chuyển card
        else:
            self.label.setText("No cards available")

        self.pushButton.setEnabled(self.current_index > 0)
        self.pushButton_2.setEnabled(self.current_index < len(self.cards) - 1)

    def flip_card(self, event):
        """ Flip between term and definition when clicking on the card. """
        if self.cards:
            if self.showing_term:
                self.label.setText(self.cards[self.current_index]["definition"])
            else:
                self.label.setText(self.cards[self.current_index]["term"])
            self.showing_term = not self.showing_term  # Đảo trạng thái

    def prev_card(self):
        """ Show the previous flashcard. """
        if self.current_index > 0:
            self.current_index -= 1
            self.update_card()

    def next_card(self):
        """ Show the next flashcard. """
        if self.current_index < len(self.cards) - 1:
            self.current_index += 1
            self.update_card()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = FlashcardApp()
    window.show()
    sys.exit(app.exec())