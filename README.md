```markdown
# 🧠 CapillaryTech Documentation Chatbot

The **CapillaryTech Documentation Chatbot** is a **Flask-based web application** that intelligently answers queries related to **CapillaryTech APIs and documentation**. It uses **FAISS** for fast semantic retrieval from scraped documentation and integrates with the **OpenRouter API** to generate concise, natural-language responses in **2–3 bullet points**. The chatbot provides accurate, context-aware answers directly from CapillaryTech documentation and handles unrelated queries gracefully.

---

## 🚀 Features
- 🔍 **Semantic Search with FAISS:** Retrieves top relevant documentation results based on query embeddings.  
- 🧩 **Scraped Local Data:** Uses pre-scraped and indexed CapillaryTech documentation stored locally for accuracy.  
- 🧠 **OpenRouter LLM Integration:** Summarizes responses into 2–3 clear, human-like bullet points.  
- ⚙️ **Flask Backend:** Lightweight and efficient REST API with clean structure.  
- 💬 **TailwindCSS Chat UI:** Modern, responsive, and user-friendly interface for interaction.  
- 🧾 **Debug Logging:** Shows query sources and embedding search logs in the backend console for transparency.  

---

## 🗂️ Project Structure
```

capillery/
├── app.py
├── scraper.py
├── rebuild_index.py
├── data/
│   └── faiss_index/
│       ├── index.faiss
│       └── metadata.json
├── templates/
│   └── index.html
├── requirements.txt
└── venv/

````

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/capillarytech-chatbot.git
cd capillarytech-chatbot
````

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Scrape Documentation

This step collects the CapillaryTech documentation and saves it as a JSONL file.

```bash
python scraper.py
```

### 5️⃣ Build the FAISS Index

Convert the scraped data into vector embeddings and store it in `data/faiss_index/`.

```bash
python rebuild_index.py
```

### 6️⃣ Set Your OpenRouter API Key

```bash
setx OPENROUTER_API_KEY "your_openrouter_api_key"
```

*(Restart your terminal after setting the key.)*

### 7️⃣ Run the Flask Application

```bash
python app.py
```

The app will start at:
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 💬 Usage

1. Open the chatbot in your browser.
2. Type your question (e.g., **“How to get user activity logs?”**) in the input box.
3. The chatbot retrieves top sources from CapillaryTech documentation and returns a summarized, bullet-point answer.
4. Off-topic or unrelated questions (like job or company info) are handled gracefully with fallback responses.

---

## 📊 Example Interaction

**User:**

> Where to get user activity logs?

**Chatbot Response:**

* You can access activity logs via **Member Care → Customer Overview** for basic details.
* For behavioral events (e.g., app usage or cart abandonment), go to **Events → Behavioral Events**.
* Use the **Customer Activity History API** for programmatic access to user logs.

---

## 🧱 Technologies Used

| Component       | Technology                                 |
| --------------- | ------------------------------------------ |
| Backend         | Flask (Python)                             |
| Vector Search   | FAISS                                      |
| Embeddings      | Sentence Transformers (`all-MiniLM-L6-v2`) |
| LLM Integration | OpenRouter API (GPT-4o-mini)               |
| Frontend        | HTML + Tailwind CSS                        |
| Data Source     | Scraped CapillaryTech Documentation        |

---

## 🧪 Debugging

* If the page is blank, ensure `index.html` is located in the `templates/` directory.
* Check that `data/faiss_index/index.faiss` and `metadata.json` exist.
* Run in debug mode:

  ```bash
  flask --app app run --debug
  ```
* Console logs will show:

  * Queries received
  * FAISS search results
  * Sources retrieved
  * Any API call errors

---

## 📹 Demo

🎥 A 1-minute demo video showcasing the chatbot’s functionality and CapillaryTech documentation responses is available here:
🔗 **[Google Drive Demo Video Link](https://drive.google.com/)**

---

## 📚 Project Summary

The CapillaryTech Documentation Chatbot demonstrates how **retrieval-augmented generation (RAG)** can be effectively implemented for real-world enterprise documentation. By combining **local semantic search** with **LLM summarization**, it ensures both **accuracy** and **clarity** — making it a reliable assistant for CapillaryTech API users and developers.

---

## 🏆 Evaluation Highlights

| Criteria           | Description                                               |
| ------------------ | --------------------------------------------------------- |
| **Efficiency**     | Retrieves precise answers with minimal latency            |
| **Accuracy**       | Responses grounded in scraped CapillaryTech documentation |
| **Code Quality**   | Clean, modular, and well-commented Python and HTML code   |
| **User Interface** | Responsive, modern, and intuitive                         |
| **Error Handling** | Manages empty queries and API failures gracefully         |

---

## 👨‍💻 Author

**Developed by:** Yogesh Yadav
📍 India
💻 Passionate about AI, LLMs, and Intelligent Automation Systems

```
```
