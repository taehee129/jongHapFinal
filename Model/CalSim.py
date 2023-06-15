
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class CalSim :
    def __init__(self) -> None:
        pass
        
    def sentenceSimilarity(self, sentence1, sentence2):
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        embeddings = model.encode([sentence1, sentence2])
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
        return similarity[0][0]

