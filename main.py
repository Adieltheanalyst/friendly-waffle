from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", cache_folder="./models")
print(model.encode(["This is a test."]))