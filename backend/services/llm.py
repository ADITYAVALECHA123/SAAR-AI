from backend.services.groq_client import client
from groq import RateLimitError, APITimeoutError, APIError
import time

PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "qwen/qwen3-32b"

def generate_response(prompt, model=PRIMARY_MODEL,temperature=0.3, max_tokens = 2048, retries=3, stream=False):
    messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=messages,
                max_tokens=max_tokens,
                stream=stream
            )
            return response.choices[0].message.content
        except RateLimitError:
            wait_time = 2** attempt
            print(f"Rate Limit hit. Retrying in {wait_time}s")
            time.sleep(wait_time)
        except APITimeoutError:
            wait_time = 2**attempt
            print(f"Timeout. Retrying in {wait_time}s")
            time.sleep(wait_time)
        except APIError as e:
            print(f"Groq API Error:{e}")
            break
        except Exception as e:
            print(f"Unexpected error:{e}")
            break
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=FALLBACK_MODEL,
                temperature=temperature,
                messages=messages,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except RateLimitError:
            wait_time = 2** attempt
            print(f"Rate Limit hit. Retrying in {wait_time}s")
            time.sleep(wait_time)
        except APITimeoutError:
            wait_time = 2**attempt
            print(f"Timeout. Retrying in {wait_time}s")
            time.sleep(wait_time)
        except Exception as e:
             print(f"Fallback Model Failed: {e}")
        return ("AI Service Temporarily Unvailable Please Try again after some time")

