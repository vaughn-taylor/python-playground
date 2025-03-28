# 🐍 Python Playground Starter

This is a modular, developer-friendly Python boilerplate for building Flask web apps with a modern frontend powered by Tailwind CSS v4 and Vite. Ideal for experimenting, learning, or starting new Flask-based projects.

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