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
