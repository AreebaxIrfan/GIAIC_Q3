import os
import asyncio
from typing import Any, List, Optional
from agents import (
    Agent,
    RunConfig,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
    RunContextWrapper,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    handoffs,
    input_guardrail,
    output_guardrail,
)
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel
from dataclasses import dataclass

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file.")

provider = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=False,
)

class Account(BaseModel):
    name:str
    pin:int
class My_output(BaseModel):
    name:str
    balanced:str
class Guardrail_Agent(BaseModel):
    is_bank_related:bool

loan_agent = Agent(
    name='Loan Agent',
    instructions='You are a Loan agent , in which you should give the all the basic information , about the loan related.'

)

customer_agent = Agent(
    name='Customer Agent',
    instructions='You are the customer agent solved all the customer quries'
)

bank_agent =Agent(
    name='Bank Agent',
    instructions='You are a bank agent , handle all the queires about the user cashing, deposit the data , refunding , but make sure user is authenticated.',
    handoffs=[customer_agent,loan_agent] 
)


guardrail_agent = Agent(
    name='Guardrail Agent',
    instructions='You are a guardrail agent , you check if the user is asking about anyting else you neglect it.',
    output_type=Guardrail_Agent
)

@input_guardrail
async def check_bank_related(ctx:RunContextWrapper[None], agent:Agent, input:str)->GuardrailFunctionOutput:

    result = await Runner.run(
        guardrail_agent,
        input,
        context = ctx.context
    )
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_bank_related
    )
    # return guardail_instance 

def check_user(ctx:RunContextWrapper[Account],agent:Agent) ->bool:
    if ctx.context.name =='Hania' and ctx.context.pin ==123:
        return True
    else:
        return False

@function_tool(is_enabled = check_user)
def check_blanced(account_number:str) -> str:
    return f"The balance of account is $100000"

user_context =Account(name='Hania', pin=1782 )

result = Runner.run_sync(
    bank_agent, 
    'I want to my balance',
    run_config=run_config)

print(result.final_output)