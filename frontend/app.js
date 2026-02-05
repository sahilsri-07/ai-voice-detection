const form = document.getElementById("upload-form");
const fileInput = document.getElementById("audio-file");
const langSelect = document.getElementById("language");
const statusEl = document.getElementById("status");
const resultCard = document.getElementById("result-card");
const resultLabel = document.getElementById("result-label");
const resultConfidence = document.getElementById("result-confidence");
const resultLanguage = document.getElementById("result-language");
const resultDetail = document.getElementById("result-detail");
const submitBtn = document.getElementById("submit-btn");
const apiKeyInput = document.getElementById("api-key");

// Adjust this if you deploy to a public URL
const API_BASE_URL = "http://127.0.0.1:8000";

function setStatus(message, type = "info") {
  const colors = {
    info: "text-slate-300",
    error: "text-red-400",
    success: "text-emerald-400",
  };
  statusEl.className = `text-sm mt-2 ${colors[type] || colors.info}`;
  statusEl.textContent = message;
}

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  submitBtn.textContent = isLoading ? "Analyzing..." : "Analyze Voice Sample";
}

function showResult(data) {
  resultCard.classList.remove("hidden");
  resultLabel.textContent =
    data.result === "AI_GENERATED" ? "AI-generated Voice" : "Human Voice";

  resultLabel.className =
    "text-xl font-semibold " +
    (data.result === "AI_GENERATED"
      ? "text-pink-400"
      : "text-sky-400");

  resultConfidence.textContent = `Confidence: ${(data.confidence * 100).toFixed(
    1
  )}%`;
  resultLanguage.textContent = `Detected language (from request): ${data.language}`;
  resultDetail.textContent = data.detail || "";
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result;
      const base64 = result.split(",")[1]; // strip "data:audio/mp3;base64,"
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  resultCard.classList.add("hidden");

  const file = fileInput.files[0];
  const language = langSelect.value;
  const apiKey = apiKeyInput.value.trim();

  if (!file) {
    setStatus("Please select an MP3 file.", "error");
    return;
  }

  if (!apiKey) {
    setStatus("Please enter your API key.", "error");
    return;
  }

  try {
    setLoading(true);
    setStatus("Encoding audio and contacting API...", "info");

    const base64 = await fileToBase64(file);

    const res = await fetch(`${API_BASE_URL}/api/detect`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
      },
      body: JSON.stringify({
        audio_base64: base64,
        language: language,
      }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `API error: ${res.status}`);
    }

    const data = await res.json();
    showResult(data);
    setStatus("Analysis completed successfully.", "success");
  } catch (err) {
    console.error(err);
    setStatus(err.message || "Something went wrong.", "error");
  } finally {
    setLoading(false);
  }
});