from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

embed_target = ['Headphones', 'Printer', 'Mouse', 'Smartwatch', 'Keyboard', 'Smartphone', 'Camera', 'Monitor', 'Tablet', 'Laptop', 'Accessories', 'Office', 'Electronics', 'North', 'South', 'East', 'West']

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(embed_target)

def purify(userQuery):
  userQuery = userQuery.split()
  for i in range(len(userQuery)):
    enc_query = model.encode(userQuery[i])
    sims = list(cosine_similarity([enc_query],embeddings))
    trust = max(sims[0])
    if trust > 0.6:
      print(trust)
      userQuery[i] = embed_target[list(sims[0]).index(max(sims[0]))]
      print(userQuery)
  return ' '.join(userQuery)

