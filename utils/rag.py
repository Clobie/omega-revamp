# utils/rag.py

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from utils.logger import Logger

class Rag:
	"""
	Singleton Retrieval-Augmented Generation backend using SentenceTransformer embeddings and ChromaDB.
	"""

	_instance = None

	def __new__(cls, *args, **kwargs):
		"""Ensure only one Rag instance is created."""
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self):
		"""Initialize embedder and persistent Chroma collection (once)."""
		if hasattr(self, "_initialized") and self._initialized:
			return

		self.logger = Logger()

		try:
			self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
		except Exception as e:
			self.logger.error(f"Error initializing SentenceTransformer: {e}")
			raise

		try:
			self.chroma = chromadb.PersistentClient(path="./rag_db", settings=Settings())
			self.collection = self.chroma.get_or_create_collection("discord_knowledge")
		except Exception as e:
			self.logger.error(f"Error initializing ChromaDB client or collection: {e}")
			raise

		self._initialized = True

	def add_document(self, text: str, doc_id=None, metadata: dict = None):
		"""Add a document with embedding and optional metadata."""
		try:
			embedding = self.embedder.encode([text])[0]
		except Exception as e:
			self.logger.error(f"Error generating embedding: {e}")
			return

		if not doc_id:
			doc_id = str(hash(text))

		full_metadata = metadata.copy() if metadata else {}
		full_metadata["id"] = doc_id

		try:
			self.collection.add(
				documents=[text],
				embeddings=[embedding.tolist()],
				ids=[doc_id],
				metadatas=[full_metadata],
			)
		except Exception as e:
			self.logger.error(f"Error adding document to collection: {e}")

	def update_document(self, doc_id: str, new_text: str, new_metadata: dict = None):
		"""Update document by ID with new text and metadata; adds if missing."""
		try:
			embedding = self.embedder.encode([new_text])[0]
		except Exception as e:
			self.logger.error(f"Error generating embedding: {e}")
			return

		try:
			self.collection.delete(ids=[doc_id])
		except Exception as e:
			self.logger.warning(f"Warning: Error deleting document with id {doc_id}: {e}")

		full_metadata = new_metadata.copy() if new_metadata else {}
		full_metadata["id"] = doc_id

		try:
			self.collection.add(
				documents=[new_text],
				embeddings=[embedding.tolist()],
				ids=[doc_id],
				metadatas=[full_metadata],
			)
		except Exception as e:
			self.logger.error(f"Error adding updated document to collection: {e}")

	def query_top_documents(self, query: str, top_k=4) -> list[str]:
		"""Return top_k most relevant documents for the query."""
		try:
			embedding = self.embedder.encode([query])[0]
		except Exception as e:
			self.logger.error(f"Error generating embedding for query: {e}")
			return []

		try:
			results = self.collection.query(query_embeddings=[embedding.tolist()], n_results=top_k)
			if 'documents' in results and results['documents']:
				return results['documents'][0]
		except Exception as e:
			self.logger.error(f"Error querying collection: {e}")
		return []

	def delete_document_by_id(self, doc_id: str):
		"""Delete document from collection by document ID."""
		try:
			self.collection.delete(ids=[doc_id])
		except Exception as e:
			self.logger.error(f"Error removing document with id {doc_id}: {e}")

	def remove_duplicate_documents(self):
		"""Remove duplicate documents, keeping only first occurrence."""
		try:
			all_docs = self.collection.get(include=["documents", "ids"])
		except Exception as e:
			self.logger.error(f"Error retrieving documents for duplicate removal: {e}")
			return

		seen_texts = set()
		ids_to_delete = []
		try:
			for doc, doc_id in zip(all_docs.get("documents", []), all_docs.get("ids", [])):
				if doc in seen_texts:
					ids_to_delete.append(doc_id)
				else:
					seen_texts.add(doc)
		except Exception as e:
			self.logger.error(f"Error processing documents for duplicates: {e}")
			return

		if ids_to_delete:
			try:
				self.collection.delete(ids=ids_to_delete)
			except Exception as e:
				self.logger.error(f"Error deleting duplicate documents: {e}")

	def get_document_by_id(self, doc_id: str) -> str | None:
		"""Retrieve a document's text by its ID or None if not found."""
		try:
			result = self.collection.get(ids=[doc_id], include=["documents"])
			if result.get("documents"):
				return result["documents"][0]
		except Exception as e:
			self.logger.error(f"Error retrieving document by id {doc_id}: {e}")
		return None
