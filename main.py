

import os
from dotenv import load_dotenv
import openai
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
apikey = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=apikey
)

def llm_invok(system_prompt, msg):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": msg,
            }
        ],
        model="llama-3.1-70b-versatile",
    )

    return chat_completion.choices[0].message.content

links = '''
[('https://www.youtube.com/watch?v=zYxUaNyiHH8', ''), ('https://www.youtube.com/watch?v=zYxUaNyiHH8', ''), ('https://www.youtube.com/watch?v=g8d5v_NCio4', ''), ('https://www.youtube.com/watch?v=g8d5v_NCio4', ''), ('https://www.youtube.com/watch?v=9bb6AMp2__0', ''), ('https://www.youtube.com/watch?v=9bb6AMp2__0', ''), ('https://www.youtube.com/watch?v=OGq4sFSGoNM', ''), ('https://www.youtube.com/watch?v=OGq4sFSGoNM', ''), ('https://www.youtube.com/watch?v=X_yoX3PkbHE', ''), ('https://www.youtube.com/watch?v=X_yoX3PkbHE', ''), ('https://www.youtube.com/watch?v=BKmv-n0yUYc', ''), ('https://www.youtube.com/watch?v=BKmv-n0yUYc', ''), ('https://www.youtube.com/watch?v=udjcKQMAyd0', ''), ('https://www.youtube.com/watch?v=udjcKQMAyd0', ''), ('https://www.youtube.com/watch?v=mniX7-rKvHk', ''), ('https://www.youtube.com/watch?v=mniX7-rKvHk', ''), ('https://www.youtube.com/watch?v=uOto7frzrCc', ''), ('https://www.youtube.com/watch?v=uOto7frzrCc', ''), ('https://www.youtube.com/watch?v=Nq2wYlWFucg', ''), ('https://www.youtube.com/watch?v=Nq2wYlWFucg', '')]
'''    

system_prompt = "Answer the question asked by the user"

class Item(BaseModel):
    query: str

app = FastAPI()

# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:5173",
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query/")
async def create_item(item: Item):
    query = item.query
    print(query)
    response = llm_invok(system_prompt, query)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)




