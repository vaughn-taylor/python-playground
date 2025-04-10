// src/frontend/mistral_chat.js

export function initMistralChat() {
    document.addEventListener("DOMContentLoaded", () => {
        const form = document.getElementById("chat-form");
        const input = document.getElementById("user-input");
        const chatBox = document.getElementById("chat-box");
        const chatStatus = document.getElementById("chat-status");
        const toggleDarkBtn = document.getElementById("toggle-dark");
        const chatScroll = document.getElementById("chat-scroll");
        const pauseButton = document.getElementById("pause-button");
        let paused = false;

        input?.focus();

        pauseButton?.addEventListener("click", () => (paused = true));

        if (chatScroll) {
            window.addEventListener("wheel", (e) => {
                const isOverChat = e.target.closest("#chat-scroll");
                if (!isOverChat) {
                    chatScroll.scrollTop += e.deltaY;
                    e.preventDefault();
                }
            }, { passive: false });
        }

        if (!form || !input || !chatBox) return;

        input.addEventListener("input", () => {
            input.style.height = "auto";
            input.style.height = `${input.scrollHeight}px`;
        });

        input.addEventListener("keydown", (e) => {
            const isMac = navigator.userAgentData
                ? navigator.userAgentData.platform === "macOS"
                : navigator.userAgent.toLowerCase().includes("mac");

            const isCmdEnter = isMac
                ? e.metaKey && e.key === "Enter"
                : e.ctrlKey && e.key === "Enter";

            if (isCmdEnter) {
                e.preventDefault();
                form.requestSubmit();
            }
        });

        if (toggleDarkBtn) {
            toggleDarkBtn.addEventListener("click", () => {
                document.documentElement.classList.toggle("dark");
                const isDark = document.documentElement.classList.contains("dark");
                localStorage.setItem("theme", isDark ? "dark" : "light");
            });

            const savedTheme = localStorage.getItem("theme");
            if (savedTheme === "dark") {
                document.documentElement.classList.add("dark");
            }
        }

        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            const message = input.value.trim();
            if (!message) return;

            const userMessageEl = document.createElement("div");
            userMessageEl.className =
                "relative flex justify-start items-baseline w-9/10 ml-auto bg-gray-100 dark:bg-gray-700 p-4 rounded-lg mb-6 opacity-0 translate-y-4 transition-all duration-300";
            userMessageEl.innerHTML = `
            <svg class="absolute -top-3 -right-3 w-5 h-5 rounded-full bg-indigo-100 dark:bg-indigo-500 fill-indigo-800 dark:fill-indigo-200"
                xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                <path d="..." />
            </svg>
            ${message}
            `;
            chatBox.appendChild(userMessageEl);
            setTimeout(() => {
                userMessageEl.classList.remove("opacity-0", "translate-y-4");
            }, 10);

            input.value = "";
            input.style.height = "auto";
            chatStatus?.classList.remove("hidden");
            pauseButton?.classList.remove("hidden");
            paused = false;

            try {
                const res = await fetch("/api/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message }),
                });

                const reader = res.body.getReader();
                const decoder = new TextDecoder();
                let llmResponse = "";

                const llmMessageEl = document.createElement("div");
                llmMessageEl.className =
                    "relative flex justify-start items-baseline w-full bg-gray-200 dark:bg-gray-800 p-4 rounded-lg mb-6 whitespace-pre-wrap opacity-0 translate-y-4 transition-all duration-300";
                llmMessageEl.innerHTML = `
                <svg class="absolute -top-3 -left-3 w-5 h-5 rounded-full bg-indigo-100 dark:bg-indigo-500 fill-indigo-800 dark:fill-indigo-200"
                    xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                    <path d="..." />
                </svg>
                <span id="llm-stream-text"></span>
                `;
                chatBox.appendChild(llmMessageEl);
                const streamSpan = llmMessageEl.querySelector("#llm-stream-text");

                setTimeout(() => {
                    llmMessageEl.classList.remove("opacity-0", "translate-y-4");
                }, 10);

                while (true) {
                    if (paused) break;

                    const { value, done } = await reader.read();
                    if (done) break;

                    const chunk = decoder.decode(value, { stream: true });
                    llmResponse += chunk;
                    streamSpan.textContent = llmResponse;
                    chatScroll.scrollTop = chatScroll.scrollHeight;
                }

                pauseButton?.classList.add("hidden");
                chatStatus?.classList.add("hidden");

                chatScroll.scrollTo({
                    top: chatScroll.scrollHeight,
                    behavior: "smooth"
                });

            } catch (err) {
                chatBox.innerHTML += `<div class="text-red-500">⚠️ Error: ${err.message}</div>`;
                chatStatus?.classList.add("hidden");
                pauseButton?.classList.add("hidden");
            }
        });
    });
}
