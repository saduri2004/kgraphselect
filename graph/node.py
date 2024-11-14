from sentence_transformers import SentenceTransformer

class Node:
    def __init__(self, node_id: int, content: str = None):
        """
        Represents a single node in the graph.
        :param node_id: Unique identifier for the node.
        :param content: Content associated with the node (e.g., text).
        """
        self.node_id = node_id
        self.content = content
        self.embedding = None  # Optional: Cache embeddings for the node

    def generate_embedding(self, model: SentenceTransformer):
        """
        Generates and stores an embedding for the node's content using a given model.
        :param model: SentenceTransformer model to use for embedding generation.
        """
        if self.content:
            self.embedding = model.encode(self.content).tolist()
        return self.embedding

    def __repr__(self):
        return f"Node(id={self.node_id}, content={self.content})"
