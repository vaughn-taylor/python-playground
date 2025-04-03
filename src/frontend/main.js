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

// TOAST-UI WYSIWYG

import Editor from '@toast-ui/editor';
import '@toast-ui/editor/dist/toastui-editor.css';
import { showToast } from './toast.js';

// Prism syntax highlighting plugin
import codeSyntaxHighlight from '@toast-ui/editor-plugin-code-syntax-highlight';
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css'; // Or choose another Prism theme
import './plugins/prism-tomorrow.css'; // Front end rendering

// Optionally add specific languages you want to highlight
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-json';
import 'prismjs/components/prism-bash';
import 'prismjs/components/prism-javascript';

document.addEventListener('DOMContentLoaded', () => {
    const el = document.querySelector('#editor');
    if (el) {
        const form = document.querySelector('form');
        const hiddenInput = document.querySelector('input[name="content"]');
        const submitBtn = form?.querySelector('button[type="submit"]');

        const editor = new Editor({
            el,
            height: '600px',
            initialEditType: 'wysiwyg',
            previewStyle: 'tab',
            initialValue: hiddenInput.value || '',
            placeholder: 'Write your page content here...',
            plugins: [[codeSyntaxHighlight, { highlighter: Prism }]],
            hooks: {
                addImageBlobHook: async (blob, callback) => {
                    try {
                        const formData = new FormData();
                        formData.append("image", blob);

                        const res = await fetch("/admin/upload-image", {
                            method: "POST",
                            body: formData,
                        });

                        const data = await res.json();
                        if (data.success && data.url) {
                            const rawName = blob.name || "uploaded-image";
                            const altText = rawName
                                .replace(/\.[^/.]+$/, "")
                                .replace(/[_\s]+/g, "-")
                                .replace(/[^\w\-]+/g, "")
                                .toLowerCase();

                            callback(data.url, altText);
                            showToast("Image uploaded successfully!", "success");
                        } else {
                            showToast(data.message || "Image upload failed.", "error");
                        }
                    } catch (err) {
                        console.error("Image upload error:", err);
                        showToast("Upload failed: " + err.message, "error");
                    }
                }
            }
        });

        // 🔁 Replace hidden input value on submit
        form.addEventListener('submit', () => {
            hiddenInput.value = editor.getMarkdown();

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
                submitBtn.innerText = 'Saving...';
            }
        });
    }
});

// =========================
// 🔦 Prism Front-End Highlighting
// =========================

document.addEventListener('DOMContentLoaded', () => {
    Prism.highlightAll();
});

// =========================
// Add Keyboard Commands
// =========================

document.addEventListener('keydown', (e) => {
    const key = e.key.toLowerCase();
    const isModifier = e.ctrlKey || e.metaKey;

    const form = document.querySelector('form');
    const submitBtn = form?.querySelector('button[type="submit"]');

    // ⌘ + S → save and go to list
    if (isModifier && !e.shiftKey && key === 's') {
        e.preventDefault();
        if (form) {
            form.querySelector('input[name="next_action"]').value = 'list';
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
                submitBtn.innerText = 'Saving...';
            }
            form.requestSubmit();
        }
    }

    // ⌘ + ⇧ + S → save and go to view page
    if (isModifier && e.shiftKey && key === 's') {
        e.preventDefault();
        if (form) {
            form.querySelector('input[name="next_action"]').value = 'view';
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
                submitBtn.innerText = 'Saving...';
            }
            form.requestSubmit();
        }
    }
});
