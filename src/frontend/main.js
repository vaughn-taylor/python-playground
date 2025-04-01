import './style.css';
import Chart from 'chart.js/auto';

let salesChart;

async function renderSalesChart(start = "", end = "") {
    const ctx = document.getElementById('salesChart');
    const chartContainer = ctx?.parentElement;
    if (!ctx) return;

    try {
        const params = new URLSearchParams();
        if (start) params.append("start", start);
        if (end) params.append("end", end);

        // 🔀 Check the toggle and decide the endpoint
        const useMock = document.getElementById('mockToggle')?.checked;
        const endpoint = useMock ? '/api/mock-sales' : `/api/sales?${params.toString()}`;

        const response = await fetch(endpoint);
        const data = await response.json();

        if (salesChart) {
            salesChart.destroy();
            salesChart = null;
        }

        if (!data.length) {
            ctx.style.display = 'none';
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

        ctx.style.display = 'block';
        const oldMsg = document.getElementById("no-data-msg");
        if (oldMsg) oldMsg.remove();

        const labels = data.map(entry => entry.date);
        const salesValues = data.map(entry => entry.total);
        const refundValues = data.map(entry => entry.refunds || 0);

        salesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels,
                datasets: [
                    {
                        label: 'Sales ($)',
                        data: salesValues,
                        fill: false,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.3
                    },
                    {
                        label: 'Refunds ($)',
                        data: refundValues,
                        fill: false,
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: '#fff',
                            usePointStyle: true,
                            pointStyle: 'circle',
                            padding: 16,
                            font: {
                                size: 13,
                                weight: '500'
                            }
                        }
                    }
                },
                scales: {
                    x: { ticks: { color: '#ccc' } },
                    y: { ticks: { color: '#ccc' } }
                },
            }
        });

        const timestamp = new Date().toLocaleTimeString();
        document.getElementById('last-updated').innerText = `Last updated: ${timestamp}`;

        // 📊 Also update summary stats
        await fetchAndShowSummary(start, end);

    } catch (error) {
        console.error("Error loading sales data:", error);
    }
}

async function fetchAndShowSummary(start = "", end = "") {
    try {
        const params = new URLSearchParams();
        if (start) params.append("start", start);
        if (end) params.append("end", end);

        const useMock = document.getElementById('mockToggle')?.checked;
        const endpoint = useMock ? '/api/mock-totals' : `/api/totals?${params.toString()}`;

        const response = await fetch(endpoint);
        const summary = await response.json();

        document.getElementById("stat-total-sales").textContent = summary.total_sales;
        document.getElementById("stat-total-refunds").textContent = summary.total_refunds;
        document.getElementById("stat-avg-sales").textContent = summary.average_sales;
        document.getElementById("stat-range").textContent =
            summary.first_date && summary.last_date
                ? `${summary.first_date} → ${summary.last_date}`
                : "–";
    } catch (error) {
        console.error("Error loading summary stats:", error);
    }
}

document.getElementById('sales-filter')?.addEventListener('submit', e => {
    e.preventDefault();
    const start = document.getElementById('startDate').value;
    const end = document.getElementById('endDate').value;
    renderSalesChart(start, end);
});

if (document.getElementById("salesChart")) {
    renderSalesChart();
    fetchAndShowSummary();

    setInterval(() => {
        const start = document.getElementById('startDate')?.value;
        const end = document.getElementById('endDate')?.value;
        renderSalesChart(start, end);
        fetchAndShowSummary(start, end);
    }, 600000);
}
