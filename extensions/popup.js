document.getElementById("analyzeBtn").addEventListener("click", () => {
  const review = document.getElementById("reviewInput").value;
  if (!review.trim()) return;

  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ review: review })
  })
    .then(response => response.json())
    .then(data => {
      const result = document.getElementById("result");
      if (data.label && data.confidence !== undefined) {
        result.innerText = `Prediction: ${data.label.toUpperCase()} (${(data.confidence * 100).toFixed(1)}%)`;
      } else {
        result.innerText = "Error: Unable to analyze the review.";
      }
    })
    .catch(() => {
      document.getElementById("result").innerText = "API Error. Make sure the server is running.";
    });
});

