import json

class TenseLogic:
    def __init__(self, json_file_path):
        self.exercises_data = self.load_exercises(json_file_path)
        self.current_tense = None
        self.current_exercise = None

    def load_exercises(self, file_path):
        """Load exercises from a JSON file."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: Could not find file '{file_path}'")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in '{file_path}'")
            return None

    def get_tense_names(self):
        """Return a list of tense names."""
        if not self.exercises_data:
            return []
        return [tense['tense'] for tense in self.exercises_data['tenses']]

    def set_current_tense(self, tense_name):
        """Set the current tense and return its details."""
        self.current_tense = next((t for t in self.exercises_data['tenses'] if t['tense'] == tense_name), None)
        if not self.current_tense:
            return None
        return {
            'name': self.current_tense['tense'],
            'description': self.current_tense['description'],
            'structure': self.current_tense['structure'],
            'examples': ' '.join(self.current_tense['examples'])
        }

    def get_exercise(self, exercise_id):
        """Get an exercise for the current tense."""
        if not self.current_tense:
            return None
        self.current_exercise = next((ex for ex in self.current_tense['exercises'] if ex['id'] == exercise_id), None)
        if not self.current_exercise:
            return None
        return {
            'question': self.current_exercise['question'],
            'options': self.current_exercise['options'],
            'correct_answer': self.current_exercise['correctAnswer'],
            'explanation': self.current_exercise['explanation']
        }

    def check_answer(self, user_answer):
        """Check if the user's answer is correct and return feedback."""
        if not self.current_exercise:
            return None
        correct_answer = self.current_exercise['correctAnswer']
        is_correct = user_answer == correct_answer
        return {
            'is_correct': is_correct,
            'correct_answer': correct_answer,
            'explanation': self.current_exercise['explanation']
        }