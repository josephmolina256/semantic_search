from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import fastapi

app = fastapi.FastAPI()

@app.get("/search")
def search(query: str):
    texts = [
        "A scientist discovers humanity lives inside a computer simulation.",
        "A detective investigates a mysterious murder in New York.",
        "A young chef learns to create a new recipe for a restaurant.",
        "A person realizes their life is controlled by an artificial world."
    ]

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    query_embedding = model.encode([query]) # [dndd, dh]
    text_embeddings = model.encode(texts) # [[dnndd], [dejde]]

    scores = cosine_similarity(query_embedding, text_embeddings)[0]
    ranked = sorted(zip(texts, scores), key=lambda item: item[1], reverse=True)

    print(f"Query: {query}\n")
    res = []
    for i, (text, score) in enumerate(ranked, start=1):
        print(f"{i}. Score: {score:.4f} | {text}")
        res.append({"text": text, "score": float(score)})

    return res


