def rerank_documents(query, docs, top_k=5):
    """
    Simple reranker using keyword overlap scoring
    """

    query_words = set(query.lower().split())
    scored_docs = []
    for doc in docs:
        content = set(doc.page_content.lower().split())
        keyword_score = len(query_words.intersection(content))
        retrieval_score = doc.metadata.get("retrieval_score", 1.0)
        final_score = (keyword_score - retrieval_score)
        scored_docs.append((final_score, doc))
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored_docs[:top_k]]


def get_dynamic_top_k(query):
    word_count = len(query.split())
    if word_count <= 5:
        return 3
    elif word_count <= 15:
        return 5
    elif word_count <= 30:
        return 8
    else:
        return 10