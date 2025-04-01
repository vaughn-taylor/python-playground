
# 🐍 Python Playground

This is a modern Python + JavaScript boilerplate that integrates **Flask**, **Tailwind CSS v4**, **Vite**, and **SQLite**, designed to serve as a flexible, full-stack playground for tinkering, prototyping, and building creative web apps.

---

## 🚀 Tech Stack

- **Backend:** Python 3 + Flask
- **Frontend:** Vite + Tailwind CSS v4
- **Database:** SQLite (`data/app.db`)
- **Build Tools:** Node.js, npm

---

## 📁 Project Structure

```
python-playground/
├── bootstrap/              # Environment setup scripts
├── data/                   # SQLite DB lives here
│   └── app.db              # Main database file
├── logs/                   # Log output directory
├── src/
│   ├── backend/            # Flask backend code
│   ├── frontend/           # JS + CSS source files (Vite entry point)
│   │   ├── main.js
│   │   └── style.css       # Tailwind @source config here
├── static/                 # Built assets from Vite
│   └── .vite/manifest.json # Used by Flask to resolve assets
├── templates/              # Jinja2 HTML templates
├── tests/                  # Python unit tests
├── .flaskenv               # Flask environment config
├── package.json            # JS dependencies
├── requirements.txt        # Python dependencies
├── run.py                  # Main entrypoint to run Flask app
└── README.md               # This file
```

---

## 🧵 Tailwind v4 + Vite Integration

### 🧠 Tailwind Setup (v4)
Tailwind v4 now uses a CSS-driven config approach. In `src/frontend/style.css`:

```css
@import "tailwindcss";

@source "../templates/**/*.html";
@custom-variant dark (&:where(.dark, .dark *));
```

No more `tailwind.config.js` needed!

### ⚙️ Vite Configuration
```js
// vite.config.mjs
import { defineConfig } from 'vite'
import path from 'path'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  root: './src/frontend',
  build: {
    outDir: '../../static',
    emptyOutDir: true,
    manifest: true,
    manifestDir: '.',
    rollupOptions: {
      input: './src/frontend/main.js',
    },
  },
  plugins: [tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src/frontend'),
    },
  },
})
```

---

## 🌐 Flask + Vite Asset Loader

A custom helper in Flask (`get_asset_path`) reads the Vite manifest to inject the correct hashed file paths into your HTML:

```html
<link rel="stylesheet" href="{{ get_asset_path('main.css') }}">
<script type="module" src="{{ get_asset_path('main.js') }}"></script>
```

Registered globally via:
```python
@app.context_processor
def inject_asset_path():
    return {'get_asset_path': get_asset_path}
```

---

## 💾 Database

- Uses SQLite located at `data/app.db`
- You can seed it with `seed_sales_db.py`

---

## 🛠️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/vaughn-taylor/python-playground.git
cd python-playground
```

### 2. Install Python dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Install JS dependencies
```bash
npm install
```

### 4. Build assets (once)
```bash
npm run build
```

Or use the dev server for live reloading:
```bash
npm run dev
```

### 5. Run the Flask app
```bash
flask run
# or
python run.py
```

---

## 🧪 Testing

Run your Python tests:
```bash
pytest
```

---

## 📸 Screenshots or Demos

_coming soon_

---

## 🙌 Credits

Built with ❤️ by [Vaughn Taylor](https://github.com/vaughn-taylor) and [Pythoneer 🐍].

---
