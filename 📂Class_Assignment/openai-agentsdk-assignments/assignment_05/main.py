# corrected_bank_agent.py
import os
import asyncio
from typing import Any
from pydantic import BaseModel
from dotenv import load_dotenv

# Agents SDK imports
from agents import (
    Agent,
    RunConfig,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
    RunContextWrapper,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    handoffs,
    input_guardrail,
    output_guardrail,
)

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file.")

# --- provider / model (adjust base_url if needed) ---
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

# --- Domain / Context models ---
class Account(BaseModel):
    name: str
    pin: int

class MessageOutput(BaseModel):
    response: str

class GuardrailAgentOutput(BaseModel):
    is_bank_related: bool
    reasoning: str | None = None

class OutputCheck(BaseModel):
    is_bank_queries: bool
    reasoning: str | None = None

# --- Handoff agents (minimum 2 as requested) ---
loan_agent = Agent(
    name="Loan Agent",
    instructions="You are a Loan agent. Provide basic information about loans, eligibility, types, interest, terms, and next steps.",
)

customer_agent = Agent(
    name="Customer Agent",
    instructions="You are the Customer Support agent. Help customers with deposit/withdrawal/refund/authentication questions and politely ask for missing info.",
)

guardrail_agent = Agent(
    name="Input Guardrail: Bank Check",
    instructions="Check whether the user's input is related to banking (balance, deposit, withdraw, transfer, loan, refund, authentication). Return a boolean 'is_bank_related' and short reasoning.",
    output_type=GuardrailAgentOutput,
)

@input_guardrail
async def check_bank_related(ctx: RunContextWrapper[None], agent: Agent, input: str) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not bool(result.final_output.is_bank_related),  # trip only if NOT bank related
    )

# --- Simple auth check used by the function tool ---
def is_authenticated(ctx: RunContextWrapper[Account], agent: Agent) -> bool:
    # Example: simple check using context
    try:
        return ctx.context.name == "Hania" and ctx.context.pin == 123
    except Exception:
        return False

@function_tool(is_enabled=is_authenticated)
def check_balance(account_number: str) -> str:
    return f"The balance for account {account_number} is $100,000"
    
control_guardrail_agent = Agent(
    name="Output Guardrail: Bank Output Check",
    instructions="Inspect the agent's final output and return whether it contains bank-related, safe content only. Return 'is_bank_queries' boolean and reasoning.",
    output_type=OutputCheck,
)

@output_guardrail
async def control_response(ctx: RunContextWrapper[None], agent: Agent, output: MessageOutput) -> GuardrailFunctionOutput:

    result = await Runner.run(control_guardrail_agent, output.response, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not bool(result.final_output.is_bank_queries),
    )

# --- Main bank agent: includes handoffs and guardrails ---
bank_agent = Agent(
    name="Bank Agent",
    instructions="You are a bank agent. Handle balance inquiries, deposits, withdrawals, transfers, refunds. Authenticate user before revealing sensitive details. If unsure, hand off to customer_agent or loan_agent.",
    handoffs=[customer_agent, loan_agent],
    input_guardrails=[check_bank_related],
    output_guardrails=[control_response],
    output_type=MessageOutput,
)

user_context = Account(name="Hania", pin=123)

# --- Run example ---
async def main():
    # Example 1: bank-related request (should pass input guardrail)
    try:
        result = await Runner.run(bank_agent, "I want to check my balance.", context=user_context, run_config=run_config)
        print("Agent result:", result.final_output.response)
    except InputGuardrailTripwireTriggered:
        print("Input guardrail tripped: user input deemed not bank-related.")
    except OutputGuardrailTripwireTriggered:
        print("Output guardrail tripped: agent produced non-bank or unsafe output.")

    # Example 2: not-bank-related request (should trip input guardrail)
    try:
        await Runner.run(bank_agent, "Help me solve my math homework: 2x + 3 = 11", context=user_context, run_config=run_config)
        print("Unexpected: guardrail didn't trip for non-bank input.")
    except InputGuardrailTripwireTriggered:
        print("Correctly trapped: non-bank input detected by input guardrail.")
    except OutputGuardrailTripwireTriggered:
        print("Output guardrail tripped (unexpected for this test).")

if __name__ == "__main__":
    asyncio.run(main())
