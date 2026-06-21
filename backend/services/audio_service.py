import os
import re
import ffmpeg
from pydub import AudioSegment

def clean_title(title):
    return re.sub(r'[\\/*?:"<>|]', "", title)

def extract_upload_audio(video_path, title, user_id):
    os.makedirs("data/audio", exist_ok=True)
    safe_title = (
    f"{user_id}_"
    f"{clean_title(title)}"
)
    output_audio = os.path.join(
        "data/audio",
        f"{safe_title}.wav"
    )
    (
        ffmpeg
        .input(video_path)
        .output(
            output_audio,
            format="wav",
            acodec="pcm_s16le",
            ac=1,
            ar="16k"
        )
        .run(overwrite_output=True)
    )
    return output_audio

def split_audio(audio_path, chunk_minutes=5):
    audio = AudioSegment.from_wav(audio_path)
    chunk_length_ms = chunk_minutes * 60 * 1000
    output_files = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_path = (
            audio_path.replace(
                ".wav",
                f"_part_{i//chunk_length_ms}.wav"
            )
        )
        chunk.export(chunk_path, format="wav")
        output_files.append(chunk_path)
    return output_files