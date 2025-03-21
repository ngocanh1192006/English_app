import sys
import json
from PyQt6 import QtWidgets, QtGui, QtCore
from grammar2 import Ui_MainWindow


class GrammarAppV2(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_exercises()
        self.tenseCombo.currentIndexChanged.connect(self.display_exercise)
        self.submitButton.clicked.connect(self.check_answer)
        self.pushButton_2.clicked.connect(self.next_question)
        self.pushButton.clicked.connect(self.prev_question)
        self.selected_structure = None
        self.current_question_index = 0
        self.current_questions = []
        self.correct_answers = 0
        self.answered_questions = set()
        self.centralwidget.setEnabled(True)

        # Set default empty selection for tenseCombo
        self.tenseCombo.setCurrentIndex(-1)

    def load_exercises(self):
        """ Load exercises from JSON file. """
        try:
            with open("exercises_2.json", "r", encoding="utf-8") as file:
                self.data = json.load(file)
                if "structures" in self.data:
                    self.tenseCombo.clear()
                    self.tenseCombo.addItems([item.get("structure") for item in self.data["structures"]])
                else:
                    raise KeyError("Missing 'structures' key in JSON file")
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load exercises_2.json:\n{str(e)}")
            self.data = {"structures": []}  # Avoid crash if data is missing

    def display_exercise(self):
        """ Display grammar structure details and first question. """
        try:
            self.selected_structure = self.tenseCombo.currentText()
            if not self.selected_structure or "structures" not in self.data:
                return

            for item in self.data["structures"]:
                if item.get("structure") == self.selected_structure:
                    details_text = f"📖 Structure: {item.get('structure', 'N/A')}\n"
                    details_text += f"📊 Level: {item.get('level', 'N/A')}\n"
                    if "description" in item:
                        details_text += f"📝 Description: {item['description']}\n"
                    if "forms" in item:
                        details_text += f"📌 Forms: {'; '.join(item['forms'])}\n"
                    if "examples" in item:
                        details_text += f"💡 Examples: {'; '.join(item['examples'])}\n"

                    self.tenseDetailsLabel.setText(details_text)

                    self.current_questions = item.get("exercises", [])
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

            self.pushButton.setEnabled(self.current_question_index > 0)
            self.pushButton_2.setEnabled(True)

            if self.current_question_index == len(self.current_questions) - 1:
                self.pushButton_2.setToolTip("Finish")
            else:
                self.pushButton_2.setToolTip("Next")

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




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GrammarAppV2()
    window.show()
    sys.exit(app.exec())
