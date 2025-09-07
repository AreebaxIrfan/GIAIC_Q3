import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import enable_verbose_stdout_logging
from agents.run import RunConfig


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found, please check your .env file.")

external_client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client= external_client
)

config = RunConfig(
    model= model,
    model_provider= external_client,
    tracing_disabled= True
)


Smart_Store_Agent = Agent(
    name= "Smart Store Agent",
    instructions= """You are a smart, friendly store assistant. When a user shares a problem (e.g., “I have a headache”), follow this structure:

    Respond calmly and positively.

    Suggest a helpful product (e.g., medicine).

    Recommend an extra tip (like an exercise or activity).

    Briefly explain why it helps.

    Tone: Supportive, caring, and clear.""",
    
)
user_input = input("Enter your problem: ")

result = Runner.run_sync(
    Smart_Store_Agent, 
    user_input,
    run_config= config
    )

print("\nAgent's Response:\n")
print("{result.final_output}\n")
