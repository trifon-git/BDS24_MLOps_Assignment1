async function fetchPrediction() {
    const response = await fetch("latest_penguin.json");
    if (response.ok) {
        const penguinData = await response.json();
        const predictionTime = new Date(penguinData.prediction_time).toLocaleString();
        const discoveryTime = new Date(penguinData.datetime).toLocaleString();

        document.getElementById("prediction").textContent =
            `🔥 Mission Success! Penguin Species Identified: ${penguinData.species} 🐧`;

        const dataTable = document.createElement('table');
        dataTable.innerHTML = `
            <tr>
                <th onclick="createPenguinRain()">Penguin Species</th>
                <th onclick="createPenguinRain()">Bill Length (mm)</th>
                <th onclick="createPenguinRain()">Bill Depth (mm)</th>
                <th onclick="createPenguinRain()">Flipper Length (mm)</th>
                <th onclick="createPenguinRain()">Body Mass (g)</th>
                <th onclick="createPenguinRain()">Discovery Time</th>
                <th onclick="createPenguinRain()">Prediction Time</th>
            </tr>
            <tr>
                <td>${penguinData.species}</td>
                <td>${penguinData.bill_length_mm.toFixed(2)}</td>
                <td>${penguinData.bill_depth_mm.toFixed(2)}</td>
                <td>${penguinData.flipper_length_mm.toFixed(2)}</td>
                <td>${penguinData.body_mass_g.toFixed(2)}</td>
                <td>${discoveryTime}</td>
                <td>${predictionTime}</td>
            </tr>
        `;
        document.getElementById("data-table").appendChild(dataTable);
    } else {
        document.getElementById("prediction").textContent = "❌ Mission Failed! Penguins are undercover!";
    }
}

async function fetchPreviousPredictions() {
    const response = await fetch("predictions.json");
    if (response.ok) {
        const predictionsData = await response.json();
        const sortedPredictions = predictionsData.sort((a, b) =>
            new Date(b.prediction_time) - new Date(a.prediction_time)
        );

        let previousPredictionsTable = `<table>
            <tr>
                <th>Species</th>
                <th>Bill Length (mm)</th>
                <th>Bill Depth (mm)</th>
                <th>Flipper Length (mm)</th>
                <th>Body Mass (g)</th>
                <th>Discovery Time</th>
                <th>Prediction Time</th>
            </tr>`;

        sortedPredictions.forEach(prediction => {
            previousPredictionsTable += `
                <tr>
                    <td>${prediction.species}</td>
                    <td>${prediction.bill_length_mm.toFixed(2)}</td>
                    <td>${prediction.bill_depth_mm.toFixed(2)}</td>
                    <td>${prediction.flipper_length_mm.toFixed(2)}</td>
                    <td>${prediction.body_mass_g.toFixed(2)}</td>
                    <td>${new Date(prediction.datetime).toLocaleString()}</td>
                    <td>${new Date(prediction.prediction_time).toLocaleString()}</td>
                </tr>
            `;
        });

        previousPredictionsTable += '</table>';
        document.getElementById("previous-predictions").innerHTML = previousPredictionsTable;
    }
}

fetchPrediction();
fetchPreviousPredictions();

function createPenguinRain() {
    for (let i = 0; i < 1000; i++) {
        const penguin = document.createElement("div");
        penguin.classList.add("penguin");
        penguin.textContent = "🐧";
        penguin.style.left = Math.random() * 100 + "vw";
        penguin.style.animationDuration = Math.random() * 2 + 2 + "s";
        penguin.style.animationDelay = Math.random() * 3 + "s";
        document.body.appendChild(penguin);

        setTimeout(() => penguin.remove(), 5000);
    }
}

function triggerEasterEgg() {
    alert("🐧 COMMANDO PENGUIN ATTACK ACTIVATED! 💥");
}
