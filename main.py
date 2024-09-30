import os
from dotenv import load_dotenv
import openai
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
load_dotenv()

apikey = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=apikey
)

def llm_invok(system_prompt,msg):
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

    return (chat_completion.choices[0].message.content)

links = '''
[('https://www.youtube.com/watch?v=zYxUaNyiHH8', ''), ('https://www.youtube.com/watch?v=zYxUaNyiHH8', ''), ('https://www.youtube.com/watch?v=g8d5v_NCio4', ''), ('https://www.youtube.com/watch?v=g8d5v_NCio4', ''), ('https://www.youtube.com/watch?v=9bb6AMp2__0', ''), ('https://www.youtube.com/watch?v=9bb6AMp2__0', ''), ('https://www.youtube.com/watch?v=OGq4sFSGoNM', ''), ('https://www.youtube.com/watch?v=OGq4sFSGoNM', ''), ('https://www.youtube.com/watch?v=X_yoX3PkbHE', ''), ('https://www.youtube.com/watch?v=X_yoX3PkbHE', ''), ('https://www.youtube.com/watch?v=BKmv-n0yUYc', ''), ('https://www.youtube.com/watch?v=BKmv-n0yUYc', ''), ('https://www.youtube.com/watch?v=udjcKQMAyd0', ''), ('https://www.youtube.com/watch?v=udjcKQMAyd0', ''), ('https://www.youtube.com/watch?v=mniX7-rKvHk', ''), ('https://www.youtube.com/watch?v=mniX7-rKvHk', ''), ('https://www.youtube.com/watch?v=uOto7frzrCc', ''), ('https://www.youtube.com/watch?v=uOto7frzrCc', ''), ('https://www.youtube.com/watch?v=Nq2wYlWFucg', ''), ('https://www.youtube.com/watch?v=Nq2wYlWFucg', '')]
'''    

system_prompt = "Answser the question asked by the user"

class Item(BaseModel):
    query: str
app = FastAPI()


@app.get("/")
async def read_root():
    return {"WELCOME": "This is welcome text"}

@app.post("/query")
async def create_item(item: Item):
    query = item.query
    print(query)
    response = llm_invok(system_prompt,query)
    return {"response": response}


# run the following command to use the api service
#  pip install uvicron on terminal
#  uvicorn main:app --reload

