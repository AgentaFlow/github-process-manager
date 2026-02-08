# Local AI RAG Chatbot - Claude Development Guide

## Project Overview

This is a lightweight, local AI-powered chatbot that combines Retrieval-Augmented Generation (RAG) with Google's Gemini API and GitHub repository integration. Built with Python and Flask, it provides a browser-based interface for intelligent document-aware conversations.

## Architecture

### Technology Stack
- **Backend**: Python 3.8+ with Flask
- **AI/ML**: Google Gemini API (gemini-pro, embedding-001)
- **Vector Database**: ChromaDB (local persistence)
- **GitHub Integration**: PyGithub
- **Document Processing**: python-docx, PyPDF2
- **Frontend**: HTML, CSS, JavaScript (vanilla)

### Core Components

1. **app.py** - Flask application with REST API endpoints
2. **rag_engine.py** - Document processing and vector retrieval using ChromaDB
3. **gemini_client.py** - Gemini API integration for chat responses
4. **github_client.py** - GitHub API client for repository data
5. **config.py** - Centralized configuration and validation
6. **logger.py** - Application logging with rotation

## Key Features

- 📚 **RAG Document Processing**: Upload .txt, .pdf, .docx files for knowledge base
- 🤖 **Gemini AI Integration**: Context-aware responses using Gemini Pro
- 🔗 **GitHub Integration**: Access PRs, issues, workflows, and repository files
- ⚡ **GitHub Actions**: Manually trigger workflows from the UI
- 🎨 **Clean UI**: Light blue/white professional interface
- 🔒 **Secure**: Environment-based configuration with .env

## Development Notes

### Environment Setup
```bash
# Virtual environment is at .venv (not venv)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configuration
# Copy .env.template to .env and add:
# - GEMINI_API_KEY (required)
# - GITHUB_TOKEN (optional)
# - GITHUB_REPO_URL (optional)
```

### Running the Application
```bash
# Quick start (automated)
.\start.ps1

# Manual start
python app.py
# Access at http://localhost:5000
```

### Project Structure
```
Feb6DEMObot/
├── .venv/                  # Virtual environment
├── app.py                  # Main Flask application
├── config.py               # Configuration management
├── logger.py               # Logging setup
├── rag_engine.py           # RAG/ChromaDB engine
├── gemini_client.py        # Gemini API client
├── github_client.py        # GitHub API client
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .env.template           # Template for .env
├── start.ps1               # PowerShell startup script
├── start.bat               # Batch launcher
├── templates/              # Jinja2 templates
│   ├── base.html
│   ├── index.html          # Chat interface
│   └── settings.html       # Settings & GitHub Actions
├── static/
│   └── css/
│       └── style.css       # Application styling
├── chroma_db/              # ChromaDB storage (auto-created)
├── uploads/                # Temporary uploads (auto-created)
└── app.log                 # Application logs
```

## API Endpoints

### Chat
- `POST /api/chat` - Send query, get AI response with RAG context

### Document Management
- `POST /api/upload` - Upload document for RAG processing
- `GET /api/rag/stats` - Get RAG database statistics
- `POST /api/rag/clear` - Clear all RAG documents

### GitHub Integration
- `POST /api/github/connect` - Connect to repository
- `GET /api/github/info` - Get repository metadata
- `GET /api/github/workflows` - List available workflows
- `POST /api/github/workflow/trigger` - Trigger workflow manually
- `GET /api/github/pulls` - Get pull requests
- `GET /api/github/issues` - Get issues

### System
- `GET /health` - Health check and system status

## Configuration Options

Key settings in `config.py`:
- `CHUNK_SIZE`: 800 characters per document chunk
- `CHUNK_OVERLAP`: 200 characters overlap between chunks
- `TOP_K_RESULTS`: 3 RAG chunks retrieved per query
- `GEMINI_MODEL`: gemini-pro
- `TEMPERATURE`: 0.7
- `MAX_OUTPUT_TOKENS`: 2048

## RAG Processing Flow

1. **Document Upload** → Extract text (.txt, .pdf, .docx)
2. **Chunking** → Split into 800-char chunks with 200-char overlap
3. **Embedding** → Generate vectors using Gemini Embedding API
4. **Storage** → Store in ChromaDB with metadata
5. **Retrieval** → Query ChromaDB for top-K relevant chunks
6. **Response** → Combine RAG context + GitHub data + user query → Gemini

## GitHub Integration

### Supported Operations
- Repository metadata (stars, forks, language)
- Pull requests (list, search, filter by state)
- Issues (list, search, filter by state)
- Workflow runs (status, conclusion)
- Repository files (browse, read)
- Manual workflow triggers (via `create_workflow_dispatch`)

### Required Permissions
GitHub token needs:
- `repo` - Full repository access
- `workflow` - Trigger GitHub Actions

## Common Development Tasks

### Adding a New Route
1. Define route handler in `app.py`
2. Add error handling with try/except
3. Log operations using `logger.info()` / `logger.error()`
4. Return JSON responses

### Modifying RAG Behavior
- Edit `rag_engine.py`
- Adjust `CHUNK_SIZE`, `CHUNK_OVERLAP` in `config.py`
- Change `TOP_K_RESULTS` for more/fewer context chunks

### Updating UI
- Templates: `templates/*.html`
- Styles: `static/css/style.css`
- Theme colors in CSS `:root` variables

### Adding Document Formats
1. Add extension to `ALLOWED_EXTENSIONS` in `config.py`
2. Implement text extraction in `rag_engine.py:extract_text()`
3. Install any required libraries

## Troubleshooting

### Common Issues

**"GEMINI_API_KEY is not set"**
- Create `.env` from `.env.template`
- Add valid Gemini API key

**ChromaDB errors**
- Delete `chroma_db/` directory
- Restart application

**GitHub connection fails**
- Verify token has `repo` and `workflow` scopes
- Check repository URL format
- Ensure token hasn't expired

**Import errors**
- Activate virtual environment: `.venv\Scripts\Activate.ps1`
- Reinstall dependencies: `pip install -r requirements.txt`

### Logs
Check `app.log` for detailed error messages and stack traces.

## Performance Considerations

- **Lightweight Design**: No GPU required, runs on CPU
- **ChromaDB**: Local vector database, no external service needed
- **Chunking Strategy**: Efficient 800-char chunks balance context and speed
- **Caching**: ChromaDB automatically caches embeddings
- **Resource Usage**: ~200-500MB RAM typical usage

## Security Notes

- `.env` file is gitignored - never commit API keys
- Session secrets managed via `FLASK_SECRET_KEY`
- File uploads limited to 16MB
- Allowed file extensions whitelist (.txt, .pdf, .docx)
- GitHub token permissions should be minimal (repo + workflow only)

## Future Enhancements (Ideas)

- [ ] Session-based chat history
- [ ] Export conversations to PDF
- [ ] Markdown rendering in chat responses
- [ ] Multiple RAG collections (project-based)
- [ ] Real-time GitHub webhook integration
- [ ] Docker containerization
- [ ] Authentication/multi-user support
- [ ] Streaming responses from Gemini
- [ ] Code syntax highlighting in responses

## Links & Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Last Updated**: February 4, 2026  
**Python Version**: 3.8+  
**Status**: ✅ Fully Implemented & Ready for Use