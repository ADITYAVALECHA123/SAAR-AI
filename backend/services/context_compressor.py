def compress_context(docs, max_chars=15000):
    seen_sentences = set()
    compressed_chunks = []
    total_chars = 0
    for doc in docs:
        text = doc.page_content.strip()
        sentences = text.split(".")
        unique_sentences = []
        for s in sentences:
            sentence = s.strip()
            if (sentence and sentence not in seen_sentences):
                seen_sentences.add(sentence)
                unique_sentences.append(sentence)
        cleaned_text = ". ".join(unique_sentences)
        if not cleaned_text:
            continue
        if (total_chars + len(cleaned_text) > max_chars):
            break
        compressed_chunks.append(cleaned_text)
        total_chars += len(cleaned_text)
    return "\n\n".join(compressed_chunks)