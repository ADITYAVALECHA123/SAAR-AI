from rank_bm25 import BM25Okapi

def vector_retrieval(db, query,  top_k=5,score_threshold=1.58):
    result = db.similarity_search_with_score(query, k=top_k)
    print("\n QUERY:", query)
    filtered_doc=[]
    for doc, score in result:
        print("SCORE:", score)
        print(doc.page_content[:100])
        print("-" * 50)
    for doc, score in result:
        if score <= score_threshold:
            doc.metadata["retrieval_score"] = float(score)
            filtered_doc.append(doc)
    return filtered_doc

def bm25_retrieval(docs, query,top_k=5):
    if not docs:
        return []
    tokenized_docs = [d.page_content.lower().split() for d in docs]
    bm25 = BM25Okapi(tokenized_docs)
    tokenized_query = (query.lower().split())
    scores = bm25.get_scores(tokenized_query)
    ranked = sorted(zip(docs, scores),key=lambda x: x[1],reverse=True)
    results = []
    for doc, score in ranked[:top_k]:
        doc.metadata["bm25_score"] = float(score)
        doc.metadata["retrieval_method"] = "bm25"
        results.append(doc)
    return results

def get_retriever(db, query, top_k=5,score_threshold=1.99):
    vector_docs = vector_retrieval(db, query,top_k=top_k,score_threshold=score_threshold)
    bm25_docs = bm25_retrieval(vector_docs, query, top_k=top_k)
    all_docs = vector_docs + bm25_docs
    unique_docs = {}
    for doc in all_docs:
        key = doc.page_content.strip()
        unique_docs[key] = doc
    return list(unique_docs.values())