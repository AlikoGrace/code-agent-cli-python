import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
    

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")

# If USE_FREE=true, use a free OpenRouter model
USE_FREE = os.getenv("USE_FREE", "false").lower() == "true"
def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")
    

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    model = "z-ai/glm-4.5-air:free" if USE_FREE else "anthropic/claude-haiku-4.5"
    chat = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": args.p}],
        max_tokens=10,
        
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")

    
    print(f"[Using model: {model}]", file=sys.stderr)

    # TODO: Uncomment the following line to pass the first stage 
    print(chat.choices[0].message.content)


if __name__ == "__main__":
    main()
