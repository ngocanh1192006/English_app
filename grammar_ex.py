import sys
import json
from PyQt6 import QtWidgets, QtGui, QtCore
from grammar import Ui_MainWindow


class GrammarApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, main_window=None):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window  # Lưu tham chiếu đến MainApp
        self.total_correct_answers_1 = 0
        # Kết nối nút 'Back' với hành động quay lại MainApp
        self.pushButton_3.clicked.connect(self.go_back)
        self.load_exercises()
        self.tenseCombo.currentIndexChanged.connect(self.display_exercise)
        self.submitButton.clicked.connect(self.check_answer)
        self.pushButton_2.clicked.connect(self.next_question)
        self.pushButton.clicked.connect(self.prev_question)
        self.selected_tense = None
        self.current_question_index = 0
        self.current_questions = []
        self.correct_answers = 0
        self.answered_questions = set()
        self.centralwidget.setEnabled(True)

        # Set default empty selection for tenseCombo
        self.tenseCombo.setCurrentIndex(-1)

    def go_back(self):
        """Quay lại giao diện chính"""
        if self.main_window:
            self.main_window.show()
        self.close()

    def load_exercises(self):
        """ Load exercises from JSON file. """
        try:
            with open("exercises.json", "r", encoding="utf-8") as file:
                self.data = json.load(file)
                self.tenseCombo.addItems([tense["tense"] for tense in self.data["tenses"]])
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load exercises.json:\n{str(e)}")
            self.data = {"tenses": []}  # Tránh crash nếu không có dữ liệu

    def display_exercise(self):
        """ Display tense details and first question. """
        try:
            self.selected_tense = self.tenseCombo.currentText()
            if not self.selected_tense:
                return

            for tense in self.data.get("tenses", []):
                if tense.get("tense") == self.selected_tense:
                    details_text = (
                        f"📖 Description: {tense.get('description', 'N/A')}\n"
                        f"🛠 Structure: {tense.get('structure', 'N/A')}\n"
                        f"💡 Examples: {', '.join(tense.get('examples', []))}"
                    )
                    self.tenseDetailsLabel.setText(details_text)

                    self.current_questions = tense.get("exercises", [])
                    self.current_question_index = 0
                    self.correct_answers = 0
                    self.answered_questions.clear()
                    self.update_question()
                    break
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def update_question(self):
        """ Update the UI with the current question. """
        if self.current_questions:
            self.current_question = self.current_questions[self.current_question_index]
            self.questionLabel.setText(f" {self.current_question['question']}")
            self.feedbackLabel.setText("")  # Clear previous feedback
            self.load_options()

            # Always show Back and Next button
            self.pushButton.setEnabled(self.current_question_index > 0)
            self.pushButton_2.setEnabled(True)

    def load_options(self):
        """ Load multiple choice options into the UI. """
        if not hasattr(self, "optionsLayout") or self.optionsLayout is None:
            return

        for i in reversed(range(self.optionsLayout.count())):
            item = self.optionsLayout.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        for option in self.current_question.get("options", []):
            radio = QtWidgets.QRadioButton(option)
            self.optionsLayout.addWidget(radio)

    def check_answer(self):
        """ Validate user selection and display feedback. """
        if self.current_question_index not in self.answered_questions:
            answered = False
            for i in range(self.optionsLayout.count()):
                radio = self.optionsLayout.itemAt(i).widget()
                if radio.isChecked():
                    answered = True
                    if radio.text() == self.current_question["correctAnswer"]:
                        self.feedbackLabel.setText(f"✅ Correct! 🎉 {self.current_question['explanation']}")
                        self.correct_answers += 1

                    else:
                        self.feedbackLabel.setText(f"❌ Incorrect! 😞 {self.current_question['explanation']}")
                    self.answered_questions.add(self.current_question_index)
                    break

            # Show warning if no answer selected
            if not answered:
                msg_box = QtWidgets.QMessageBox()
                msg_box.setWindowTitle("Warning")
                msg_box.setText("⚠️ Please select an answer before submitting!")
                msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                msg_box.exec()

    def next_question(self):
        """ Move to the next question or show warning if unanswered. """
        if self.current_question_index not in self.answered_questions:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle("Warning")
            msg_box.setText("⚠️ You must answer the question before proceeding!")
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg_box.exec()
        else:
            if self.current_question_index < len(self.current_questions) - 1:
                self.current_question_index += 1
                self.update_question()
            else:
                self.show_results()

    def prev_question(self):
        """ Move to the previous question. """
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.update_question()

    def show_results(self):
        """ Show final results in a message box. """
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Quiz Results")
        msg_box.setText(f"You answered {self.correct_answers}/{len(self.current_questions)} questions correctly! 🎉")
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg_box.exec()

        total_questions = 115  # Tổng số câu hỏi

        # Cộng dồn điểm của lần làm bài hiện tại vào tổng điểm
        self.total_correct_answers_1 += self.correct_answers

        # Tính phần trăm đúng
        percentage_1 = (self.total_correct_answers_1 / total_questions) * 100

        # Gửi dữ liệu về MainApp
        if self.main_window:
            self.main_window.update_score_1(self.total_correct_answers_1, percentage_1)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GrammarApp()
    window.show()
    sys.exit(app.exec())