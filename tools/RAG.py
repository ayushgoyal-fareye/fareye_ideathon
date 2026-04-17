from sentence_transformers import SentenceTransformer

class RAG:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the RAG class with a specific embedding model.
        Default is a lightweight, high-performance local model.
        """
        self.model = SentenceTransformer(model_name)

    def create_text_embedding(self, text: str) -> list[float]:
        """
        Takes a string and returns a list of floats representing the embedding.
        """
        if not text:
            return []
            
        
        embedding = self.model.encode(text)
        
        
        return embedding.tolist()

