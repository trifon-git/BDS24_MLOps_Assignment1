async function fetchPrediction() {
    try {
        const response = await fetch('latest_penguin.json');
        const data = await response.json();
        displayPrediction(data);
        displayMetrics(data.penguin_data);
        displayProbabilities(data.probabilities);
        displayFeatureImportance(data);
    } catch (error) {
        console.error("Error fetching data:", error);
        document.getElementById("prediction").innerText = "Error loading prediction.";
    }
}

function displayPrediction(data) {
    const predictionBox = document.getElementById("prediction");
    predictionBox.textContent = `${data.predicted_species} Penguin Found!`;
    predictionBox.style.backgroundColor = data.predicted_species === "Adelie" ? "#a24124" : "#e37e44";

    const timestampEl = document.getElementById("timestamp");
    timestampEl.textContent = `Last updated: ${data.timestamp}`;
}

function displayMetrics(metrics) {
    const metricsContainer = document.getElementById("metrics");
    metricsContainer.innerHTML = '';

    for (const [key, value] of Object.entries(metrics)) {
        const metricDiv = document.createElement("div");
        metricDiv.classList.add("metric");
        metricDiv.innerHTML = `<strong>${formatLabel(key)}:</strong> ${value.toFixed(2)}`;
        metricsContainer.appendChild(metricDiv);
    }
}

function displayProbabilities(probabilities) {
    const barsContainer = document.getElementById("probability-bars");
    barsContainer.innerHTML = '';

    for (const [species, probability] of Object.entries(probabilities)) {
        const barWrapper = document.createElement("div");
        barWrapper.classList.add("probability-bar");

        const bar = document.createElement("div");
        bar.classList.add("bar", "animated-bar");
        bar.style.width = `${(probability * 100).toFixed(2)}%`;
        bar.textContent = `${species}: ${(probability * 100).toFixed(2)}%`;

        barWrapper.appendChild(bar);
        barsContainer.appendChild(barWrapper);
    }
}

function displayFeatureImportance(data) {
    const importanceContainer = document.getElementById("feature-importance");
    importanceContainer.innerHTML = '';

    for (const [feature, importance] of Object.entries(data.feature_importance)) {
        const featureDiv = document.createElement("div");
        featureDiv.classList.add("feature-bar");
        featureDiv.innerHTML = `<strong>${formatLabel(feature)}:</strong> ${Math.round(importance * 100)}%`;
        importanceContainer.appendChild(featureDiv);
    }
}

function formatLabel(label) {
    return label.replace(/_/g, " ").replace(/\b\w/g, char => char.toUpperCase());
}

fetchPrediction();
