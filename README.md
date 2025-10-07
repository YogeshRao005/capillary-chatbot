# CapillaryTech Documentation Chatbot

The **CapillaryTech Documentation Chatbot** is a Flask-based AI application that provides instant answers to queries related to **CapillaryTech APIs and documentation**. It uses **retrieval-augmented generation (RAG)** to combine the speed of vector search with the clarity of AI-generated summaries.

---

## 🧠 Overview

This chatbot efficiently retrieves information from CapillaryTech’s developer documentation using a **FAISS vector index**. It embeds text data using **Sentence Transformers**, searches semantically similar content for any user query, and generates concise responses using the **OpenRouter API**. The system ensures accuracy by relying entirely on locally scraped documentation data.

---

## ⚙️ Key Features

- **Flask Backend** for lightweight web serving  
- **FAISS Vector Index** for fast similarity search  
- **Sentence Transformers** for embedding generation  
- **OpenRouter Integration** for AI-powered summaries  
- **Tailwind CSS Interface** for a modern and responsive UI  
- **Debug Logging** for content verification and performance tracking  
- **Offline Retrieval** from pre-scraped local data  

---

## 🚀 How It Works

1. Documentation pages from CapillaryTech’s developer site are **scraped and stored** locally.  
2. Each document is **cleaned and embedded** using a Sentence Transformer model.  
3. All embeddings are **indexed in FAISS** for fast retrieval.  
4. The Flask server receives a **user query** and embeds it to perform a similarity search.  
5. Top results are passed to the **OpenRouter API** to generate a **concise, bullet-point answer**.  
6. The frontend displays the response and lists **relevant sources** for transparency.

---

## 🖥️ User Interface

The web interface is simple, clean, and built with **Tailwind CSS**.  
It allows users to:
- Enter questions directly in a chat-style input field  
- View structured, concise responses  
- See relevant source documentation links  

---

## 🧩 Tech Stack

- **Python 3.10+**  
- **Flask**  
- **FAISS**  
- **Sentence Transformers (all-MiniLM-L6-v2)**  
- **OpenRouter API**  
- **Tailwind CSS**  

---

## 📊 Example Output

**User Query:**  
> How to fetch user journey history in CapillaryTech?

**Response:**  
- Use the `/journey/history` API endpoint for user session tracking.  
- Include the `user_id` and date filters to narrow results.  
- Responses are returned in JSON format with session attributes.

**Sources:**  
- [Search User Journey History](https://docs.capillarytech.com/docs/search-user-journey-history)  
- [Session Logs](https://docs.capillarytech.com/docs/session_logs)

---

## 🧰 Debugging

All FAISS retrieval steps and API responses are logged for verification.  
If results appear off-topic or missing, logs help confirm which documents were retrieved and why.

---

## 📘 Summary

This project showcases a **fully functional AI documentation assistant** designed for enterprise use cases. It combines **semantic search, AI summarization, and web deployment** into one efficient tool for exploring technical documentation. The chatbot demonstrates how intelligent retrieval and local data integration can create accurate, context-aware answers for developers.
