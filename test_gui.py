import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QComboBox, QLabel, QRadioButton, QPushButton, QButtonGroup
from tense_logic import TenseLogic

class TenseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("English Tenses App (Test)")
        self.setGeometry(100, 100, 600, 400)

        # Initialize logic
        self.logic = TenseLogic('exercises.json')
        if not self.logic.exercises_data:
            sys.exit(1)

        # Set up the main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Tense selection
        self.tense_combo = QComboBox()
        self.tense_combo.addItems(self.logic.get_tense_names())
        self.tense_combo.currentTextChanged.connect(self.on_tense_selected)
        self.layout.addWidget(QLabel("Select a Tense:"))
        self.layout.addWidget(self.tense_combo)

        # Tense details
        self.tense_details_label = QLabel()
        self.layout.addWidget(self.tense_details_label)

        # Exercise display
        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        # Options (radio buttons)
        self.options_widget = QWidget()
        self.options_layout = QVBoxLayout(self.options_widget)
        self.options_group = QButtonGroup(self.options_widget)
        self.layout.addWidget(self.options_widget)

        # Submit button
        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.clicked.connect(self.on_submit)
        self.layout.addWidget(self.submit_button)

        # Feedback
        self.feedback_label = QLabel()
        self.layout.addWidget(self.feedback_label)

        # Initialize with the first tense
        if self.tense_combo.count() > 0:
            self.tense_combo.setCurrentIndex(0)
            self.on_tense_selected(self.tense_combo.currentText())

    def on_tense_selected(self, tense_name):
        """Handle tense selection."""
        tense_details = self.logic.set_current_tense(tense_name)
        if not tense_details:
            self.tense_details_label.setText(f"Error: Tense '{tense_name}' not found!")
            return

        # Display tense details
        details_text = (
            f"Tense: {tense_details['name']}\n"
            f"Description: {tense_details['description']}\n"
            f"Structure: {tense_details['structure']}\n"
            f"Examples: {tense_details['examples']}"
        )
        self.tense_details_label.setText(details_text)

        # Display the first exercise
        exercise = self.logic.get_exercise(1)
        if not exercise:
            self.question_label.setText("Error: Exercise not found!")
            return

        self.question_label.setText(f"Question: {exercise['question']}")

        # Clear previous options
        for button in self.options_group.buttons():
            self.options_group.removeButton(button)
            button.deleteLater()
        self.options_layout.update()

        # Add new options as radio buttons
        for i, option in enumerate(exercise['options']):
            radio_button = QRadioButton(option)
            self.options_group.addButton(radio_button, i)
            self.options_layout.addWidget(radio_button)

        # Clear feedback
        self.feedback_label.setText("")

    def on_submit(self):
        """Handle answer submission."""
        selected_button = self.options_group.checkedButton()
        if not selected_button:
            self.feedback_label.setText("Please select an answer!")
            return

        user_answer = selected_button.text()
        feedback = self.logic.check_answer(user_answer)

        if feedback['is_correct']:
            self.feedback_label.setText(f"Correct! 🎉\nExplanation: {feedback['explanation']}")
            self.feedback_label.setStyleSheet("color: green;")
        else:
            self.feedback_label.setText(
                f"Incorrect. 😞\nCorrect Answer: {feedback['correct_answer']}\nExplanation: {feedback['explanation']}"
            )
            self.feedback_label.setStyleSheet("color: red;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TenseApp()
    window.show()
    sys.exit(app.exec_())