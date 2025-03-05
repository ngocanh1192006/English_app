import json

# Load JSON data
def load_exercises(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Could not find file '{file_path}'")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{file_path}'")
        return None

# Display tense details and exercises
def display_tense(exercises_data, tense_name):
    tense = next((t for t in exercises_data['tenses'] if t['tense'] == tense_name), None)
    if not tense:
        print(f"Error: Tense '{tense_name}' not found!")
        return

    print(f"\nTense: {tense['tense']}")
    print(f"Description: {tense['description']}")
    print(f"Structure: {tense['structure']}")
    print(f"Examples: {' '.join(tense['examples'])}")
    return tense

# Display an exercise
def display_exercise(tense, exercise_id):
    exercise = next((ex for ex in tense['exercises'] if ex['id'] == exercise_id), None)
    if not exercise:
        print(f"Error: Exercise ID '{exercise_id}' not found!")
        return None

    print("\nQuestion:", exercise['question'])
    print("Options:")
    for i, option in enumerate(exercise['options'], 1):
        print(f"{i}. {option}")
    return exercise

# Check user answer
def check_answer(exercise, user_answer):
    correct_answer = exercise['correctAnswer']
    if user_answer == correct_answer:
        print("Correct! 🎉")
        print(f"Explanation: {exercise['explanation']}")
    else:
        print("Incorrect. 😞")
        print(f"Correct Answer: {correct_answer}")
        print(f"Explanation: {exercise['explanation']}")

# Main function to test the logic
def main():
    # Load exercises
    exercises_data = load_exercises('exercises.json')
    if not exercises_data:
        return

    # Display list of tenses
    print("Available Tenses:")
    for i, tense in enumerate(exercises_data['tenses'], 1):
        print(f"{i}. {tense['tense']}")

    # Ask user to select a tense
    try:
        tense_choice = int(input("\nSelect a tense (enter the number): ")) - 1
        tense_name = exercises_data['tenses'][tense_choice]['tense']
    except (ValueError, IndexError):
        print("Error: Invalid selection!")
        return

    # Display tense details
    tense = display_tense(exercises_data, tense_name)
    if not tense:
        return

    # Display the first exercise (you can expand this to handle multiple exercises)
    exercise = display_exercise(tense, 1)
    if not exercise:
        return

    # Get user answer
    try:
        answer_choice = int(input("\nSelect an answer (enter the number): ")) - 1
        user_answer = exercise['options'][answer_choice]
    except (ValueError, IndexError):
        print("Error: Invalid selection!")
        return

    # Check answer
    check_answer(exercise, user_answer)

if __name__ == "__main__":
    main()