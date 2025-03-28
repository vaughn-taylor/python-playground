# 🐍 Python Playground Starter
![WIP](https://img.shields.io/badge/🚧-work%20in%20progress-orange)

This is a modular, developer-friendly Python boilerplate for building Flask web apps with a modern frontend powered by Tailwind CSS v4 and Vite. Ideal for experimenting, learning, or starting new Flask-based projects.

---

## 📊 Project Info

![Version](https://img.shields.io/github/v/release/vaughn-taylor/python-playground?label=release)
![License](https://img.shields.io/github/license/vaughn-taylor/python-playground?color=blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Last Commit](https://img.shields.io/github/last-commit/vaughn-taylor/python-playground)
![Issues](https://img.shields.io/github/issues/vaughn-taylor/python-playground)
![Pull Requests](https://img.shields.io/github/issues-pr/vaughn-taylor/python-playground)
![Stars](https://img.shields.io/github/stars/vaughn-taylor/python-playground?style=social)
![Forks](https://img.shields.io/github/forks/vaughn-taylor/python-playground?style=social)

---

## 🧪 Tech Stack

[![Flask](https://img.shields.io/badge/flask-2.x-lightgrey?logo=flask)](https://flask.palletsprojects.com/)
[![Vite](https://img.shields.io/badge/vite-5.x-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/tailwindcss-4.x-38B2AC?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Dark Mode](https://img.shields.io/badge/dark--mode-supported-000000?logo=halfmoon&logoColor=white)](https://tailwindcss.com/docs/dark-mode)
[![Jinja](https://img.shields.io/badge/jinja-3.x-B41717?logo=jinja&logoColor=white)](https://jinja.palletsprojects.com/)
[![HTML](https://img.shields.io/badge/html-5-orange?logo=html5)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS](https://img.shields.io/badge/css-3-264de4?logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)

---

## 🚀 Features

- ✅ **Flask** with auto-reloading templates
- 🎨 **Tailwind CSS v4** via Vite (with build pipeline)
- 🔍 Log viewer and archiving tool
- 🧩 Modular project structure
- 🧪 Sample utilities and route blueprints
- 🌈 Dark mode support
- 📦 Preconfigured `.gitignore`

---

## 📁 Project Structure

```
src/
├── app.py             # Main Flask entry point
├── routes/            # Flask Blueprints (e.g. logs.py)
├── utils/             # Python utilities (e.g. time formatter)
├── examples/          # Scripts and experiments
├── templates/         # Jinja templates
├── frontend/          # Tailwind CSS + Vite frontend
static/                # Compiled assets from Vite
logs/                  # Runtime logs + archive
```

---

## 🧰 Requirements

- Python 3.10+
- Node.js (for Tailwind+Vite)
- `pip install -r requirements.txt`
- `npm install` (inside `src/frontend`)

---

## 🛠 Usage

### 🔧 1. Build frontend
```bash
npm run build
```

### 🧪 2. Run app
```bash
python src/app.py
```

Then visit [http://localhost:5050](http://localhost:5050)

## 🛠 ALTERNATELY: Vite Watch + Run app

```bash
npm run dev
```

Then visit [http://localhost:5050](http://localhost:5050)


---

## 🧪 Example Scripts

```bash
python src/examples/parse_log.py
```

---

## 📚 Tips

- Tailwind config is in `vite.config.mjs` and `style.css`
- Logs archive automatically from `app_events.log`
- You can add Blueprints under `src/routes` and register them in `app.py`
- Live reload is difficult to achieve — `⌘R` is always faithful ❤️

---

## 📎 License

MIT – Use freely for personal, learning, or commercial projects.

---

<p align="center">
  Made with ❤️ using Flask, TailwindCSS+Vite, and Python
</p>
