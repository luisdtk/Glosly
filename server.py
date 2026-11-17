import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

SYSTEM = "You are Glosly, an assistant for gamers. Reply in the same language as the user, clear and direct."


class Message(BaseModel):
    role: str
    content: str


class Talking(BaseModel):
    messages: list[Message]


@app.post("/ask")
def ask(c: Talking):
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM}] + [m.model_dump() for m in c.messages],
    )
    return {"answer": r.choices[0].message.content}


# always the last: give a folder public (index.html, app.js, style.css)
app.mount("/", StaticFiles(directory="public", html=True), name="static")