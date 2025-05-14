import { marked } from 'marked';

export function initFinanceChat() {
    const form = document.getElementById("chat-form")
    const input = document.getElementById("user-input")
    const chatBox = document.getElementById("chat-box")
    const chatStatus = document.getElementById("chat-status")
    const chatScroll = document.getElementById("chat-scroll")

    input?.focus()

    if (!form || !input || !chatBox) return

    input.addEventListener("input", () => {
        input.style.height = "auto"
        input.style.height = `${input.scrollHeight}px`
    })

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

    form.addEventListener("submit", async (e) => {
        e.preventDefault()
        const query = input.value.trim()
        if (!query) return

        // User message
        const userMessageEl = document.createElement("div")
        userMessageEl.className =
            "relative flex justify-start items-baseline w-9/10 ml-auto bg-gray-100 dark:bg-gray-700 p-4 rounded-lg mb-6 opacity-0 translate-y-4 transition-all duration-300"
        userMessageEl.innerHTML = query
        chatBox.appendChild(userMessageEl)

        setTimeout(() => {
            userMessageEl.classList.remove("opacity-0", "translate-y-4")
        }, 10)

        input.value = ""
        input.style.height = "auto"
        chatStatus?.classList.remove("hidden")

        try {
            const res = await fetch("/api/finance-chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query }),
            })

            const data = await res.json()

            const responseEl = document.createElement("div")
            responseEl.className =
                "relative flex flex-col justify-start w-full bg-gray-200 dark:bg-gray-800 p-4 rounded-lg mb-6 whitespace-pre-wrap opacity-0 translate-y-4 transition-all duration-300"
            responseEl.innerHTML = `
                <div class="flex items-start gap-1">
                    <div class="markdown-body">${marked.parse(data.response || data.error || "No response")}</div>
                </div>
            `
            chatBox.appendChild(responseEl)

            setTimeout(() => {
                responseEl.classList.remove("opacity-0", "translate-y-4")
            }, 10)

            chatStatus?.classList.add("hidden")
            chatScroll.scrollTo({ top: chatScroll.scrollHeight, behavior: "smooth" })

        } catch (err) {
            chatBox.innerHTML += `<div class="text-red-500">⚠️ Error: ${err.message}</div>`
            chatStatus?.classList.add("hidden")
        }
    })

    // ✅ Sidebar toggle logic
    const toggleSidebarBtn = document.getElementById("toggle-sidebar");
    const showSidebarBtn = document.getElementById("show-sidebar");
    const sidebar = document.getElementById("tool-sidebar");

    if (toggleSidebarBtn && showSidebarBtn && sidebar) {
        toggleSidebarBtn.addEventListener("click", () => {
            sidebar.classList.remove("block");
            sidebar.classList.add("hidden");
            toggleSidebarBtn.classList.add("hidden");
            showSidebarBtn.classList.remove("hidden");
        });

        showSidebarBtn.addEventListener("click", () => {
            sidebar.classList.remove("hidden");
            sidebar.classList.add("block");
            toggleSidebarBtn.classList.remove("hidden");
            showSidebarBtn.classList.add("hidden");
        });
    }

    // ✅ Handle sidebar prompt clicks
    document.querySelectorAll(".tool-suggestion").forEach(button => {
        button.addEventListener("click", () => {
            const prompt = button.dataset.prompt;
            if (!prompt) return;

            input.value = prompt;
            input.focus();

            // Optional: highlight [TICKER] for quick replace
            const start = prompt.indexOf("[TICKER]");
            if (start >= 0) {
                input.setSelectionRange(start, start + 8);
            }
        });
    });
}
