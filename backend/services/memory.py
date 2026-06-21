def build_chat_context(chat_history,limit=8):
    if not chat_history:
        return ""
    context_parts = []
    history = chat_history[-limit:]
    for msg in history:
        role = msg.get("role", "").strip()
        content = msg.get("content","").strip()
        if not content:
            continue
        if role == "user":
            context_parts.append(f"User: {content}")
        elif role == "assistant":
            context_parts.append(f"Assistant: {content}")
    context = "\n".join(context_parts)
    MAX_CONTEXT_CHARS = 10000
    return context[:MAX_CONTEXT_CHARS]