import './style.css';

import Chart from 'chart.js/auto';

async function renderSalesChart() {
    const ctx = document.getElementById('salesChart');
    if (!ctx) return;

    try {
        const response = await fetch('/api/sales');
        const data = await response.json();

        const labels = data.map(entry => entry.date);
        const values = data.map(entry => entry.total);

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
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
                    legend: {
                        labels: {
                            color: '#fff'
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: '#ccc' }
                    },
                    y: {
                        ticks: { color: '#ccc' }
                    }
                }
            }
        });

    } catch (error) {
        console.error("Error loading sales data:", error);
    }
}

renderSalesChart();
