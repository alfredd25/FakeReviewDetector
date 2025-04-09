function getReviewElements() {
  const host = window.location.hostname;

  if (host.includes("tripadvisor.com")) {
    return document.querySelectorAll("div._T.FKffI.bmUTE");
  }

  if (host.includes("amazon.in")) {
    return document.querySelectorAll("span[data-hook='review-body']");
  }

  return [];
}

function highlightReview(element, label, confidence) {
  if (label === "fake") {
    element.style.backgroundColor = "rgba(255, 0, 0, 0.2)";
  } else if (label === "real" && confidence >= 0.7) {
    element.style.backgroundColor = "rgba(0, 255, 0, 0.2)";
  } else if (label === "real" && confidence < 0.7) {
    element.style.backgroundColor = "rgba(255, 255, 0, 0.2)";
  }

  element.style.borderRadius = "6px";
  element.style.padding = "4px";
}

function analyzeReviewElement(element) {
  const text = element.innerText.trim();
  if (!text || element.dataset.analyzed) return;

  element.dataset.analyzed = "true";

  chrome.runtime.sendMessage(
    { type: "analyzeReview", review: text },
    response => {
      if (response && response.label && response.confidence !== undefined) {
        highlightReview(element, response.label, response.confidence);
      }
    }
  );
}

function scanPage() {
  const elements = getReviewElements();
  elements.forEach(analyzeReviewElement);
}

const observer = new MutationObserver(() => {
  scanPage();
});

observer.observe(document.body, { childList: true, subtree: true });

scanPage();
