async function fetchPrediction() {
    try {
        const response = await fetch('https://trifon-git.github.io/BDS24_MLOps_Assignment1/latest_penguin.json');
        const data = await response.json();

        if (!data.species) {
            throw new Error("Species data not found in JSON.");
        }

        // Update Timestamp
        document.getElementById('timestamp').innerText = `Last updated: ${data.datetime}`;

        // Display Prediction
        document.getElementById('prediction').innerHTML = `
            <div class="prediction-box">
                <div class="prediction-text">${data.species} Penguin Spotted! 🐧</div>
            </div>
        `;

        // Display Penguin Measurements
        const penguinData = data;
        const dataDiv = document.getElementById('penguin-data');
        dataDiv.innerHTML = '<h2>Penguin Measurements 📏</h2>';

        const keysToShow = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'];

        keysToShow.forEach(key => {
            if (penguinData[key]) {
                dataDiv.innerHTML += `
                    <div class="data-item">
                        <strong>${formatLabel(key)}:</strong> ${Number(penguinData[key]).toFixed(2)}
                    </div>`;
            }
        });
    } catch (error) {
        console.error(error);
        document.getElementById('error-message').innerText = 'Error loading prediction. Please check your JSON file.';
    }
}

function formatLabel(key) {
    return key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
}

fetchPrediction();
