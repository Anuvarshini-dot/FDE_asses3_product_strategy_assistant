import chromadb


class VectorStore:
    def __init__(self):
        self._client = chromadb.EphemeralClient()
        self._collection = self._client.get_or_create_collection("product_docs")
        self._count = 0

    def add_documents(self, texts: list, ids: list):
        valid = [(t, i) for t, i in zip(texts, ids) if t.strip()]
        if valid:
            docs, doc_ids = zip(*valid)
            self._collection.add(documents=list(docs), ids=list(doc_ids))
            self._count += len(valid)

    def search(self, query: str, n_results: int = 3) -> list:
        if self._count == 0:
            return []
        try:
            n = min(n_results, self._count)
            results = self._collection.query(query_texts=[query], n_results=n)
            return results["documents"][0] if results["documents"] else []
        except Exception:
            return []

    def clear(self):
        self._client.delete_collection("product_docs")
        self._collection = self._client.get_or_create_collection("product_docs")
        self._count = 0
