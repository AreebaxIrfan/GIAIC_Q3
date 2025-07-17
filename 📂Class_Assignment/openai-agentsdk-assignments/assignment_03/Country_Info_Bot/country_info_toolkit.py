import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel

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
# Define agents
language_agent = Agent(
    name="language_agent",
    instructions="You should give the language name of the country or answer language-related questions, such as translations or greetings.",
    model= model
)

capital_agent = Agent(
    name="capital_agent",
    instructions="You should give the capital of the country",
    model = model
)

population_agent = Agent(
    name="population_agent",
    instructions="You should give the population of the country",
    model= model
)


orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a country information agent. Use the tools 'get_country_language', "
        "'get_country_capital', or 'get_country_population' to answer queries about a country. "
        "Extract the country name from the query and pass it as the 'input' parameter to the appropriate tool."
    ),
    model = model ,
    tools=[
        language_agent.as_tool(
            tool_name="get_country_language",
            tool_description="Get the language of the country or answer language-related questions",
   
),

        capital_agent.as_tool(
             tool_name="get_country_capital",
             tool_description="Get the capital of the country",
    
),

        population_agent.as_tool(
             tool_name="get_country_population",
             tool_description="Get the population of the country",
   
),
    ],
  
)

result = Runner.run_sync(
    orchestrator_agent,
    input="What is the capital of the United States?",
    run_config=config
)

print(result.final_output)