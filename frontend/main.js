import './style.css';
import { initChat } from './js/chat';
import { initAnalyze } from './js/analyze';

document.addEventListener("DOMContentLoaded", () => {
    const page = document.body.dataset.page;

    if (page === "chat") {
        initChat();
    } else if (page === "analyze") {
        initAnalyze();
    }
});
