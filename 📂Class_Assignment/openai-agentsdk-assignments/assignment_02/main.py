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


Agent = Agent(
    name= "Agent",
    instructions= "You should always responed on a homble and the repected and the motivated and teh activated way, the user will inspired with you "
    
)
user_input = input("Enter your problem: ")

result = Runner.run_sync(
    Agent, 
    user_input,
    run_config= config
    )

print(f"\nAgent's Response:\n")
print(f"{result.final_output}\n")