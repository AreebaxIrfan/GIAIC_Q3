import os 
import chainlit as cl
from dotenv import load_dotenv
from typing import Optional , Dict 
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.tool import function_tool
import requests

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize OpenAI provider with Gemini API settings
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

# Configure the language model
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=provider)


@function_tool("get_weather")
def get_weather(location:str, unit:str ='C')-> str:
    """
    Fetch the weather for a given location , return the weather
    """
    return f"The weather in {location} is 22 degree {unit}"


agent = Agent(
    name="Greeting Agent",
    instructions="You are a Greeting Agent. Your task is to greet the user with a friendly message. When someone says hi, reply back with 'Salam from Areeba Irfan'. If someone says bye, respond with 'Allah Hafiz from Areeba Irfan'. If someone asks about the weather, use the get_weather tool to fetch the weather. For any other queries, respond with 'Areeba is here just for greeting, I can't answer anything else, sorry.'",
    model=model,
    tools=[get_weather],
   
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
    history.append(
        {"role":"user","content":message.content}
    )

    result = await cl.make_async(Runner.run_sync)(agent, input= history)

    response_text = result.final_output
    await cl.Message(content=response_text).send()

    history.append({
        "role":"assistant",
        "content":response_text
    })
    cl.user_session.set("history",history)