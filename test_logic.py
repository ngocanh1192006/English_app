from tense_logic import TenseLogic

def main():
    # Initialize the logic with the JSON file
    logic = TenseLogic('exercises.json')
    if not logic.exercises_data:
        return

    # Display available tenses
    tense_names = logic.get_tense_names()
    print("Available Tenses:")
    for i, name in enumerate(tense_names, 1):
        print(f"{i}. {name}")

    # Simulate selecting a tense
    try:
        tense_choice = int(input("\nSelect a tense (enter the number): ")) - 1
        tense_name = tense_names[tense_choice]
    except (ValueError, IndexError):
        print("Error: Invalid selection!")
        return

    # Display tense details
    tense_details = logic.set_current_tense(tense_name)
    if not tense_details:
        print(f"Error: Tense '{tense_name}' not found!")
        return
    print("\nTense Details:")
    for key, value in tense_details.items():
        print(f"{key.capitalize()}: {value}")

    # Display the first exercise
    exercise = logic.get_exercise(1)
    if not exercise:
        print("Error: Exercise not found!")
        return
    print("\nExercise:")
    print(f"Question: {exercise['question']}")
    print("Options:")
    for i, option in enumerate(exercise['options'], 1):
        print(f"{i}. {option}")

    # Simulate selecting an answer
    try:
        answer_choice = int(input("\nSelect an answer (enter the number): ")) - 1
        user_answer = exercise['options'][answer_choice]
    except (ValueError, IndexError):
        print("Error: Invalid selection!")
        return

    # Check the answer
    feedback = logic.check_answer(user_answer)
    if feedback['is_correct']:
        print("Correct! 🎉")
    else:
        print("Incorrect. 😞")
    print(f"Correct Answer: {feedback['correct_answer']}")
    print(f"Explanation: {feedback['explanation']}")

if __name__ == "__main__":
    main()