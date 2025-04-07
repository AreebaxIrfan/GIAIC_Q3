import os 
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional , Dict 

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel(
    model_name = "gemini-2.0-flash"
)

@cl.oauth_callback
def oauth_callback(
    provider_id :str,
    token:str,
    raw_user_data:Dict[str, str],
    default_user:cl.User,
) -> Optional[cl.User]:
    """
    Handle the Oauth callback from Github
    Return the user object if authentication is successful , None otherwise
    """
    print(f"Provider:{provider_id}")
    print(f"User data: {raw_user_data}")

    return default_user
@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history",[])
    await cl.Message(content="Hello ! How can I help you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):

    history = cl.user_session.get("history")
    history.append({"role":"user","content":message.content})

    formatted_history=[]
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"

        formatted_history.append({"role":role, "parts":[{"text":msg["content"]}]})

    response = model.generate_content(formatted_history)

    response_text = response.text if hasattr(response,"text")else ""

    history.append({"role":"assistant","content": response_text})

    cl.user_session.set("history",history)

    await cl.Message(content=response_text).send()