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
        ]

def assistant_msg_to_dict(msg):
    out={"role":"assistant", "content":msg.content}
    if msg.tool_calls:
        out["tools_calls"]=[{
            "id":tc.id,
            "type":tc.type,
            "function":{
                "name":tc.function.name,
                "arguments":tc.function.arguments,
            }
        }
        for tc in msg.tool_calls
        ]
        return out 

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")
    

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    model = "z-ai/glm-4.5-air:free" if USE_FREE else "anthropic/claude-haiku-4.5"




    messages=[{"role":"user", "content":args.p}]
#=====================Me -> model:my request==========#
  
    while True:
     chat = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=300,
       tools=tools, 
       tool_choice="auto",
       temperature=0
        
    )
     if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response") 

#===================model to me :response===============#
     msg=chat.choices[0].message

     messages.append(assistant_msg_to_dict(msg))

    #  messages.append({
    #    "role":"assistant",
    #    "content":msg.content,
    #    "tool_calls":msg.tool_calls
    # })

     if not msg.tool_calls:
       print((msg.content or "").strip())
       break
    
    #====How i  handle the model's response======#
    for tc in msg.tool_calls:
        tool_name=tc.function.name
        tool_args=json.loads(tc.function.arguments)
    
        # to executing toolcall\
        if tool_name=="read":
            path=tool_args['file_path']
            with open(path, "r", encoding="utf-8") as f:
             result=f.read()
        else:
            raise RuntimeError(f"Unknowwn tool: {tool_name}")   
        messages.append({
            "role":"tool",
            "tool_call_id":tc.id,
            "content":result,
        })  
   
    

if __name__ == "__main__":
    main()
