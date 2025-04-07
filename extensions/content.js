function analyzeAndHighlight(reviewElement) {
  const reviewText = reviewElement.innerText;
  chrome.runtime.sendMessage(
    { type: "analyzeReview", review: reviewText },
    response => {
      if (response && response.label) {
        if (response.label === "fake") {
          reviewElement.style.backgroundColor = "rgba(255, 0, 0, 0.2)";
        } else if (response.label === "real") {
          reviewElement.style.backgroundColor = "rgba(0, 255, 0, 0.2)";
        }
        reviewElement.style.borderRadius = "6px";
        reviewElement.style.padding = "4px";
      }
    }
  );
}

function scanAndHighlightReviews() {
  const reviews = document.querySelectorAll('div._T.FKffI.bmUTE');
  reviews.forEach(review => {
    if (!review.dataset.analyzed) {
      analyzeAndHighlight(review);
      review.dataset.analyzed = "true";
    }
  });
}

const observer = new MutationObserver(() => {
  scanAndHighlightReviews();
});

observer.observe(document.body, { childList: true, subtree: true });

scanAndHighlightReviews();
