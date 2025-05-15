import './style.css';
import { initChat } from './js/chat';

document.addEventListener("DOMContentLoaded", () => {
    const page = document.body.dataset.page;
    if (page === "chat") {
        initChat();
    }
});
