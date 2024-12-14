class Retriever:
    """Retriever class to handle vector search queries."""

    def __init__(self, vector_store):
        self.retriever = vector_store.as_retriever()

    def retrieve(self, query, top_k=3):
        """Retrieve the top-k results for the given query."""
        print(f"Retrieving top {top_k} results for query: {query}")
        results = self.retriever.invoke(query, top_k=top_k)
        print("Results retrieved.")
        return results