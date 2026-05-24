// --------------------------------------------------
// Slider Linking
// --------------------------------------------------

function linkSlider(sliderId, numberId) {

    const slider = document.getElementById(sliderId);
    const number = document.getElementById(numberId);

    if (!slider || !number) return;

    slider.addEventListener("input", () => {
        number.value = slider.value;
    });

    number.addEventListener("input", () => {
        slider.value = number.value;
    });

    number.value = slider.value;
}


// --------------------------------------------------
// Slider Pairs
// --------------------------------------------------

const sliderPairs = [

    ["equity_opening_slider", "equity_opening_number"],
    ["equity_monthly_slider", "equity_monthly_number"],
    ["equity_cagr_slider", "equity_cagr_number"],

    ["fd_opening_slider", "fd_opening_number"],
    ["fd_monthly_slider", "fd_monthly_number"],
    ["fd_cagr_slider", "fd_cagr_number"],

    ["bonds_opening_slider", "bonds_opening_number"],
    ["bonds_monthly_slider", "bonds_monthly_number"],
    ["bonds_cagr_slider", "bonds_cagr_number"],

    ["gold_opening_slider", "gold_opening_number"],
    ["gold_monthly_slider", "gold_monthly_number"],
    ["gold_cagr_slider", "gold_cagr_number"],

    ["years_slider", "years_number"],

    ["tax_rate_slider", "tax_rate_number"],
    ["withdraw_amount_slider", "withdraw_amount_number"],
    ["withdraw_increase_slider", "withdraw_increase_number"],
    ["growth_rate_slider", "growth_rate_number"]

];

sliderPairs.forEach(pair => {
    linkSlider(pair[0], pair[1]);
});


// --------------------------------------------------
// INR Formatter
// --------------------------------------------------

function formatINR(value) {

    return "₹ " + Number(value).toLocaleString("en-IN", {
        maximumFractionDigits: 0
    });
}


// --------------------------------------------------
// Create Table
// --------------------------------------------------

function createTable(title, rows) {

    if (!rows || rows.length === 0) return "";

    let html = `
        <div class="result-card">
            <h2>${title}</h2>

            <table>
                <thead>
                    <tr>
    `;

    Object.keys(rows[0]).forEach(col => {
        html += `<th>${col}</th>`;
    });

    html += `
                    </tr>
                </thead>
                <tbody>
    `;

    rows.forEach(row => {

        html += "<tr>";

        Object.entries(row).forEach(([key, value]) => {

            if (
                typeof value === "number"
                &&
                key !== "Year"
            ) {
                html += `<td>${formatINR(value)}</td>`;
            }
            else {
                html += `<td>${value}</td>`;
            }

        });

        html += "</tr>";
    });

    html += `
                </tbody>
            </table>

            <canvas id="${title.replace(/\s/g, '')}Chart"></canvas>

        </div>
    `;

    return html;
}


// --------------------------------------------------
// Create Chart
// --------------------------------------------------

function createChart(canvasId, title, rows) {

    const ctx = document.getElementById(canvasId);

    if (!ctx) return;

    const labels = rows.map(r => r.Year);

    let data = [];

    if (rows[0]["Closing"]) {
        data = rows.map(r => r["Closing"]);
    }
    else if (rows[0]["Closing Corpus"]) {
        data = rows.map(r => r["Closing Corpus"]);
    }

    new Chart(ctx, {

        type: "line",

        data: {

            labels: labels,

            datasets: [{
                label: title,
                data: data,
                borderWidth: 3,
                tension: 0.3,
                fill: false
            }]
        },

        options: {

            responsive: true,

            plugins: {

                legend: {
                    display: true
                }
            },

            scales: {

                y: {

                    ticks: {

                        callback: function(value) {
                            return "₹ " + value.toLocaleString("en-IN");
                        }
                    }
                }
            }
        }
    });
}


// --------------------------------------------------
// Submit Forecast
// --------------------------------------------------

document
.getElementById("forecastForm")
.addEventListener("submit", async function(e) {

    e.preventDefault();

    const formData = new FormData(this);

    const data = Object.fromEntries(formData.entries());

    try {

        const response = await fetch("/run_forecast", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        });

        const result = await response.json();

        const resultsDiv = document.getElementById("results");

        resultsDiv.innerHTML = "";

        if (result.error) {

            resultsDiv.innerHTML = `
                <div class="result-card">
                    <h2>Error</h2>
                    <p>${result.error}</p>
                </div>
            `;

            return;
        }

        Object.entries(result).forEach(([title, rows]) => {

            resultsDiv.innerHTML += createTable(title, rows);

        });

        Object.entries(result).forEach(([title, rows]) => {

            createChart(
                `${title.replace(/\s/g, '')}Chart`,
                title,
                rows
            );

        });

    }
    catch (error) {

        document.getElementById("results").innerHTML = `
            <div class="result-card">
                <h2>Error</h2>
                <p>Something went wrong while generating forecast.</p>
            </div>
        `;
    }
});


// --------------------------------------------------
// Reset Handler
// --------------------------------------------------

document
.getElementById("forecastForm")
.addEventListener("reset", function() {

    setTimeout(() => {

        sliderPairs.forEach(pair => {

            const slider = document.getElementById(pair[0]);
            const number = document.getElementById(pair[1]);

            if (!slider || !number) return;

            if (pair[0] === "years_slider") {

                slider.value = 10;
                number.value = 10;
            }
            else {

                slider.value = 0;
                number.value = 0;
            }
        });

        document.getElementById("results").innerHTML = "";

    }, 0);
});