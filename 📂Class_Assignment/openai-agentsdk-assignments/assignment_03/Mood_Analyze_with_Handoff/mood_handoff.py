import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.run import RunConfig

# Load environment variables
load_dotenv()

# Get Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found, please check your .env file.")

# Configure external client for Gemini API
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

# Configure the model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Configure the run settings
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Define Mood Suggestions Agent
Mood_Suggestions = Agent(
    name="Mood Suggestions",
    instructions="You should give the suggestion to the user based on the mood of the user. If mood is 'sad' or 'stressed', suggests an activity or a way to deal with the situation or by giving some tips to the user to overcome the mood.",
)

# Define Mood Analyst Agent
mood_analyst = Agent(
    name="Mood Analyst",
    instructions="You analyse the mood of the user and handsoff to the appropriate agent.",
    handoffs=[Mood_Suggestions],
)

# Get user input
user_input = input("Enter your mood: ")

# Run both agents
result_suggestions = Runner.run_sync(
    Mood_Suggestions,
    user_input,
    run_config=config
)

result_analyst = Runner.run_sync(
    mood_analyst,
    user_input,
    run_config=config
)

# Prepare the output to write to a file
output_content = f"""
Agent Responses:

Mood Suggestions Agent Response:
{result_suggestions.final_output}
Responded by: {Mood_Suggestions.name}

Mood Analyst Agent Response:
{result_analyst.final_output}
Responded by: {result_analyst.last_agent.name}
"""

# Write the responses to a file
output_file = "agent_responses.txt"
with open(output_file, "w") as file:
    file.write(output_content)

print(f"Responses have been written to {output_file}")

# Print the responses to the console as well
print(output_content)