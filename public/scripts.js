async function fetchPrediction() {
    const response = await fetch("latest_penguin.json");
    if (response.ok) {
        const penguinData = await response.json();
        document.getElementById("prediction").textContent = `🔥 Mission Success! Penguin Species Identified: ${penguinData.species} 🐧`;

        const dataTable = document.createElement('table');
        dataTable.innerHTML = `
            <tr>
                <th onclick="createPenguinRain()">Penguin Species</th>
                <th onclick="createPenguinRain()">Bill Length (mm)</th>
                <th onclick="createPenguinRain()">Bill Depth (mm)</th>
                <th onclick="createPenguinRain()">Flipper Length (mm)</th>
                <th onclick="createPenguinRain()">Body Mass (g)</th>
                <th onclick="createPenguinRain()">Discovery Time</th>
            </tr>
            <tr>
                <td>${penguinData.species}</td>
                <td>${penguinData.bill_length_mm.toFixed(2)}</td>
                <td>${penguinData.bill_depth_mm.toFixed(2)}</td>
                <td>${penguinData.flipper_length_mm.toFixed(2)}</td>
                <td>${penguinData.body_mass_g.toFixed(2)}</td>
                <td>${new Date(penguinData.datetime).toLocaleString()}</td>
            </tr>
        `;
        document.getElementById("data-table").appendChild(dataTable);
    } else {
        document.getElementById("prediction").textContent = "❌ Mission Failed! Penguins are undercover!";
    }
}

fetchPrediction();

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
