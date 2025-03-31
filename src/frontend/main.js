import './style.css';
import Chart from 'chart.js/auto';

let salesChart;

async function renderSalesChart(start = "", end = "") {
    const ctx = document.getElementById('salesChart');
    const chartContainer = ctx?.parentElement; // so we can add a message below it
    if (!ctx) return;

    try {
        const params = new URLSearchParams();
        if (start) params.append("start", start);
        if (end) params.append("end", end);

        const response = await fetch(`/api/sales?${params.toString()}`);
        const data = await response.json();

        // 🔄 Destroy existing chart if it exists
        if (salesChart) {
            salesChart.destroy();
            salesChart = null;
        }

        // ❗ Handle no data
        if (!data.length) {
            ctx.style.display = 'none'; // hide canvas
            const msgId = "no-data-msg";
            if (!document.getElementById(msgId)) {
                const msg = document.createElement("p");
                msg.id = msgId;
                msg.className = "text-center text-sm text-gray-500 dark:text-gray-400 mt-4";
                msg.innerText = "No sales found for this date range.";
                chartContainer.appendChild(msg);
            }
            return;
        }

        // ✅ Otherwise, draw chart
        ctx.style.display = 'block';
        const oldMsg = document.getElementById("no-data-msg");
        if (oldMsg) oldMsg.remove();

        const labels = data.map(entry => entry.date);
        const values = data.map(entry => entry.total);

        salesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: 'Sales ($)',
                    data: values,
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { labels: { color: '#fff' } }
                },
                scales: {
                    x: { ticks: { color: '#ccc' } },
                    y: { ticks: { color: '#ccc' } }
                }
            }
        });

    } catch (error) {
        console.error("Error loading sales data:", error);
    }
}

document.getElementById('sales-filter')?.addEventListener('submit', e => {
    e.preventDefault();
    const start = document.getElementById('startDate').value;
    const end = document.getElementById('endDate').value;
    renderSalesChart(start, end);
});

// render initially with all data
renderSalesChart();
