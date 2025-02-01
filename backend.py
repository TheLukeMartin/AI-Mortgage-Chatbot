# %%
import os
import requests
import sqlite3
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.schema import AIMessage, BaseMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MORTGAGE_API_HOST = os.getenv("MORTGAGE_API_HOST")
MORTGAGE_API_KEY = os.getenv("MORTGAGE_API_KEY")
ZILLOW_API_HOST = os.getenv("ZILLOW_API_HOST")
ZILLOW_API_KEY = os.getenv("ZILLOW_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ ERROR: OPENAI_API_KEY is missing. Check your .env file!")

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ Set up SQLite Database (Thread-Safe)
def get_db():
    conn = sqlite3.connect("chat_history.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, user TEXT, bot TEXT)")
    conn.commit()
    return conn, cursor

# ✅ Updated LangChain Model
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=OPENAI_API_KEY
)

# ✅ Updated Prompt Template
prompt_template = PromptTemplate(
    input_variables=["user_input", "chat_history"],
    template="Previous chat:\n{chat_history}\nUser: {user_input}\nAI:"
)

# ✅ Updated Chain
chain = prompt_template | llm | RunnableLambda(lambda x: x)

# ✅ Request Model for `/chat`
class ChatRequest(BaseModel):
    user_input: str

# ✅ Chatbot Endpoint
@app.post("/chat")
async def chat(request: ChatRequest, db=Depends(get_db)):
    try:
        conn, cursor = db

        # Retrieve Chat History for Context
        cursor.execute("SELECT bot FROM history ORDER BY id DESC LIMIT 5")
        chat_history = "\n".join([row[0] for row in cursor.fetchall()])
        print("✅ Chat History Loaded")

        # ✅ Run LangChain Model
        response = chain.invoke({"user_input": request.user_input, "chat_history": chat_history})
        print(f"🔹 Raw LangChain Response: {response}")

        # ✅ FIX: Convert LangChain `AIMessage` Response to Text
        if isinstance(response, BaseMessage):
            response = response.content  # ✅ Extracts text from AIMessage
        elif isinstance(response, list):
            response = "\n".join([msg.content if isinstance(msg, BaseMessage) else str(msg) for msg in response])
        elif isinstance(response, dict) and "text" in response:
            response = response["text"]
        else:
            response = str(response)

        print(f"✅ Final Processed Response: {response}")

        # ✅ Save to Chat History
        cursor.execute("INSERT INTO history (user, bot) VALUES (?, ?)", (request.user_input, response))
        conn.commit()
        conn.close()

        return {"response": response}
    except Exception as e:
        print(f"🚨 Error in Chatbot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Chat History Endpoint
@app.get("/history")
async def get_chat_history(db=Depends(get_db)):
    conn, cursor = db
    cursor.execute("SELECT user, bot FROM history ORDER BY id DESC LIMIT 10")
    chat_data = cursor.fetchall()
    conn.close()
    return {"history": [{"user": row[0], "bot": row[1]} for row in chat_data]}

# ✅ Start FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)

# %%
