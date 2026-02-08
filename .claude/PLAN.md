# Local AI RAG Chatbot with Gemini API Key and Connection to GitHub Repository

I need to build a local AI RAG (Retrieval-Augmented Generation) chatbot that utilizes the Gemini API key for advanced language processing capabilities. The chatbot should be able to connect to a specific GitHub repository to retrieve relevant documents and information to enhance its responses.

This chatbot should be designed to run locally on my machine. It should be lightweight, simple to set up and use minimal resources. The chatbot should be able to handle user queries, fetch relevant data from the connected GitHub repository, and generate responses using the Gemini API referring to RAG documents.

It should be easy for users to see how to upload reference documents for RAG and how to connect their own GitHub repositories. The chatbot should also include error handling for issues such as invalid API keys, connection problems with GitHub, and document retrieval failures.

## Technical Guidance 

1. **Environment Setup**:
   - Use Python as the primary programming language.
   - Set up a virtual environment to manage dependencies.
   - Install necessary libraries such as `requests` for API calls, `PyGithub` for GitHub interactions, and any Gemini API SDK if available.
   - Create a browser-based interface using `Flask` for user interaction.
   - The browser based user interface should be clear, simple, and easy to navigate. It should have a professional look and feel and the primary color scheme should be light blue and white.
    - Variables should come from a .env file for easy configuration.
    - I have a Gemini API key and a GitHub repository URL ready to use. I can get a GitHub personal access token if needed.
    - Implement error handling for missing or invalid environment variables.
    - Set up logging to track errors and important events.
    - Create a README file with setup instructions and usage guidelines.

2. **Gemini API Integration**:
   - Obtain the Gemini API key and set up authentication.
    - Create functions to send user queries to the Gemini API and receive responses.
3. **GitHub Repository Connection**:
   - Use the `PyGithub` library to authenticate and connect to the specified GitHub repository
    - Implement functions to fetch pull requests, actions, artifacts, and files from the repository based on user queries.

## Important Considerations

The user must be able to chat through the chatbot in the browser interface.
The user must be able to upload reference documents for RAG.
The user must be able to connect their own GitHub repositories.
Most importantly, the chatbot must use minimal resources and be lightweight to run locally, take the RAG documents into account, and generate accurate responses using the Gemini API with connected GitHub repository data.
Ideally I would like have specific GitHub Actions that can communicate with the chatbot for specific tasks.

## Building Plan

Local AI RAG Chatbot with Gemini & GitHub Integration
Build a lightweight Flask-based chatbot that runs locally, integrating ChromaDB for RAG document retrieval with Gemini API responses, and connects to GitHub repositories for contextual data. The system will feature a browser interface with document upload (.txt, .docx, .pdf), repository connection, manual GitHub Actions triggers, and chat capabilities.

Steps
Set up Python environment and dependencies — Create virtual environment, requirements.txt with Flask, google-generativeai, PyGithub, chromadb, python-dotenv, python-docx, PyPDF2, and .env.template for GEMINI_API_KEY, GITHUB_TOKEN, GITHUB_REPO_URL with .gitignore to protect secrets.

Build Flask application structure — Create app.py with routes (/, /chat, /upload, /settings, /github-actions), static/css/style.css with light blue/white theme, templates/ folder with base.html, index.html, settings.html, and initialize logger.py for error tracking.

Implement RAG engine with ChromaDB — Build rag_engine.py to process uploads (.txt, .docx, .pdf), extract text with python-docx and PyPDF2, chunk documents (500-1000 tokens), generate embeddings via Gemini Embedding API, store in ChromaDB local persistence, and retrieve top-k relevant chunks for queries.

Create Gemini API integration — Develop gemini_client.py with authentication, generate_response() function that combines user query + RAG context + GitHub data, streaming response support for better UX, error handling for rate limits/invalid keys, and configuration for model parameters (temperature, max_tokens).

Build GitHub integration module — Implement github_client.py using PyGithub to authenticate, fetch repository metadata, list/search PRs and issues, retrieve workflow runs and artifacts, access repository files, and expose manual trigger interface for GitHub Actions workflows.

Add configuration and documentation — Write comprehensive README.md with prerequisites, setup steps (virtual env, API keys, GitHub token), usage instructions, document upload guide, troubleshooting section, and create config.py to validate environment variables with helpful error messages.

Implementation Notes
ChromaDB persistence: Store vector database in ./chroma_db/ directory for fast local retrieval
Manual GitHub Actions triggers: UI button to manually trigger workflows via PyGithub's create_workflow_dispatch()
Document processing: Use python-docx for .docx, PyPDF2 for .pdf, direct read for .txt
Lightweight design: No GPU requirements, minimal dependencies, efficient chunking strategy
Error handling: Try-except blocks around all API calls with user-friendly error messages logged to app.log

## Implemented

🎯 Key Features Implemented
✅ RAG document processing (.txt, .pdf, .docx)
✅ ChromaDB vector storage with Gemini embeddings
✅ Gemini API chat integration with context
✅ GitHub repository connection
✅ Pull requests, issues, and workflow data
✅ Manual GitHub Actions triggers
✅ Browser-based UI with light blue/white theme
✅ Environment-based configuration
✅ Comprehensive error handling and logging
✅ Lightweight, local-first design

🚀 Next Steps
Set up your environment:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Configure your API keys:

Copy .env.template to .env
Add your Gemini API key
Add your GitHub token (optional)
Run the application:
python app.py

Access at: http://localhost:5000

The chatbot is ready to use! Upload documents, connect to GitHub repositories, and start chatting with your AI assistant. 🎉

## Personal Repository update

I have downloaded this codebase into my personal repository and have made some updates to the README.md file to include more detailed instructions on how to use the chatbot, as well as a more comprehensive project structure and configuration options. I have also added a section on the implemented features and next steps for users to get started with the chatbot.

Things to update: 
Remove all KPMG branding and mentions of KPMG
