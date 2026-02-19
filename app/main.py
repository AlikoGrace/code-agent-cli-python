import argparse
import os
import sys
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
    

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")
USE_FREE = os.getenv("USE_FREE", "false").lower() == "true"
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


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
        max_tokens=300,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "read",
                    "description": "Read and return the contents of a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "The path to the file to read",
                            }
                        },
                        "required": ["file_path"]
                    },
                },
            }
        ],
        
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")
    
    msg=chat.choices[0]
     # for debugging purposes
    print("TOOL CALLS:", msg.tool_calls, file=sys.stderr)
    if msg.tools_calls:
        tool_call=msg.tool_call[0]
        tool_name=tool_call.function.name
        tool_args=json.loads(tool_call.function.arguments)


        # to executing toolcall\
        if tool_name=="read":
            path=tool_args['path']
            
            with open(path, "r", encoding="utf-8") as f:
             results=f.read()

             print(results, end="")
        else:
            raise RuntimeError(f"Unknowwn tool: {tool_name}")     
        
    else:
        print(chat.choices[0].message.content)         
 
    
    print(f"[Using model: {model}]", file=sys.stderr)

    

if __name__ == "__main__":
    main()
