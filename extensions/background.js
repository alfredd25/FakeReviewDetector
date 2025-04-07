chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "analyzeReview") {
    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ review: request.review })
    })
      .then(response => response.json())
      .then(data => {
        sendResponse({ label: data.label, confidence: data.confidence });
      })
      .catch(error => {
        sendResponse({ error: "API error" });
      });
    return true;
  }
});

