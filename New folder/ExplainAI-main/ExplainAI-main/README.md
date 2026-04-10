# 🚀 ExplainAI

## 📌 Overview

ExplainAI is an AI-powered application designed to simplify complex concepts into easy-to-understand explanations. It provides an interactive interface where users can input queries and receive clear, structured responses.

This project demonstrates practical implementation of Python-based application development with a focus on usability and real-world problem solving.

---

## 🎯 Key Features

* 🧠 AI-based concept explanation
* 💻 User-friendly interface (Tkinter GUI / Flask Web App)
* ⚡ Fast input → output processing
* 🗂️ Organized project structure
* 🔄 Easy to extend with new features

---

## 🛠️ Tech Stack

* **Language:** Python
* **Frontend:** Tkinter / HTML-CSS (if Flask)
* **Backend:** Python
* **Database:** SQLite (if used)
* **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
ExplainAI/
│
├── main.py              # Main application entry point
├── requirements.txt    # Dependencies
├── README.md           # Project documentation
├── .gitignore          # Ignored files
│
├── assets/             # Images / screenshots
├── src/                # Core logic (if added)
```

---

## ▶️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/jroshani281/ExplainAI.git
cd ExplainAI
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Cutoff data (CSV or GitHub PDFs)

- **CAP cutoff PDFs** (e.g. from [jroshani281/data-](https://github.com/jroshani281/data-)): clone that repo, then from the `backend` folder run:

  ```bash
  python import_cap_pdfs.py --pdf-dir "C:\path\to\data-" --replace-years 2025 2024
  ```

  Useful files there: `*ENGG_CAP*_CutOff*.pdf`, `CAP_Round_*_2025_2026.pdf`, `*_round*.pdf`.  
  Seat matrix and merit-list PDFs are **skipped** (different format; not used by the predictor).

- **Legacy**: `import_csv.py` / `import_2025_fixed.py` target **PostgreSQL**; prefer `import_cap_pdfs.py` for the default SQLite app.

### 4️⃣ Run the Application

```bash
cd backend
python app.py
```

Open the frontend (`index.html` via Live Server or `python -m http.server` from the project root). Set `DATABASE_URL` if you use PostgreSQL; otherwise SQLite is created under `backend/instance/`.

---




---

## 👩‍💻 Author

**Roshnai**

---

## ⭐ Support

If you find this project useful, consider giving it a star ⭐ on GitHub.
