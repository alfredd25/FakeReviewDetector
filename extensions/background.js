chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "analyzeReview") {
    fetch("https://fake-review-api.onrender.com/predict", {
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

