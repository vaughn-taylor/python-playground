export function showToast(message, type = "info", duration = 5000) {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `
        max-w-sm px-4 py-2 rounded-xl shadow-lg text-sm font-medium
        transform transition-all duration-300 ease-out
        opacity-0 -translate-y-4
        ${type === "error" ? "bg-rose-600 text-white" : ""}
        ${type === "success" ? "bg-green-600 text-white" : ""}
        ${type === "info" ? "bg-gray-800 text-white" : ""}
    `;
    toast.textContent = message;

    container.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
        toast.classList.remove("opacity-0", "-translate-y-4");
        toast.classList.add("opacity-100", "translate-y-0");
    });

    // Animate out
    setTimeout(() => {
        toast.classList.remove("opacity-100", "translate-y-0");
        toast.classList.add("opacity-0", "-translate-y-4");

        setTimeout(() => toast.remove(), 300);
    }, duration);
}
