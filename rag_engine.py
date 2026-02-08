"""
RAG (Retrieval-Augmented Generation) Engine using ChromaDB.
Handles document processing, embedding generation, and context retrieval.
"""
import os
import chromadb
from chromadb.config import Settings
import google.generativeai as genai
from docx import Document
from PyPDF2 import PdfReader
from logger import logger
from config import Config

class RAGEngine:
    """RAG engine for document processing and retrieval."""
    
    def __init__(self):
        """Initialize the RAG engine with ChromaDB and Gemini embeddings."""
        try:
            # Initialize ChromaDB
            self.client = chromadb.PersistentClient(
                path=Config.CHROMA_DB_PATH,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="rag_documents",
                metadata={"description": "RAG document embeddings"}
            )
            
            # Configure Gemini for embeddings
            genai.configure(api_key=Config.GEMINI_API_KEY)
            
            logger.info("RAG Engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG Engine: {e}")
            raise
    
    def extract_text(self, file_path, file_type):
        """
        Extract text content from uploaded file.
        
        Args:
            file_path: Path to the file
            file_type: File extension (txt, pdf, docx)
        
        Returns:
            Extracted text content
        """
        try:
            if file_type == 'txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif file_type == 'pdf':
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
            
            elif file_type == 'docx':
                doc = Document(file_path)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text
            
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            raise
    
    def chunk_text(self, text, chunk_size=None, overlap=None):
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            chunk_size: Maximum characters per chunk
            overlap: Number of overlapping characters
        
        Returns:
            List of text chunks
        """
        chunk_size = chunk_size or Config.CHUNK_SIZE
        overlap = overlap or Config.CHUNK_OVERLAP
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence or word boundary
            if end < text_length:
                # Look for sentence end
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size * 0.5:  # Only if we're past halfway
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return [c for c in chunks if c]  # Filter empty chunks
    
    def generate_embedding(self, text):
        """
        Generate embedding for text using Gemini.
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding vector
        """
        try:
            result = genai.embed_content(
                model=Config.GEMINI_EMBEDDING_MODEL,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def add_document(self, file_path, filename):
        """
        Process and add document to ChromaDB.
        
        Args:
            file_path: Path to the uploaded file
            filename: Original filename
        
        Returns:
            Number of chunks added
        """
        try:
            # Extract file type
            file_type = filename.rsplit('.', 1)[1].lower()
            
            # Extract text
            logger.info(f"Extracting text from {filename}")
            text = self.extract_text(file_path, file_type)
            
            if not text.strip():
                raise ValueError("No text content found in document")
            
            # Chunk text
            logger.info(f"Chunking document {filename}")
            chunks = self.chunk_text(text)
            logger.info(f"Created {len(chunks)} chunks from {filename}")
            
            # Generate embeddings and add to ChromaDB
            documents = []
            metadatas = []
            ids = []
            embeddings = []
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{filename}_chunk_{i}"
                
                # Generate embedding
                embedding = self.generate_embedding(chunk)
                
                documents.append(chunk)
                metadatas.append({
                    "filename": filename,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                })
                ids.append(chunk_id)
                embeddings.append(embedding)
            
            # Add to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings
            )
            
            logger.info(f"Successfully added {len(chunks)} chunks from {filename} to RAG database")
            return len(chunks)
            
        except Exception as e:
            logger.error(f"Error adding document {filename}: {e}")
            raise
    
    def retrieve_context(self, query, top_k=None):
        """
        Retrieve relevant context for a query.
        
        Args:
            query: User query
            top_k: Number of results to retrieve
        
        Returns:
            List of relevant text chunks with metadata
        """
        try:
            top_k = top_k or Config.TOP_K_RESULTS
            
            # Generate query embedding
            query_embedding = genai.embed_content(
                model=Config.GEMINI_EMBEDDING_MODEL,
                content=query,
                task_type="retrieval_query"
            )['embedding']
            
            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            # Format results
            context_chunks = []
            if results and results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                    context_chunks.append({
                        'text': doc,
                        'metadata': metadata,
                        'distance': results['distances'][0][i] if results['distances'] else None
                    })
            
            logger.info(f"Retrieved {len(context_chunks)} context chunks for query")
            return context_chunks
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []
    
    def get_stats(self):
        """Get statistics about the RAG database."""
        try:
            count = self.collection.count()
            return {
                'total_chunks': count,
                'collection_name': self.collection.name
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {'total_chunks': 0}
    
    def clear_database(self):
        """Clear all documents from the RAG database."""
        try:
            # Delete and recreate collection
            self.client.delete_collection("rag_documents")
            self.collection = self.client.get_or_create_collection(
                name="rag_documents",
                metadata={"description": "RAG document embeddings"}
            )
            logger.info("RAG database cleared successfully")
            return True
        except Exception as e:
            logger.error(f"Error clearing database: {e}")
            return False
