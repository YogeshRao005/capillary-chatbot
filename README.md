CapillaryTech Documentation Chatbot
A Flask-based chatbot that answers queries using pre-scraped CapillaryTech documentation. It leverages a FAISS index for efficient document retrieval and the OpenRouter API to generate concise, text-based responses without external links, ensuring accuracy and relevance.
Features

Queries a FAISS index of CapillaryTech documentation for relevant content.
Scrapes and cleans content from metadata URLs for context.
Generates brief, bullet-point answers (2-3 points) using OpenRouter API.
User-friendly web interface built with HTML and Tailwind CSS.
Handles off-topic queries with appropriate text fallbacks.

Project Structure
capillarytech-chatbot/
├── data/
│   └── faiss_index/
│       ├── index.faiss
│       └── metadata.json
├── templates/
│   └── index.html
├── app.py
├── requirements.txt
└── README.md

Setup

Clone the Repository:git clone https://github.com/[your-username]/capillarytech-chatbot.git
cd capillarytech-chatbot


Install Dependencies:Ensure Python 3.8+ is installed, then run:pip install -r requirements.txt

Contents of requirements.txt:flask==2.3.2
sentence-transformers==2.2.2
faiss-cpu==1.7.4
numpy==1.24.3
requests==2.31.0
beautifulsoup4==4.12.2


Prepare Data:
Ensure data/faiss_index/index.faiss and metadata.json exist, containing pre-scraped CapillaryTech documentation embeddings and metadata (URLs and titles).
Verify the FAISS index aligns with metadata.json to avoid incorrect data retrieval.


Run the Application:python app.py

Open http://localhost:5000 in a browser.

Usage

Web Interface:
Access the chatbot at http://localhost:5000.
Enter queries about CapillaryTech APIs or documentation (e.g., "What are path parameters?", "How to authenticate?").
Receive brief, text-based answers in 2-3 bullet points without links.


Example Queries and Responses:
Query: "What are path parameters?"
Answer: - Path parameters are URL variables like {userId}.
- They identify resources in API calls.




Query: "How to authenticate?"
Answer: - Use API keys in Authorization header.
- Bearer <token> format.




Query: "What is the salary?"
Answer: - Check official careers page for job-related queries.






Debugging:
Check terminal logs for scraped content (Scraped <url>: ...) and context (Context for ...) to ensure data is sourced correctly.
Verify the OpenRouter API key is valid and has sufficient quota.



Dependencies

Python 3.8+
Flask==2.3.2
sentence-transformers==2.2.2
faiss-cpu==1.7.4
numpy==1.24.3
requests==2.31.0
beautifulsoup4==4.12.2

Notes

The chatbot uses only pre-scraped data from data/faiss_index/ to ensure accurate responses.
Responses are generated without external links, focusing on concise explanations.
Off-topic queries (e.g., job-related) are handled with appropriate text fallbacks.

Demo
A 1-minute demo video showcasing the chatbot’s functionality is available at: [Google Drive link] (to be updated after recording).
Troubleshooting

Incorrect Answers: Verify index.faiss and metadata.json are aligned and contain relevant CapillaryTech documentation.
API Errors: Ensure the OpenRouter API key is active. Check terminal logs for error details.
Scraping Issues: Confirm URLs in metadata.json are accessible and return valid content.

Submission Details

Repository: https://github.com/YogeshRao005/capillary-chatbot


License
MIT License