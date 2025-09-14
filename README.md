# 📂 AI Document Analyzer

An AI-powered system that *classifies, summarizes, and searches documents* with *role-based access control*.  
Built for hackathons to showcase how *AI + Streamlit + MySQL* can solve real-world document management problems.  

---

## ✨ Features

✅ Upload PDF, DOCX, TXT files  
✅ Automatic AI classification (Finance, HR, Legal, etc.)  
✅ AI-powered summarization (short overview of document)  
✅ Keyword-based search with ranked results  
✅ Role-based access (HR only sees HR docs, Finance only sees Finance docs, etc.)  
✅ Clean multi-page Streamlit dashboard (Login → Upload → Search)  
✅ MySQL database integration for users & documents  

---

## 🛠 Tech Stack

- *Python 3.11*  
- *Streamlit* (frontend + dashboard)  
- *Hugging Face Transformers* (classification + summarization)  
- *PyTorch* (model backend)  
- *MySQL (XAMPP)* (users, documents storage)  
- *PyPDF2 / python-docx* (text extraction)  

---

## ⚡ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/AI-Document-Analyzer.git
cd AI-Document-Analyzer
```

### 2. Install dependencies

```bash
py -3.11 -m pip install -r requirements.txt
```

### 3. Setup MySQL database

- Open phpMyAdmin (XAMPP) or MySQL Workbench
- Run the queries in schema.sql
- This creates doc_ai DB, tables, and demo users

### 4. Run the app

```bash
py -3.11 -m streamlit run app.py
```
Then open: 👉 http://localhost:8501

---

## 📂 Project Structure

```bash
AI-Document-Analyzer/
│── app.py              # main Streamlit app
│── requirements.txt    # dependencies
│── schema.sql          # MySQL DB setup
│── README.md           # documentation
│── uploads/            # uploaded files (empty, auto-filled by app)
```

---

## 🚀 Demo Flow

1. Login with role-based account (Admin / HR / Finance / Legal)
2. Upload a PDF/DOCX/TXT → AI extracts text → classifies category → generates summary
3. Search for keywords or phrases → see ranked results
4. Access Control: HR only sees HR docs, Finance only sees Finance docs, etc.

---

## 🌟 Future Improvements

- Add semantic search (embeddings-based)
- Add visualization dashboard (charts of document categories)
- Add file download & export options
- Deploy to cloud (Streamlit Cloud / AWS / Heroku)
