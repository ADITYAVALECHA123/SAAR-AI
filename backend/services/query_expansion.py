from backend.services.llm import generate_response
def expand_query(query, model="llama-3.3-70b-versatile"):
    prompt = f"""
Rewrite the user query into 3 different search queries.

Rules:
- Keep them short
- Keep meaning same
- No numbering
- No extra explanation

Query: {query}

Output:
"""
    try:
        response = generate_response(prompt, model=model)
        if hasattr(response, "content"):
            response = response.content
        else:
            response = str(response)
        lines = response.split("\n")
        queries = [query]
        for line in lines:
            line = line.strip()
            if line and len(line) > 3:
                if line[0].isdigit():
                    line = line.split(".", 1)[-1].strip()
                if line.startswith("-") or line.startswith("•"):
                    line = line[1:].strip()
                queries.append(line)
        queries = list(set(queries))
        return queries[:10]
    except Exception:
        return [query]