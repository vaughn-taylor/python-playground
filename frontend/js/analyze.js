import Chart from 'chart.js/auto';

let chart = null; // Global chart instance to manage redraws

export function initAnalyze() {
    const analyzeForm = document.getElementById("analyze-form");
    const analyzeInput = document.getElementById("analyze-input");
    const analyzeResult = document.getElementById("analyze-result");
    const uploadForm = document.getElementById("upload-form");
    const uploadInput = document.getElementById("csv-file");
    const uploadStatus = document.getElementById("upload-status");
    const fileSelect = document.getElementById("selected-file");
    const chartCanvas = document.getElementById("analyze-chart");
    const chartTypeSelect = document.getElementById("chart-type");
    const downloadBtn = document.getElementById("download-chart");
    const csvBtn = document.getElementById("download-csv");

    async function loadFileOptions() {
        try {
            const res = await fetch("/api/list-uploads");
            const files = await res.json();

            if (Array.isArray(files)) {
                files.forEach((filename) => {
                    const option = document.createElement("option");
                    option.value = filename;
                    option.textContent = filename;
                    fileSelect.appendChild(option);
                });
            }
        } catch (err) {
            console.error("Failed to load file list", err);
        }
    }

    if (fileSelect) loadFileOptions();

    if (analyzeForm && analyzeInput && analyzeResult) {
        analyzeForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            analyzeResult.textContent = "Thinking... 🤔";

            if (downloadBtn) {
                downloadBtn.classList.add("hidden");
                downloadBtn.disabled = true;
            }

            if (csvBtn) {
                csvBtn.classList.add("hidden");
                csvBtn.disabled = true;
            }

            const query = analyzeInput.value.trim();
            const selectedFile = fileSelect?.value;
            const chartType = chartTypeSelect?.value || "bar";

            if (!query) {
                analyzeResult.textContent = "Please enter a question.";
                return;
            }

            if (!selectedFile) {
                analyzeResult.textContent = "Please select a CSV file to analyze.";
                return;
            }

            try {
                const res = await fetch("/api/analyze", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        query,
                        selected_file: selectedFile,
                        chart_type: chartType,
                    }),
                });

                const data = await res.json();
                analyzeResult.textContent = data.result || data.error || "Unknown error";

                // 🎯 Draw chart if backend provided chart data
                if (data.chart && chartCanvas) {
                    const { labels, values } = data.chart;
                    const type = chartType === "area" ? "line" : chartType;

                    if (chart) {
                        chart.destroy();
                    }

                    chart = new Chart(chartCanvas, {
                        type,
                        data: {
                            labels,
                            datasets: [{
                                label: 'Value',
                                data: values,
                                fill: chartType === "area",
                                backgroundColor: 'rgba(132, 204, 22, 0.6)',
                                borderColor: 'rgba(132, 204, 22, 1)',
                                borderWidth: 1,
                                tension: 0.4,
                                pointRadius: chartType === "scatter" ? 5 : 3
                            }]
                        },
                        options: {
                            responsive: true,
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    ticks: {
                                        callback: value => Intl.NumberFormat().format(value)
                                    }
                                }
                            }
                        }
                    });

                    if (downloadBtn) {
                        downloadBtn.classList.remove("hidden");
                        downloadBtn.disabled = false;
                        downloadBtn.addEventListener("click", () => {
                            const link = document.createElement("a");
                            link.href = chart.toBase64Image();
                            link.download = "chart.png";
                            link.click();
                        }, { once: true });
                    }

                    if (csvBtn) {
                        csvBtn.classList.remove("hidden");
                        csvBtn.disabled = false;
                        csvBtn.addEventListener("click", () => {
                            const rows = [["Label", "Value"], ...labels.map((label, i) => [label, values[i]])];
                            const csv = rows.map(row => row.join(",")).join("\n");
                            const blob = new Blob([csv], { type: "text/csv" });
                            const url = URL.createObjectURL(blob);
                            const link = document.createElement("a");
                            link.href = url;
                            link.download = "chart-data.csv";
                            link.click();
                            URL.revokeObjectURL(url);
                        }, { once: true });
                    }

                    // 💾 Enable download button after chart is drawn
                    if (downloadBtn) {
                        downloadBtn.disabled = false;
                        downloadBtn.addEventListener("click", () => {
                            const link = document.createElement("a");
                            link.href = chart.toBase64Image();
                            link.download = "chart.png";
                            link.click();
                        }, { once: true });
                    }
                }
            } catch (err) {
                analyzeResult.textContent = "⚠️ Could not contact server.";
            }
        });
    }

    if (uploadForm && uploadInput && uploadStatus) {
        uploadForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const file = uploadInput.files[0];
            if (!file) {
                uploadStatus.textContent = "Please select a CSV file.";
                return;
            }

            const formData = new FormData();
            formData.append("file", file);

            uploadStatus.textContent = "Uploading... 📤";

            try {
                const res = await fetch("/api/upload-earnings", {
                    method: "POST",
                    body: formData,
                });

                const data = await res.json();
                uploadStatus.textContent = data.message || data.error || "Unknown error";

                if (!data.error) {
                    fileSelect.innerHTML =
                        '<option value="" disabled selected>Select an uploaded file</option>';
                    loadFileOptions();
                }
            } catch (err) {
                uploadStatus.textContent = "⚠️ Upload failed.";
            }
        });
    }
}
