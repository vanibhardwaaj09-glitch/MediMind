/**
 * MediMind – Frontend Application Logic
 * ----------------------------------------
 * This file handles:
 *  1. Form validation
 *  2. Sending symptoms to the FastAPI backend
 *  3. Displaying the AI response on the page
 *  4. Loading and error states
 */

// ===== DOM ELEMENT REFERENCES =====
// We grab all elements once at the top for cleaner code below.

const symptomForm = document.getElementById("symptom-form");
const symptomsInput = document.getElementById("symptoms");
const durationInput = document.getElementById("duration");
const severityInput = document.getElementById("severity");
const disclaimerCheck = document.getElementById("disclaimer-check");
const analyzeBtn = document.getElementById("analyze-btn");
const charCount = document.getElementById("char-count");
const formError = document.getElementById("form-error");

// Results panel elements
const resultsPlaceholder = document.getElementById("results-placeholder");
const loadingState = document.getElementById("loading-state");
const resultsContent = document.getElementById("results-content");
const guidanceSections = document.getElementById("guidance-sections");
const emergencyAlert = document.getElementById("emergency-alert");
const resultsDisclaimerText = document.getElementById("results-disclaimer-text");
const analyzeAgainBtn = document.getElementById("analyze-again-btn");


// ===== CHARACTER COUNTER =====
// Updates the "0 / 500" counter as the user types.

symptomsInput.addEventListener("input", () => {
  const length = symptomsInput.value.length;
  charCount.textContent = `${length} / ${CONFIG.MAX_SYMPTOMS_LENGTH}`;
});


// ===== FORM SUBMIT HANDLER =====
// Runs when the user clicks "Analyze Symptoms".

symptomForm.addEventListener("submit", async (event) => {
  // Prevent the browser from reloading the page on submit
  event.preventDefault();

  // Clear any previous error message
  hideError();

  // --- Client-side validation ---
  const symptoms = symptomsInput.value.trim();

  if (!symptoms) {
    showError("Please describe your symptoms before submitting.");
    symptomsInput.focus();
    return;
  }

  if (!disclaimerCheck.checked) {
    showError("Please acknowledge the medical disclaimer to continue.");
    return;
  }

  // --- Prepare the request body (matches backend schema) ---
  const requestBody = {
    symptoms: symptoms,
    duration: durationInput.value.trim() || null,
    severity: severityInput.value || null,
  };

  // --- Show loading state ---
  showLoading();

  try {
    // Send POST request to FastAPI /analyze endpoint
    const apiUrl = `${getApiBaseUrl()}/analyze`;

    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    });

    // Parse the JSON response from the backend
    const data = await response.json();

    if (!response.ok || data.success === false) {
      // Backend returned an error (400, 500, etc.)
      // FastAPI may wrap errors in a "detail" object — handle both formats
      const errorMessage =
        data.error ||
        (data.detail && data.detail.error) ||
        (typeof data.detail === "string" ? data.detail : null) ||
        "Something went wrong. Please try again.";
      throw new Error(errorMessage);
    }

    // Success – display the AI guidance
    displayResults(data);

  } catch (error) {
    // Network error or backend failure
    hideLoading();
    showError(
      error.message ||
      "Unable to connect to the server. Make sure the backend is running on port 8000."
    );
  }
});


// ===== DISPLAY RESULTS =====
// Renders the structured AI response into the results panel.

function displayResults(data) {
  hideLoading();

  const guidance = data.guidance;

  // Build HTML for each guidance section
  guidanceSections.innerHTML = "";

  // Summary section
  if (guidance.summary) {
    guidanceSections.appendChild(createGuidanceCard("Summary", guidance.summary, false));
  }

  // Possible causes (list)
  if (guidance.possible_causes && guidance.possible_causes.length > 0) {
    guidanceSections.appendChild(
      createGuidanceCard("Possible Considerations", guidance.possible_causes, true)
    );
  }

  // Self-care tips (list)
  if (guidance.self_care_tips && guidance.self_care_tips.length > 0) {
    guidanceSections.appendChild(
      createGuidanceCard("General Self-Care Tips", guidance.self_care_tips, true)
    );
  }

  // When to seek care (list)
  if (guidance.when_to_seek_care && guidance.when_to_seek_care.length > 0) {
    guidanceSections.appendChild(
      createGuidanceCard("When to See a Doctor", guidance.when_to_seek_care, true)
    );
  }

  // General advice
  if (guidance.general_advice) {
    guidanceSections.appendChild(
      createGuidanceCard("General Advice", guidance.general_advice, false)
    );
  }

  // Show emergency alert if backend flagged urgent symptoms
  if (data.emergency_detected) {
    emergencyAlert.classList.remove("hidden");
  } else {
    emergencyAlert.classList.add("hidden");
  }

  // Display the disclaimer text returned by the backend
  resultsDisclaimerText.textContent = data.disclaimer;

  // Show the results panel
  resultsContent.classList.remove("hidden");
}


// ===== HELPER: CREATE A GUIDANCE CARD =====
// Creates a styled card for each section of the AI response.

function createGuidanceCard(title, content, isList) {
  const card = document.createElement("div");
  card.className = "guidance-card";

  const heading = document.createElement("h4");
  heading.textContent = title;
  card.appendChild(heading);

  if (isList && Array.isArray(content)) {
    const list = document.createElement("ul");
    content.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      list.appendChild(li);
    });
    card.appendChild(list);
  } else {
    const paragraph = document.createElement("p");
    paragraph.textContent = content;
    card.appendChild(paragraph);
  }

  return card;
}


// ===== UI STATE HELPERS =====

function showLoading() {
  resultsPlaceholder.classList.add("hidden");
  resultsContent.classList.add("hidden");
  loadingState.classList.remove("hidden");
  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing…";
}

function hideLoading() {
  loadingState.classList.add("hidden");
  analyzeBtn.disabled = false;
  analyzeBtn.textContent = "Analyze Symptoms";
}

function showError(message) {
  formError.textContent = message;
  formError.classList.remove("hidden");
}

function hideError() {
  formError.textContent = "";
  formError.classList.add("hidden");
}


// ===== ANALYZE AGAIN BUTTON =====
// Resets the results panel so the user can submit new symptoms.

analyzeAgainBtn.addEventListener("click", () => {
  resultsContent.classList.add("hidden");
  resultsPlaceholder.classList.remove("hidden");
  symptomForm.reset();
  charCount.textContent = `0 / ${CONFIG.MAX_SYMPTOMS_LENGTH}`;
  hideError();
});
