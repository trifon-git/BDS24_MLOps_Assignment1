async function fetchPrediction() {
    try {
        const response = await fetch("latest_penguin.json");
        if (response.ok) {
            const penguinData = await response.json();
            const predictionTime = new Date(penguinData.prediction_time).toLocaleString();
            const discoveryTime = new Date(penguinData.datetime).toLocaleString();

            const predictionElement = document.getElementById("prediction");
            let message = '';

            if (penguinData.species === "Adelie") {
                message = `✅ 🔥 Mission Success! Today's Penguin Identified as: ${penguinData.species} 🐧`;
                predictionElement.className = "prediction-success";
            } else {
                message = `❌ Mission Unsuccessful! Today's Penguin Identified as: ${penguinData.species}. 😔`;
                predictionElement.className = "prediction-fail";
            }

            predictionElement.textContent = message;

            const dataTable = document.createElement('table');
            dataTable.innerHTML = `
                <thead>
                    <tr>
                        <th onclick="createPenguinRain()">Penguin Species</th>
                        <th onclick="createPenguinRain()">Bill Length (mm)</th>
                        <th onclick="createPenguinRain()">Bill Depth (mm)</th>
                        <th onclick="createPenguinRain()">Flipper Length (mm)</th>
                        <th onclick="createPenguinRain()">Body Mass (g)</th>
                        <th onclick="createPenguinRain()">Discovery Time</th>
                        <th onclick="createPenguinRain()">Prediction Time</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>${penguinData.species}</td>
                        <td>${penguinData.bill_length_mm.toFixed(2)} mm</td>
                        <td>${penguinData.bill_depth_mm.toFixed(2)} mm</td>
                        <td>${penguinData.flipper_length_mm.toFixed(2)} mm</td>
                        <td>${penguinData.body_mass_g.toFixed(2)} g</td>
                        <td>${discoveryTime}</td>
                        <td>${predictionTime}</td>
                    </tr>
                </tbody>
            `;
            document.getElementById("data-table").appendChild(dataTable);
        } else {
            document.getElementById("prediction").textContent = "❌ Mission Failed! Penguins are undercover!";
        }
    } catch (error) {
        console.error("Error fetching prediction:", error);
    }
}

async function fetchPreviousPredictions() {
    try {
        const response = await fetch("predictions.json");
        if (response.ok) {
            const predictionsData = await response.json();
            const sortedPredictions = predictionsData.sort((a, b) =>
                new Date(b.prediction_time) - new Date(a.prediction_time)
            );

            let previousPredictionsTable = `<table>
                <thead>
                    <tr>
                        <th>Species</th>
                        <th>Bill Length (mm)</th>
                        <th>Bill Depth (mm)</th>
                        <th>Flipper Length (mm)</th>
                        <th>Body Mass (g)</th>
                        <th>Discovery Time</th>
                        <th>Prediction Time</th>
                    </tr>
                </thead>
                <tbody>
            `;

            sortedPredictions.forEach(prediction => {
                previousPredictionsTable += `
                    <tr>
                        <td>${prediction.species}</td>
                        <td>${prediction.bill_length_mm.toFixed(2)} mm</td>
                        <td>${prediction.bill_depth_mm.toFixed(2)} mm</td>
                        <td>${prediction.flipper_length_mm.toFixed(2)} mm</td>
                        <td>${prediction.body_mass_g.toFixed(2)} g</td>
                        <td>${new Date(prediction.datetime).toLocaleString()}</td>
                        <td>${new Date(prediction.prediction_time).toLocaleString()}</td>
                    </tr>
                `;
            });

            previousPredictionsTable += '</tbody></table>';
            document.getElementById("previous-predictions").innerHTML = previousPredictionsTable;
        }
    } catch (error) {
        console.error("Error fetching previous predictions:", error);
    }
}

function createPenguinRain() {
    for (let i = 0; i < 1000; i++) {
        const penguin = document.createElement("div");
        penguin.classList.add("penguin");
        penguin.textContent = "🐧";
        penguin.style.position = "fixed";
        penguin.style.left = Math.random() * 100 + "vw";
        penguin.style.top = "-5%";
        penguin.style.fontSize = Math.random() * 20 + 10 + "px";
        penguin.style.animation = `fall ${Math.random() * 2 + 3}s linear forwards`;

        document.body.appendChild(penguin);

        setTimeout(() => penguin.remove(), 5000);
    }
}

function triggerEasterEgg() {
    alert("🐧 COMMANDO PENGUIN ATTACK ACTIVATED! 💥");
}

fetchPrediction();
fetchPreviousPredictions();

/* Penguin Falling Animation */
const styleSheet = document.createElement("style");
styleSheet.innerHTML = `
    @keyframes fall {
        0% { transform: translateY(0); }
        100% { transform: translateY(100vh); }
    }
`;
document.head.appendChild(styleSheet);
