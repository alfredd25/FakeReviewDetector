const input = document.getElementById("reviewInput");
const button = document.getElementById("analyzeBtn");
const resultBox = document.getElementById("result");

button.addEventListener("click", () => {
  const review = input.value.trim();
  if (!review) return;

  resultBox.innerText = "Analyzing...";
  resultBox.style.color = "#333";

  fetch("https://fake-review-api.onrender.com/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ review: review })
  })
    .then(response => response.json())
    .then(data => {
      if (data.label && data.confidence !== undefined) {
        const labelText = data.label.toUpperCase();
        const confidencePercent = (data.confidence * 100).toFixed(1);
        const color = data.label === "fake" ? "red" : "green";
        resultBox.innerText = `Prediction: ${labelText} (${confidencePercent}%)`;
        resultBox.style.color = color;
      } else {
        resultBox.innerText = "Unexpected response.";
        resultBox.style.color = "orange";
      }
    })
    .catch(() => {
      resultBox.innerText = "API error. Make sure the server is running.";
      resultBox.style.color = "red";
    });
});
