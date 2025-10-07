"""
CapillaryTech Documentation Chatbot
===================================
A Flask-based chatbot that queries a pre-built FAISS index of CapillaryTech docs,
fetches and processes content from top sources, and uses OpenRouter API to generate
structured text responses. Updated to prioritize concise, accurate text solutions.

Author: [Your Name]
Date: October 08, 2025

Usage:
    1. Ensure data/faiss_index/index.faiss and metadata.json exist.
    2. pip install -r requirements.txt
    3. python app.py
    4. Open http://localhost:5000

Dependencies (requirements.txt):
    flask==2.3.2
    sentence-transformers==2.2.2
    faiss-cpu==1.7.4
    numpy==1.24.3
    requests==2.31.0
    beautifulsoup4==4.12.2
"""

import os
import json
import re
from flask import Flask, request, jsonify, render_template
import numpy as np
import faiss
import requests
from bs4 import BeautifulSoup

INDEX_DIR = "data/faiss_index"
INDEX_FILE = os.path.join(INDEX_DIR, "index.faiss")
META_FILE = os.path.join(INDEX_DIR, "metadata.json")

app = Flask(__name__)

# Fail fast if index or metadata is missing
if not os.path.exists(INDEX_FILE) or not os.path.exists(META_FILE):
    raise SystemExit(f"ERROR: {INDEX_FILE} or {META_FILE} not found. Build the index first.")

# Load FAISS index and metadata
index = faiss.read_index(INDEX_FILE)
with open(META_FILE, "r", encoding="utf-8") as f:
    meta = json.load(f)  # Expecting {"urls": [...], "titles": [...]}

# Lazy load SentenceTransformer for query embedding
EMBED_MODEL = None
def embed_query(query):
    """Embed a query using SentenceTransformer."""
    global EMBED_MODEL
    if EMBED_MODEL is None:
        from sentence_transformers import SentenceTransformer
        EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    vec = EMBED_MODEL.encode([query], convert_to_numpy=True)
    return np.array(vec, dtype=np.float32)

def clean_content(text):
    """Clean scraped text by removing excessive whitespace and irrelevant content."""
    if not text:
        return ""
    # Remove multiple spaces, newlines, and tabs
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove boilerplate phrases (e.g., navigation text)
    boilerplate = ["skip to content", "back to top", "all rights reserved"]
    for phrase in boilerplate:
        text = text.replace(phrase, "")
    return text[:1000]  # Limit to 1000 chars for API compatibility

def scrape_content(url):
    """Scrape and clean text content from a given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove irrelevant elements (scripts, styles, navigation, footer)
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        # Prioritize main content areas
        content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile('content|body'))
        if not content:
            content = soup.body
        
        text = content.get_text(separator=' ', strip=True)
        return clean_content(text)
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def call_openrouter(query, context):
    """Generate a response using OpenRouter API with cleaned context and fallback."""
    api_key = "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"
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "CapillaryChatbot",
    }
    
    # Immediate fallback for HR-related or off-topic queries
    if any(term in query.lower() for term in ["join", "package", "salary", "hire", "career"]):
        return ("This query relates to employment at CapillaryTech. "
                "For details on careers, visit the official CapillaryTech careers page.")

    # Fallback if no context or query is unrelated to documentation
    if not context or all(term not in context.lower() for term in ["api", "request", "parameter", "loyalty", "documentation"]):
        return ("This query does not match CapillaryTech documentation content. "
                "Please ask about APIs, parameters, or product usage for a detailed response.")

    # Chunk context to fit within token limits (approx. 500 tokens ~ 2000 chars)
    context_chunks = [context[i:i+1500] for i in range(0, len(context), 1500)]
    context = context_chunks[0]  # Use first chunk for brevity

    # Refined prompt for structured, concise responses
    prompt = (
        f"Answer the query '{query}' using only the provided CapillaryTech documentation context. "
        "Return a concise, structured response with numbered points (e.g., 1. Step..., 2. Step...). "
        "If the context lacks specific details, provide a general explanation based on the context. "
        f"Context: {context}"
    )
    
    models_to_try = ["google/gemma-2-9b-it:free", "meta-llama/llama-4-maverick:free"]
    
    for model in models_to_try:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,  # Reduced for concise responses
            "temperature": 0.7  # Balanced creativity
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=5)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error with model {model}: {e}")
            continue
    
    # Enhanced fallback with summarized context
    lines = context.split(' ')
    summary = [f"{i+1}. {line.strip()[:50]}..." for i, line in enumerate(lines[:3]) if line.strip()]
    fallback = "Based on CapillaryTech documentation:\n" + "\n".join(summary) if summary else ""
    
    # Add general API explanation for specific query types
    if "path parameter" in query.lower() or "request path" in query.lower():
        fallback += (
            "\n\nIn CapillaryTech APIs, path parameters are variables in the URL path "
            "(e.g., /v2/customers/{userId}) that identify specific resources. "
            "They are required and must match the expected format (e.g., numeric ID)."
        )
    elif "authentication" in query.lower():
        fallback += (
            "\n\nCapillaryTech APIs typically use API keys or OAuth tokens for authentication. "
            "Include the key in the Authorization header (e.g., Bearer <token>). "
            "Check the specific API documentation for setup details."
        )

    return fallback if fallback else "No specific details found in the documentation."

def generate_response(query, top_urls, top_titles):
    """Generate a text response based on scraped documentation content."""
    if not top_urls:
        return "No relevant documentation found. Try rephrasing your query."

    # Scrape and clean content from top URLs
    scraped_contents = [scrape_content(url) for url in top_urls]
    context = "\n".join([f"{title}: {content}" for title, content in zip(top_titles, scraped_contents) if content])
    
    # Log context for debugging (truncated for readability)
    print(f"Context for '{query}': {context[:500]}...")
    
    return call_openrouter(query, context)

@app.route("/")
def homepage():
    """Render the chatbot's front-end interface."""
    try:
        return render_template("index.html")
    except Exception as e:
        print(f"Error rendering homepage: {e}")
        return "Error loading the chatbot interface.", 500

@app.route("/ask", methods=["POST"])
def ask():
    """Handle user queries and return structured responses."""
    try:
        body = request.json or {}
        query = body.get("question", "").strip()
        if not query:
            return jsonify({"answer": "Please provide a question."}), 400

        # Embed query and search FAISS index
        query_vector = embed_query(query)
        top_k = int(os.getenv("TOP_K", 3))
        distances, indices = index.search(query_vector, top_k)

        # Collect top sources
        top_urls = []
        top_titles = []
        for idx in indices[0]:
            if idx >= 0 and idx < len(meta["urls"]):
                top_urls.append(meta["urls"][idx])
                top_titles.append(meta["titles"][idx])

        # Generate text response
        answer = generate_response(query, top_urls, top_titles)
        sources = [{"title": title, "url": url} for title, url in zip(top_titles, top_urls)]

        return jsonify({"answer": answer, "sources": sources})

    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({"answer": "Unable to process your request. Please try again."}), 500

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5000))
    app.run(host=host, port=port, debug=True)