export function initAnalyze() {
    const analyzeForm = document.getElementById("analyze-form");
    const analyzeInput = document.getElementById("analyze-input");
    const analyzeResult = document.getElementById("analyze-result");

    if (!analyzeForm || !analyzeInput || !analyzeResult) return;

    analyzeForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        analyzeResult.textContent = "Thinking... 🤔";

        const query = analyzeInput.value.trim();
        if (!query) {
            analyzeResult.textContent = "Please enter a question.";
            return;
        }

        try {
            const res = await fetch("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query }),
            });

            const data = await res.json();
            analyzeResult.textContent = data.result || data.error || "Unknown error";
        } catch (err) {
            analyzeResult.textContent = "⚠️ Could not contact server.";
        }
    });
}
