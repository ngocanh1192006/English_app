// Load JSON data (for testing, we'll simulate fetching it)
let exercisesData = {};

// Fetch the JSON file (in a real app, this would be an actual fetch request)
fetch('exercises.json')
    .then(response => response.json())
    .then(data => {
        exercisesData = data;
        initializeApp();
    })
    .catch(error => console.error('Error loading JSON:', error));

// Initialize the app
function initializeApp() {
    const tenseList = document.getElementById('tense-options');
    exercisesData.tenses.forEach(tense => {
        const li = document.createElement('li');
        const button = document.createElement('button');
        button.textContent = tense.tense;
        button.addEventListener('click', () => displayTense(tense.tense));
        li.appendChild(button);
        tenseList.appendChild(li);
    });
}

// Display tense details and exercises
function displayTense(tenseName) {
    const tense = exercisesData.tenses.find(t => t.tense === tenseName);
    if (!tense) {
        console.error('Tense not found!');
        return;
    }

    // Show tense details
    document.getElementById('tense-list').style.display = 'none';
    document.getElementById('exercise-section').style.display = 'block';
    document.getElementById('tense-title').textContent = tense.tense;
    document.getElementById('tense-description').textContent = `Description: ${tense.description}`;
    document.getElementById('tense-structure').textContent = `Structure: ${tense.structure}`;
    document.getElementById('tense-examples').textContent = `Examples: ${tense.examples.join(' ')}`;

    // Display the first exercise (you can expand this to show multiple exercises)
    displayExercise(tenseName, tense.exercises[0].id);
}

// Display an exercise
function displayExercise(tenseName, exerciseId) {
    const tense = exercisesData.tenses.find(t => t.tense === tenseName);
    const exercise = tense.exercises.find(ex => ex.id === exerciseId);
    if (!exercise) {
        console.error('Exercise not found!');
        return;
    }

    // Show question
    document.getElementById('question-text').textContent = exercise.question;

    // Show options as radio buttons
    const optionsDiv = document.getElementById('options');
    optionsDiv.innerHTML = '';
    exercise.options.forEach(option => {
        const label = document.createElement('label');
        const input = document.createElement('input');
        input.type = 'radio';
        input.name = 'answer';
        input.value = option;
        label.appendChild(input);
        label.appendChild(document.createTextNode(` ${option}`));
        optionsDiv.appendChild(label);
        optionsDiv.appendChild(document.createElement('br'));
    });

    // Handle form submission
    const form = document.getElementById('answer-form');
    form.onsubmit = (e) => {
        e.preventDefault();
        const selectedOption = form.querySelector('input[name="answer"]:checked');
        if (selectedOption) {
            checkAnswer(tenseName, exerciseId, selectedOption.value);
        } else {
            alert('Please select an answer!');
        }
    };
}

// Check user answer
function checkAnswer(tenseName, exerciseId, userAnswer) {
    const tense = exercisesData.tenses.find(t => t.tense === tenseName);
    const exercise = tense.exercises.find(ex => ex.id === exerciseId);
    const feedback = document.getElementById('feedback');

    if (userAnswer === exercise.correctAnswer) {
        feedback.textContent = `Correct! 🎉 Explanation: ${exercise.explanation}`;
        feedback.className = 'correct';
    } else {
        feedback.textContent = `Incorrect. 😞 Correct Answer: ${exercise.correctAnswer}. Explanation: ${exercise.explanation}`;
        feedback.className = 'incorrect';
    }
    feedback.style.display = 'block';
}