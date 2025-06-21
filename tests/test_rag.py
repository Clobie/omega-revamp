import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from utils.rag import Rag

class TestRag(unittest.TestCase):
	def setUp(self):
		# Patch dependencies
		self.patcher_embedder = patch("utils.rag.SentenceTransformer")
		self.patcher_client = patch("utils.rag.chromadb.PersistentClient")
		self.mock_embedder_cls = self.patcher_embedder.start()
		self.mock_client_cls = self.patcher_client.start()
		self.addCleanup(self.patcher_embedder.stop)
		self.addCleanup(self.patcher_client.stop)

		# Mock embedder and client/collection
		self.mock_embedder = MagicMock()
		self.mock_embedder_cls.return_value = self.mock_embedder

		self.mock_collection = MagicMock()
		self.mock_client_instance = MagicMock()
		self.mock_client_instance.get_or_create_collection.return_value = self.mock_collection
		self.mock_client_cls.return_value = self.mock_client_instance

		# Reset singleton between tests
		Rag._instance = None
		self.rag = Rag()

	def test_singleton_behavior(self):
		rag2 = Rag()
		self.assertIs(self.rag, rag2)

	def test_add_document_success(self):
		text = "some document text"
		embedding = np.array([0.1, 0.2, 0.3])
		self.mock_embedder.encode.return_value = [embedding]

		self.rag.add_document(text)

		self.mock_embedder.encode.assert_called_once_with([text])
		self.mock_collection.add.assert_called_once()
		args, kwargs = self.mock_collection.add.call_args
		self.assertIn(text, kwargs['documents'])
		self.assertIn(embedding.tolist(), kwargs['embeddings'])
		self.assertEqual(len(kwargs['ids']), 1)

	def test_add_document_embedding_exception(self):
		self.mock_embedder.encode.side_effect = Exception("embedding error")
		result = self.rag.add_document("fail test")
		self.assertIsNone(result)
		self.mock_collection.add.assert_not_called()

	def test_update_document_success(self):
		doc_id = "123"
		new_text = "updated text"
		embedding = np.array([0.5, 0.6])
		self.mock_embedder.encode.return_value = [embedding]

		self.rag.update_document(doc_id, new_text)

		self.mock_collection.delete.assert_called_once_with(ids=[doc_id])
		self.mock_collection.add.assert_called_once()
		args, kwargs = self.mock_collection.add.call_args
		self.assertIn(new_text, kwargs['documents'])
		self.assertIn(embedding.tolist(), kwargs['embeddings'])
		self.assertIn(doc_id, kwargs['ids'])

	def test_update_document_embedding_exception(self):
		self.mock_embedder.encode.side_effect = Exception("embedding error")
		result = self.rag.update_document("123", "text")
		self.assertIsNone(result)
		self.mock_collection.delete.assert_not_called()
		self.mock_collection.add.assert_not_called()

	def test_update_document_delete_exception(self):
		embedding = np.array([1, 2, 3])
		self.mock_embedder.encode.return_value = [embedding]
		self.mock_collection.delete.side_effect = Exception("delete failed")

		self.rag.update_document("123", "text")

		self.mock_collection.add.assert_called_once()

	def test_query_top_documents_success(self):
		query = "find this"
		embedding = np.array([0.7, 0.8])
		self.mock_embedder.encode.return_value = [embedding]

		expected_docs = ["doc1", "doc2", "doc3"]
		self.mock_collection.query.return_value = {'documents': [expected_docs]}

		results = self.rag.query_top_documents(query, top_k=3)

		self.mock_embedder.encode.assert_called_once_with([query])
		self.mock_collection.query.assert_called_once_with(query_embeddings=[embedding.tolist()], n_results=3)
		self.assertEqual(results, expected_docs)

	def test_query_top_documents_embedding_exception(self):
		self.mock_embedder.encode.side_effect = Exception("embedding error")
		results = self.rag.query_top_documents("query")
		self.assertEqual(results, [])

	def test_query_top_documents_collection_exception(self):
		embedding = np.array([0.1])
		self.mock_embedder.encode.return_value = [embedding]
		self.mock_collection.query.side_effect = Exception("query error")

		results = self.rag.query_top_documents("query")
		self.assertEqual(results, [])

	def test_delete_document_by_id_success(self):
		self.rag.delete_document_by_id("doc123")
		self.mock_collection.delete.assert_called_once_with(ids=["doc123"])

	def test_delete_document_by_id_exception(self):
		self.mock_collection.delete.side_effect = Exception("delete error")
		self.rag.delete_document_by_id("doc123")
		self.mock_collection.delete.assert_called_once()

	def test_remove_duplicate_documents(self):
		docs = ["docA", "docB", "docA", "docC"]
		ids = ["id1", "id2", "id3", "id4"]
		self.mock_collection.get.return_value = {"documents": docs, "ids": ids}

		self.rag.remove_duplicate_documents()

		self.mock_collection.delete.assert_called_once_with(ids=["id3"])

	def test_remove_duplicate_documents_get_exception(self):
		self.mock_collection.get.side_effect = Exception("get error")
		self.rag.remove_duplicate_documents()
		self.mock_collection.delete.assert_not_called()

	def test_remove_duplicate_documents_processing_exception(self):
		self.mock_collection.get.return_value = {"documents": None, "ids": None}
		self.rag.remove_duplicate_documents()
		self.mock_collection.delete.assert_not_called()

	def test_get_document_by_id_success(self):
		self.mock_collection.get.return_value = {"documents": ["some text"]}
		result = self.rag.get_document_by_id("doc1")
		self.assertEqual(result, "some text")
		self.mock_collection.get.assert_called_once_with(ids=["doc1"], include=["documents"])

	def test_get_document_by_id_not_found(self):
		self.mock_collection.get.return_value = {"documents": []}
		result = self.rag.get_document_by_id("doc1")
		self.assertIsNone(result)

	def test_get_document_by_id_exception(self):
		self.mock_collection.get.side_effect = Exception("get error")
		result = self.rag.get_document_by_id("doc1")
		self.assertIsNone(result)

if __name__ == "__main__":
	unittest.main()
