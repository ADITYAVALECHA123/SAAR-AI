from backend.services.llm import generate_response
def generate_chat_title(message, model="llama-3.3-70b-versatile"):
    try:
        prompt = f"""
        Generate a SHORT chat title.
        Rules:
        - Maximum 10 words
        - No quotes
        - No punctuation
        - Clear and meaningful
        - Summarize the topic
        Message:
        {message}
        Title:
        """
        title = generate_response(prompt,model=model)
        return title.strip().replace('"', "")[:100]
    except Exception as e:
        print(f"Title Generation Error: {e}")
        return message[:60]
