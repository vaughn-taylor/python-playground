# 🐍 Python Playground Starter

![WIP](https://img.shields.io/badge/🚧-work%20in%20progress-orange)

This is a modular, developer-friendly Python boilerplate for building **Flask** web apps with a modern frontend powered by **Tailwind CSS v4** and **Vite**. Ideal for experimenting, learning, or kicking off new Flask-based projects with modern styling and dev tools.

---

## 📊 Project Info

![Version](https://img.shields.io/github/v/release/vaughn-taylor/python-playground?label=release)
![License](https://img.shields.io/github/license/vaughn-taylor/python-playground?color=blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Last Commit](https://img.shields.io/github/last-commit/vaughn-taylor/python-playground)
![Issues](https://img.shields.io/github/issues/vaughn-taylor/python-playground)
![Pull Requests](https://img.shields.io/github/issues-pr/vaughn-taylor/python-playground)

---

## 🧰 Tech Stack

- **Backend**: Flask (modular, with `bootstrap/` init layer)
- **Frontend**: Tailwind CSS v4 + Vite
- **JS Tools**: Node/NPM
- **Build Output**: Served via Flask from `/static/assets/`

---

## 📁 Project Structure

```
python-playground/
├── bootstrap/                # App config, logging, env loading
├── src/
│   └── frontend/             # Vite entry point, Tailwind CSS, JS
│       ├── main.js
│       └── style.css
├── templates/                # Flask Jinja templates
├── static/                   # Vite builds output here
│   └── assets/
│       ├── main.js
│       └── main.css
├── vite.config.mjs           # Vite config for building frontend
├── run.py                    # Flask entry point
├── requirements.txt
└── README.md
```

---

## 🚀 Quickstart

### 1. Clone and install Python dependencies

```bash
git clone https://github.com/your-username/python-playground.git
cd python-playground
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Install and build frontend

```bash
npm install
npm run build  # or `npm run dev` during development
```

### 3. Run Flask

```bash
flask run
```

Then visit [http://localhost:5000](http://localhost:5000)

---

## 🎨 Tailwind CSS v4 Configuration

Tailwind v4 no longer uses `tailwind.config.js`. Instead, configuration is embedded in CSS:

```css
/* src/frontend/style.css */
@import "tailwindcss";

@source "../../templates/**/*.html";
@custom-variant dark (&:where(.dark, .dark *));
```

This keeps config CSS-first and scoped to the templates Flask renders.

---

## ⚙️ Vite Setup Highlights

```js
// vite.config.mjs
export default defineConfig({
  root: './src/frontend',
  build: {
    outDir: '../../static/assets',
    emptyOutDir: true,
    manifest: true,
    manifestDir: '../.vite',
    rollupOptions: {
      input: './src/frontend/main.js'
    }
  }
});
```

- Outputs `main.js` and `main.css` to `/static/assets/`
- Generates a manifest in `.vite/manifest.json` for Flask to use

---

## 🧠 Flask + Vite Integration

Flask uses a helper called `get_asset_path()` to read the Vite manifest and inject the correct hashed asset paths into templates:

```html
<!-- base.html -->
<link rel="stylesheet" href="{{ get_asset_path('main.css') }}">
<script type="module" src="{{ get_asset_path('main.js') }}"></script>
```

The helper is registered globally via:

```python
@app.context_processor
def inject_asset_path():
    return {'get_asset_path': get_asset_path}
```

---

## 🤓 For Dev Mode

To use Vite’s hot module reload in dev:

```bash
npm run dev
```

And in your `base.html`, you can load from `localhost:5173` directly for live reloading if needed.

---

## 📌 TODO / Ideas

- Add basic auth + database integration
- Extend with Blueprints for multi-page routing
- Set up Docker for deployment
- Add tests + CI support

---

**Logged with ❤️ by Pythoneer + Vaughn**
