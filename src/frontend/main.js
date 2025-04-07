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

// CHATBOX //

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("chat-form")
    const input = document.getElementById("user-input")
    const chatBox = document.getElementById("chat-box")
    const chatStatus = document.getElementById("chat-status")
    const toggleDarkBtn = document.getElementById("toggle-dark")
    const chatScroll = document.getElementById("chat-scroll")
    const pauseButton = document.getElementById("pause-button")
    let paused = false

    input?.focus()

    // 🛑 PAUSE BUTTON: Attach once
    pauseButton?.addEventListener("click", () => {
        paused = true
    })

    // 🖱️ Redirect scroll to chat-scroll even if mouse is outside it
    if (chatScroll) {
        window.addEventListener("wheel", (e) => {
            const isOverChat = e.target.closest("#chat-scroll")
            if (!isOverChat) {
                chatScroll.scrollTop += e.deltaY
                e.preventDefault()
            }
        }, { passive: false })
    }

    // ⛔ Bail early if not on chat page
    if (!form || !input || !chatBox) return

    // ✏️ Auto-expand input
    input.addEventListener("input", () => {
        input.style.height = "auto"
        input.style.height = `${input.scrollHeight}px`
    })

    // ⌘ + Enter or Ctrl + Enter to submit
    input.addEventListener("keydown", (e) => {
        const isMac = navigator.userAgentData
            ? navigator.userAgentData.platform === "macOS"
            : navigator.userAgent.toLowerCase().includes("mac")
        const isCmdEnter = isMac
            ? (e.metaKey && e.key === "Enter")
            : (e.ctrlKey && e.key === "Enter")
        if (isCmdEnter) {
            e.preventDefault()
            form.requestSubmit()
        }
    })

    // 🌓 Dark mode toggle
    if (toggleDarkBtn) {
        toggleDarkBtn.addEventListener("click", () => {
            document.documentElement.classList.toggle("dark")
            const isDark = document.documentElement.classList.contains("dark")
            localStorage.setItem("theme", isDark ? "dark" : "light")
        })

        const savedTheme = localStorage.getItem("theme")
        if (savedTheme === "dark") {
            document.documentElement.classList.add("dark")
        }
    }

    // 💬 Submit chat
    form.addEventListener("submit", async (e) => {
        e.preventDefault()
        const message = input.value.trim()
        if (!message) return

        // 🎤 Show user message
        const userMessageEl = document.createElement("div")
        userMessageEl.className =
            "relative flex justify-start items-baseline w-9/10 ml-auto bg-gray-100 dark:bg-gray-700 p-4 rounded-lg mb-6 opacity-0 translate-y-4 transition-all duration-300"
        userMessageEl.innerHTML = `
        <svg class="absolute -top-3 -right-3 w-5 h-5 rounded-full bg-indigo-100 dark:bg-indigo-500 fill-indigo-800 dark:fill-indigo-200"
             xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M464 256A208 208 0 1 0 48 256a208 208 0 1 0 416 0zM0 256a256 256 0 1 1 512 0A256 256 0 1 1 0 256zm169.8-90.7c7.9-22.3 29.1-37.3 52.8-37.3l58.3 0c34.9 0 63.1 28.3 63.1 63.1c0 22.6-12.1 43.5-31.7 54.8L280 264.4c-.2 13-10.9 23.6-24 23.6c-13.3 0-24-10.7-24-24l0-13.5c0-8.6 4.6-16.5 12.1-20.8l44.3-25.4c4.7-2.7 7.6-7.7 7.6-13.1c0-8.4-6.8-15.1-15.1-15.1l-58.3 0c-3.4 0-6.4 2.1-7.5 5.3l-.4 1.2c-4.4 12.5-18.2 19-30.6 14.6s-19-18.2-14.6-30.6l.4-1.2zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"/></svg>
        ${message}
        `
        chatBox.appendChild(userMessageEl)
        setTimeout(() => {
            userMessageEl.classList.remove("opacity-0", "translate-y-4")
        }, 10)

        input.value = ""
        input.style.height = "auto"
        chatStatus?.classList.remove("hidden")
        pauseButton?.classList.remove("hidden")
        paused = false

        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message }),
            })

            const reader = res.body.getReader()
            const decoder = new TextDecoder()
            let llmResponse = ""

            const llmMessageEl = document.createElement("div")
            llmMessageEl.className =
                "relative flex justify-start items-baseline w-full bg-gray-200 dark:bg-gray-800 p-4 rounded-lg mb-6 whitespace-pre-wrap opacity-0 translate-y-4 transition-all duration-300"
            llmMessageEl.innerHTML = `
                <svg class="absolute -top-3 -left-3 w-5 h-5 rounded-full bg-indigo-100 dark:bg-indigo-500 fill-indigo-800 dark:fill-indigo-200"
                     xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M464 256A208 208 0 1 0 48 256a208 208 0 1 0 416 0zM0 256a256 256 0 1 1 512 0A256 256 0 1 1 0 256zm177.6 62.1C192.8 334.5 218.8 352 256 352s63.2-17.5 78.4-33.9c9-9.7 24.2-10.4 33.9-1.4s10.4 24.2 1.4 33.9c-22 23.8-60 49.4-113.6 49.4s-91.7-25.5-113.6-49.4c-9-9.7-8.4-24.9 1.4-33.9s24.9-8.4 33.9 1.4zM144.4 208a32 32 0 1 1 64 0 32 32 0 1 1 -64 0zm192-32a32 32 0 1 1 0 64 32 32 0 1 1 0-64z"/></svg>
                <span id="llm-stream-text"></span>
            `
            chatBox.appendChild(llmMessageEl)
            const streamSpan = llmMessageEl.querySelector("#llm-stream-text")

            setTimeout(() => {
                llmMessageEl.classList.remove("opacity-0", "translate-y-4")
            }, 10)

            while (true) {
                if (paused) break

                const { value, done } = await reader.read()
                if (done) break

                const chunk = decoder.decode(value, { stream: true })
                llmResponse += chunk
                streamSpan.textContent = llmResponse
                chatScroll.scrollTop = chatScroll.scrollHeight
            }

            pauseButton?.classList.add("hidden")
            chatStatus?.classList.add("hidden")

            chatScroll.scrollTo({
                top: chatScroll.scrollHeight,
                behavior: "smooth"
            })

        } catch (err) {
            chatBox.innerHTML += `<div class="text-red-500">⚠️ Error: ${err.message}</div>`
            chatStatus?.classList.add("hidden")
            pauseButton?.classList.add("hidden")
        }
    })
})
