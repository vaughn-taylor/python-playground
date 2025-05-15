import { marked } from 'marked';

export function initChat() {
    let lastInputTime = null;
    let selectedIndex = -1; // No item selected initially
    const form = document.getElementById("chat-form");
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const chatStatus = document.getElementById("chat-status");
    const chatScroll = document.getElementById("chat-scroll");
    const suggestionBox = document.getElementById("autocomplete-list");

    if (!form || !input || !chatBox || !suggestionBox) {
        console.warn("🚫 Missing key DOM elements, chat init aborted.");
        return;
    }

    input.focus();

    // ✅ Sidebar toggle logic
    const toggleSidebarBtn = document.getElementById("toggle-sidebar");
    const showSidebarBtn = document.getElementById("show-sidebar");
    const sidebar = document.getElementById("tool-sidebar");
    const toggleWrapper = document.getElementById("toggle-wrapper");

    if (toggleSidebarBtn && showSidebarBtn && sidebar) {
        toggleSidebarBtn.addEventListener("click", () => {
            sidebar.classList.add("hidden");
            sidebar.classList.remove("block");
            toggleSidebarBtn.classList.add("hidden");
            showSidebarBtn.classList.remove("hidden");
            toggleWrapper.classList.remove("border-r");
            toggleWrapper.classList.add("border-l");
        });

        showSidebarBtn.addEventListener("click", () => {
            sidebar.classList.remove("hidden");
            sidebar.classList.add("block");
            toggleSidebarBtn.classList.remove("hidden");
            showSidebarBtn.classList.add("hidden");
            toggleWrapper.classList.add("border-r");
            toggleWrapper.classList.remove("border-l");
        });
    }

    // ✅ Mirror textarea setup
    const mirror = document.getElementById("mirror-textarea");

    function updateMirror() {
        if (!mirror) return;
        const text = input.value;
        const parts = text.split(/(\s+)/); // split on whitespace
        const last = parts.pop();
        parts.push(`<span id="caret-marker">${last || "&nbsp;"}</span>`);
        mirror.innerHTML = parts.join("");

        // match styles (if needed)
        mirror.style.width = `${input.offsetWidth}px`;
        mirror.style.font = getComputedStyle(input).font;
        mirror.style.lineHeight = getComputedStyle(input).lineHeight;
        mirror.scrollTop = input.scrollTop;
    }

    function positionSuggestionBox() {
        const marker = document.getElementById("caret-marker");
        if (!marker) return;
        const markerRect = marker.getBoundingClientRect();
        const containerRect = input.getBoundingClientRect();
        const offsetTop = markerRect.bottom - containerRect.top;
        const offsetLeft = markerRect.left - containerRect.left;

        suggestionBox.style.position = "absolute";
        suggestionBox.style.top = `${offsetTop + 45}px`;
        suggestionBox.style.left = `${offsetLeft + 60}px`;
    }

    // ✅ Close autocomplete when clicking outside
    document.addEventListener("click", (e) => {
        const isInsideInput = input.contains(e.target);
        const isInsideSuggestions = suggestionBox.contains(e.target);

        if (!isInsideInput && !isInsideSuggestions) {
            suggestionBox.classList.add("hidden");
            suggestionBox.innerHTML = "";
            selectedIndex = -1;
        }
    });

    // ✅ Debounce utility
    function debounce(fn, delay = 2000) {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                console.log("⏱ Debounced autocomplete firing...");
                fn(...args);
            }, delay);
        };
    }

    // ✅ Handle suggestion clicks
    suggestionBox.addEventListener("click", (e) => {
        const target = e.target.closest("li[data-symbol]");
        if (!target) return;

        const symbol = target.dataset.symbol;

        // Replace the last $... or #... if present, otherwise append symbol
        if (/\$[A-Za-z]{0,10}$/.test(input.value) || /\#[A-Za-z]{1,10}$/.test(input.value)) {
            input.value = input.value.replace(/[$#][A-Za-z]{0,10}$/, symbol);
        } else {
            input.value = input.value.trim() + ' ' + symbol;
        }

        suggestionBox.classList.add("hidden");
        input.focus();
    });

    // ✅ Key commands for autosuggest
    input.addEventListener("keydown", (e) => {
        // ⎈ + Space → force autocomplete
        if (e.ctrlKey && e.code === "Space") {
            e.preventDefault();

            // If no $ or # trigger is found, append "$" to simulate context
            if (!input.value.match(/[$#][A-Za-z]{1,10}$/)) {
                input.value = input.value.trim() + " $";
            }

            console.log("🚀 Ctrl+Space pressed — triggering autocomplete");
            debouncedAutocomplete(true);
            return;
        }

        // ESC → close suggestions
        if (e.key === "Escape") {
            suggestionBox.classList.add("hidden");
            suggestionBox.innerHTML = "";
            return;
        }

        // ⏎ Enter key should accept first autocomplete result if visible
        if (e.key === "Enter" && !e.ctrlKey && !e.metaKey) {
            const items = suggestionBox.querySelectorAll("li[data-symbol]");
            if (!items.length || suggestionBox.classList.contains("hidden")) return;

            const targetItem = selectedIndex >= 0 ? items[selectedIndex] : items[0];
            if (!targetItem) return;

            e.preventDefault();

            const symbol = targetItem.dataset.symbol;
            if (/\s?[$#][A-Za-z]{0,10}$/.test(input.value)) {
                input.value = input.value.replace(/\s?[$#][A-Za-z]{0,10}$/, ` ${symbol}`);
            } else {
                input.value = input.value.trim() + ' ' + symbol;
            }

            suggestionBox.classList.add("hidden");
            suggestionBox.innerHTML = "";
            selectedIndex = -1;
            input.focus();
            return;
        }

        // 🔽 Down / Up arrows
        if ((e.key === "ArrowDown" || e.key === "ArrowUp") && !suggestionBox.classList.contains("hidden")) {
            e.preventDefault();

            const items = suggestionBox.querySelectorAll("li[data-symbol]");
            if (!items.length) return;

            // Update selected index
            if (e.key === "ArrowDown") {
                selectedIndex = (selectedIndex + 1) % items.length;
            } else if (e.key === "ArrowUp") {
                selectedIndex = (selectedIndex - 1 + items.length) % items.length;
            }

            // Remove previous highlights
            items.forEach(item => item.classList.remove("autocomplete-active"));

            // Add highlight to current
            items[selectedIndex].classList.add("autocomplete-active");

            items[selectedIndex].scrollIntoView({
                block: "nearest",
                behavior: "smooth"
            });

            return;
        }

        // Cmd+Enter or Ctrl+Enter → submit
        const isMac = navigator.userAgentData
            ? navigator.userAgentData.platform === "macOS"
            : navigator.userAgent.toLowerCase().includes("mac");
        const isCmdEnter = isMac
            ? (e.metaKey && e.key === "Enter")
            : (e.ctrlKey && e.key === "Enter");
        if (isCmdEnter) {
            e.preventDefault();
            form.requestSubmit();
        }
    });

    // ✅ Debounced autocomplete handler
    const debouncedAutocomplete = debounce(async (force = false) => {
        const inputText = input.value.trim();

        const symbolMatch = inputText.match(/\$([A-Za-z]{1,5})$/);
        const nameMatch = inputText.match(/\#([A-Za-z]{1,})$/);

        let query = null;
        let mode = "symbol";

        if (symbolMatch) {
            query = symbolMatch[1].toUpperCase();
            mode = "symbol";
        } else if (nameMatch) {
            query = nameMatch[1].toUpperCase();
            mode = "name";
        }

        if (!force && !query) {
            suggestionBox.innerHTML = "";
            suggestionBox.classList.add("hidden");
            return;
        }

        if (!query && force) {
            // fallback default: just suggest top 10 popular symbols
            query = ""; // empty string will match everything in the backend
            mode = "symbol";
        }

        console.log("📥 Triggered autocomplete", { query, mode, force });

        try {
            const res = await fetch(`/api/autocomplete?q=${query}&mode=${mode}`);
            const data = await res.json();

            if (!data.length) {
                suggestionBox.classList.add("hidden");
                return;
            }

            suggestionBox.innerHTML = data.map((t, i) => `
                <li class="px-4 py-2 cursor-pointer hover:bg-stone-200 dark:hover:bg-stone-600"
                    data-symbol="${t.symbol}" data-index="${i}">
                    <span class="font-bold">${t.symbol}</span> — <span class="text-sm">${t.name}</span>
                </li>
            `).join("");

            selectedIndex = -1; // reset on every new list
            suggestionBox.classList.remove("hidden");

        } catch (err) {
            suggestionBox.classList.add("hidden");
        }
    }, 500);


    // ✅ Single input event listener
    input.addEventListener("input", () => {
        lastInputTime = performance.now();
        console.log(`🖊 Input at ${new Date().toLocaleTimeString()}`);

        // Immediately hide any existing suggestions
        suggestionBox.classList.add("hidden");
        suggestionBox.innerHTML = "";

        // Resize input box
        input.style.height = "auto";
        input.style.height = `${input.scrollHeight}px`;

        // Debounced logic
        debouncedAutocomplete();

        updateMirror();
        positionSuggestionBox();
    });

    // Enter key submit
    input.addEventListener("keydown", (e) => {
        const isMac = navigator.userAgentData
            ? navigator.userAgentData.platform === "macOS"
            : navigator.userAgent.toLowerCase().includes("mac");
        const isCmdEnter = isMac
            ? (e.metaKey && e.key === "Enter")
            : (e.ctrlKey && e.key === "Enter");
        if (isCmdEnter) {
            e.preventDefault();
            form.requestSubmit();
        }
    });

    // ✅ Handle sidebar tool clicks
    document.querySelectorAll(".tool-suggestion").forEach(button => {
        button.addEventListener("click", () => {
            const prompt = button.dataset.prompt;
            if (!prompt) return;

            input.value = prompt;
            input.focus();

            // Try to highlight [TICKER] if present
            const start = prompt.indexOf("[TICKER]");
            if (start >= 0) {
                input.setSelectionRange(start, start + "[TICKER]".length);
            }

            updateMirror();
            positionSuggestionBox();
        });
    });

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const query = input.value.trim();
        if (!query) return;

        const userMessageEl = document.createElement("div");
        userMessageEl.className =
            "relative flex justify-start items-baseline w-9/10 ml-auto bg-gray-100 dark:bg-gray-700 p-6 rounded-lg mb-6 opacity-0 translate-y-4 transition-all duration-300";
        userMessageEl.innerHTML = query;
        chatBox.appendChild(userMessageEl);

        setTimeout(() => {
            userMessageEl.classList.remove("opacity-0", "translate-y-4");
        }, 10);

        input.value = "";
        input.style.height = "auto";
        chatStatus?.classList.remove("hidden");

        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query }),
            });

            const data = await res.json();

            const responseEl = document.createElement("div");
            responseEl.className =
                "relative flex flex-col justify-start w-full bg-gray-200 dark:bg-gray-800 p-6 rounded-lg mb-6 opacity-0 translate-y-4 transition-all duration-300";
            responseEl.innerHTML = `
                <div class="flex items-start">
                    <div class="markdown-body">${marked.parse(data.response || data.error || "No response")}</div>
                </div>
            `;
            chatBox.appendChild(responseEl);

            setTimeout(() => {
                responseEl.classList.remove("opacity-0", "translate-y-4");
            }, 10);

            chatStatus?.classList.add("hidden");
            chatScroll.scrollTo({ top: chatScroll.scrollHeight, behavior: "smooth" });

        } catch (err) {
            chatBox.innerHTML += `<div class="text-red-500">⚠️ Error: ${err.message}</div>`;
            chatStatus?.classList.add("hidden");
        }
    });
}
