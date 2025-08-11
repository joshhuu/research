def rag_query(user_query):
    query_embedding = model.encode(user_query).tolist()
    results = index.query(vector=query_embedding, top_k=3, include_metadata=True)
    context = "\n\n".join([match["metadata"]["text"] for match in results["matches"]])
    prompt = f"Answer the question based on the following research context:\n\n{context}\n\nQuestion: {user_query}\nAnswer:"
    response = genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt)
    return response.text
