import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QRadioButton, QButtonGroup
from PyQt6.uic import loadUi
from tense_logic import TenseLogic

class TenseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the .ui file
        loadUi('tense_app.ui', self)

        # Initialize logic
        self.logic = TenseLogic('exercises.json')
        if not self.logic.exercises_data:
            sys.exit(1)

        # Populate tense combo box
        self.tenseCombo.addItems(self.logic.get_tense_names())

        # Connect signals
        self.tenseCombo.currentTextChanged.connect(self.on_tense_selected)
        self.submitButton.clicked.connect(self.on_submit)

        # Initialize options button group
        self.options_group = QButtonGroup(self.optionsWidget)

        # Initialize with the first tense
        if self.tenseCombo.count() > 0:
            self.tenseCombo.setCurrentIndex(0)
            self.on_tense_selected(self.tenseCombo.currentText())

    def on_tense_selected(self, tense_name):
        """Handle tense selection."""
        tense_details = self.logic.set_current_tense(tense_name)
        if not tense_details:
            self.tenseDetailsLabel.setText(f"Error: Tense '{tense_name}' not found!")
            return

        # Display tense details
        details_text = (
            f"Tense: {tense_details['name']}\n"
            f"Description: {tense_details['description']}\n"
            f"Structure: {tense_details['structure']}\n"
            f"Examples: {tense_details['examples']}"
        )
        self.tenseDetailsLabel.setText(details_text)

        # Display the first exercise
        exercise = self.logic.get_exercise(1)
        if not exercise:
            self.questionLabel.setText("Error: Exercise not found!")
            return

        self.questionLabel.setText(f"Question: {exercise['question']}")

        # Clear previous options
        for button in self.options_group.buttons():
            self.options_group.removeButton(button)
            button.deleteLater()

        # Add new options as radio buttons
        for i, option in enumerate(exercise['options']):
            radio_button = QRadioButton(option, self.optionsWidget)
            self.options_group.addButton(radio_button, i)
            self.optionsWidget.layout().addWidget(radio_button)

        # Clear feedback
        self.feedbackLabel.setText("")

    def on_submit(self):
        """Handle answer submission."""
        selected_button = self.options_group.checkedButton()
        if not selected_button:
            self.feedbackLabel.setText("Please select an answer!")
            return

        user_answer = selected_button.text()
        feedback = self.logic.check_answer(user_answer)

        if feedback['is_correct']:
            self.feedbackLabel.setText(f"Correct! 🎉\nExplanation: {feedback['explanation']}")
            self.feedbackLabel.setStyleSheet("color: green;")
        else:
            self.feedbackLabel.setText(
                f"Incorrect. 😞\nCorrect Answer: {feedback['correct_answer']}\nExplanation: {feedback['explanation']}"
            )
            self.feedbackLabel.setStyleSheet("color: red;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TenseApp()
    window.show()
    sys.exit(app.exec_())