// AI AdMonitor SaaS Interactive Frontend Script
document.addEventListener("DOMContentLoaded", function () {
  console.log("AI AdMonitor dashboard initialized.");

  // 1. Initialize Real-Time Auto-Refresh Poller
  initRealtimePoller();

  // 2. Initialize What-If Budget Prediction Slider
  initWhatIfSimulator();
});

/**
 * Periodically polls the server for real-time metric updates
 * and smoothly updates KPI cards.
 */
function initRealtimePoller() {
  const realtimePill = document.getElementById("realtime-status-pill");
  if (!realtimePill) return;

  setInterval(function () {
    fetch("/api/realtime-metrics")
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "success") {
          // Update live DOM metrics
          updateMetricElement("kpi-clicks-val", data.clicks.toLocaleString());
          updateMetricElement("kpi-impressions-val", data.impressions.toLocaleString());
          updateMetricElement("kpi-spend-val", "$" + data.cost.toLocaleString(undefined, {minimumFractionDigits: 2}));
          updateMetricElement("kpi-ctr-val", data.ctr + "%");

          // Pulse animation trigger
          realtimePill.classList.add("pulse-glow");
          setTimeout(() => realtimePill.classList.remove("pulse-glow"), 800);
        }
      })
      .catch((err) => console.log("Realtime polling update error:", err));
  }, 5000);
}

function updateMetricElement(id, textContent) {
  const el = document.getElementById(id);
  if (el) {
    el.textContent = textContent;
  }
}

/**
 * Handles interactive What-If budget prediction slider logic.
 */
function initWhatIfSimulator() {
  const slider = document.getElementById("budget-slider");
  const campaignIdInput = document.getElementById("campaign-id-input");
  
  if (!slider || !campaignIdInput) return;

  const campaignId = campaignIdInput.value;
  const sliderValDisplay = document.getElementById("budget-slider-val");

  slider.addEventListener("input", function (e) {
    const val = e.target.value;
    sliderValDisplay.textContent = (val > 0 ? "+" + val : val) + "%";

    // Debounced AJAX prediction request
    debouncePredictionRequest(campaignId, val);
  });
}

let debounceTimer = null;
function debouncePredictionRequest(campaignId, adjustmentPct) {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(function () {
    fetch(`/campaigns/${campaignId}/simulate-prediction`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ budget_adjustment_pct: adjustmentPct })
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "success") {
          const pred = data.prediction;
          document.getElementById("sim-budget").textContent = "$" + pred.simulated_budget.toLocaleString();
          document.getElementById("sim-ctr").textContent = pred.predicted_ctr + "%";
          document.getElementById("sim-roi").textContent = pred.predicted_roi + "%";
          document.getElementById("sim-conv").textContent = pred.predicted_conversions;
          document.getElementById("sim-cpc").textContent = "$" + pred.predicted_cpc;
        }
      })
      .catch((err) => console.error("Prediction simulation error:", err));
  }, 300);
}
