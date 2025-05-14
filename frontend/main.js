import './style.css';
import { initFinanceChat } from './js/finance_chat';

// ============================
// Page Bootstrap
// ============================

document.addEventListener("DOMContentLoaded", () => {
    const page = document.body.dataset.page;
    if (page === "finance-chat") {
        initFinanceChat();
    }
});
