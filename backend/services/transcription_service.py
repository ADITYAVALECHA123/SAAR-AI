import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
def transcribe_audio(audio_path):
    with open(audio_path, "rb") as file:
        transcription = (client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3-turbo",
            response_format="verbose_json"))
    return transcription.text