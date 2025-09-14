import os
import streamlit as st
import mysql.connector
from transformers import pipeline
import PyPDF2
import docx

# ----------------------------
# Database connection
# ----------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",     # change if needed
        password="",     # add password if set
        database="doc_ai"
    )

# ----------------------------
# AI Pipelines (Lightweight with fallback)
# ----------------------------
try:
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception:
    classifier = None
    summarizer = None

# ----------------------------
# Text Extraction
# ----------------------------
def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for i, page in enumerate(reader.pages[:3]):  # first 3 pages only
                text += page.extract_text() or ""
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    return text.strip()

# ----------------------------
# Authentication
# ----------------------------
def login_user(username, password):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return user

# ----------------------------
# App
# ----------------------------
st.set_page_config(page_title="AI Document Analyzer", layout="wide")

if "user" not in st.session_state:
    st.session_state.user = None

# ----------------------------
# Login Page
# ----------------------------
if not st.session_state.user:
    st.title("🔐 AI Document Analyzer - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.user = user
            st.success(f"Welcome {user['username']} ({user['role']}) 🎉")
            st.rerun()   # ✅ fixed
        else:
            st.error("❌ Invalid credentials")

# ----------------------------
# Logged-in Pages
# ----------------------------
else:
    st.sidebar.title("📂 Navigation")
    page = st.sidebar.radio("Go to", ["Upload Document", "Search Documents", "My Documents", "Logout"])

    # Upload Page
    if page == "Upload Document":
        st.title("📤 Upload a Document")

        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])
        if uploaded_file:
            os.makedirs("uploads", exist_ok=True)
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            text = extract_text(file_path)
            preview = text[:1000]

            st.subheader("🔎 Preview")
            st.text_area("Extracted Text", preview, height=200)

            # Metadata
            title = st.text_input("Title", uploaded_file.name)
            author = st.text_input("Author", "Unknown")
            doc_date = st.text_input("Date", "2025-09-13")

            # Classification
            categories = ["Finance", "HR", "Legal", "Contracts", "Technical Reports"]
            top_category = "Uncategorized"
            if classifier:
                try:
                    result = classifier(preview[:400], candidate_labels=categories)
                    top_category = result["labels"][0]
                except:
                    pass

            # Summarization
            summary = preview[:200] + "..."
            if summarizer:
                try:
                    summary = summarizer(preview[:400], max_length=80, min_length=25, do_sample=False)[0]["summary_text"]
                except:
                    pass

            st.write(f"*Category:* {top_category}")
            st.write(f"*Summary:* {summary}")

            if st.button("Save to Database"):
                db = get_db()
                cursor = db.cursor()
                cursor.execute("""
                    INSERT INTO documents (filename, title, author, doc_date, category, summary, role, filepath)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    uploaded_file.name,
                    title,
                    author,
                    doc_date,
                    top_category,
                    summary,
                    st.session_state.user['role'],
                    file_path
                ))
                db.commit()
                cursor.close()
                db.close()
                st.success("✅ Document saved to database!")

    # Search Page
    elif page == "Search Documents":
        st.title("🔍 Search Documents")
        query = st.text_input("Enter keyword or phrase")
        if query:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM documents WHERE summary LIKE %s OR title LIKE %s OR category LIKE %s",
                (f"%{query}%", f"%{query}%", f"%{query}%")
            )
            results = cursor.fetchall()
            cursor.close()
            db.close()

            if results:
                for doc in results:
                    with st.expander(f"{doc['title']} ({doc['category']})"):
                        st.write(f"*Author:* {doc['author']}")
                        st.write(f"*Date:* {doc['doc_date']}")
                        st.write(f"*Summary:* {doc['summary']}")
            else:
                st.warning("No documents found.")

    # My Documents Page
    elif page == "My Documents":
        st.title("📂 My Documents")
        role = st.session_state.user["role"]
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM documents WHERE role=%s", (role,))
        docs = cursor.fetchall()
        cursor.close()
        db.close()

        if docs:
            for doc in docs:
                with st.expander(f"{doc['title']} ({doc['category']})"):
                    st.write(f"*Author:* {doc['author']}")
                    st.write(f"*Date:* {doc['doc_date']}")
                    st.write(f"*Summary:* {doc['summary']}")
        else:
            st.info("No documents uploaded under your role.")

    # Logout Page
    elif page == "Logout":
        st.session_state.user = None
        st.success("✅ Logged out!")
        st.rerun()   # ✅ fixed
