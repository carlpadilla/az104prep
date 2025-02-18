let questionIndex = 0;

function loadQuestion() {
  fetch(`/question/${questionIndex}`)
    .then(response => response.json())
    .then(data => {
      if (data.question) {
        document.getElementById("question-box").innerText = data.question;
        // Clear previous feedback and input value
        document.getElementById("feedback").innerText = "";
        document.getElementById("answer-input").value = "";
      } else {
        document.getElementById("question-box").innerText = "Quiz completed!";
        document.getElementById("answer-input").style.display = 'none';
        document.getElementById("submit-btn").style.display = 'none';
      }
    })
    .catch(error => {
      console.error("Error loading question:", error);
      document.getElementById("question-box").innerText = "Error loading question.";
    });
}

function submitAnswer() {
  const userAnswer = document.getElementById("answer-input").value;
  fetch("/check_answer", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ question_index: questionIndex, answer: userAnswer })
  })
  .then(response => response.json())
  .then(data => {
    if (data.correct) {
      document.getElementById("feedback").innerText = "Correct! Moving to the next question...";
      questionIndex++;
      setTimeout(loadQuestion, 1000);
    } else {
      document.getElementById("feedback").innerText = "Incorrect! Try again.";
    }
  })
  .catch(error => {
    console.error("Error checking answer:", error);
    document.getElementById("feedback").innerText = "Error checking answer.";
  });
}

window.onload = loadQuestion;
