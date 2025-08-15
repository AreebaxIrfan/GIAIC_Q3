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

# By using Pydantic
class UserInfo(BaseModel):
    name: str
    is_premium: bool
    issue_type: Optional[str] = None  # Can be "billing", "product", or "technical"

# Define Product dataclass
@dataclass
class Product:
    name: str
    price: int
    quantity: int
    description: str

# Tool no 1
@function_tool
async def stationary_items(wrapper: RunContextWrapper[UserInfo]) -> List[Product]:
    """Provide information about available stationary products."""
    return [
        Product(name="pencil", price=250, quantity=140, description="Pencil is available in just 2 colors"),
        Product(name="eraser", price=29, quantity=50, description="We have Dollar brand of eraser only"),
        Product(name="notebook", price=290, quantity=20, description="We have 500, 600, or 900 pages notebook available only"),
    ]

# Tool no 2 for checking if the user is premium or not
@function_tool(is_enabled=lambda self, context: isinstance(context, (RunContextWrapper, UserInfo)) and context.is_premium)
async def refund_tool(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Process a refund for the user."""
    if not wrapper.context.is_premium:
        return "Error: Refunds are only available for premium users."
    return f"Refund processed for {wrapper.context.name} (Premium user)."

# Tool no 2
@function_tool
async def restart_service(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Restart the service for technical issues."""
    return f"Service restarted for {wrapper.context.name}."

# Define the guardrail output model
class TechnicalGuardrailOutput(BaseModel):
    is_correct_routing: bool
    reasoning: str
    expected_agent: str
    restart_service_called: bool

# Guardrail agent to check technical routing and restart_service
guardrail_agent = Agent(
    name="TechnicalGuardrailAgent",
    instructions=(
        "Analyze the output of the SupportAgent to determine if it correctly handles technical queries. "
        "If the user query has issue_type='technical', the output should indicate a handoff to the TechnicalAgent "
        "and the restart_service tool should be called. "
        "Return whether the routing is correct, the reasoning, the expected agent, and whether restart_service was called."
    ),
    output_type=TechnicalGuardrailOutput,
    model=model,
)

# Output guardrail to validate technical query handling
@output_guardrail
async def technical_guardrail(
    ctx: RunContextWrapper[UserInfo], agent: Agent, output: str
) -> GuardrailFunctionOutput:
    # Extract the user query issue type from the context
    user_query_issue_type = ctx.context.issue_type if ctx.context else "unknown"
    # Run the guardrail agent to analyze the output
    result = await Runner.run(
        guardrail_agent,
        input=f"User query issue type: {user_query_issue_type}\nSupportAgent output: {output}",
        context=ctx.context,
        run_config=run_config
    )

    # If issue_type is technical, ensure restart_service was called
    tripwire_triggered = False
    if user_query_issue_type == "technical":
        if not result.final_output.is_correct_routing or not result.final_output.restart_service_called:
            tripwire_triggered = True

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=tripwire_triggered,
    )
# Agent 1
# Item Info Agent for product-related queries
Item_info_agent = Agent(
    name="ItemInfoAgent",
    instructions=(
        "Handle all queries related to product information, such as name, price, quantity, or description. "
        "Use the stationary_items tool to retrieve product details and answer the user's query."
    ),
    tools=[stationary_items],
    model=model,
)
# Agent 2
# Billing Agent for refund-related queries
billing_agent = Agent(
    name="BillingAgent",
    instructions=(
        "Handle billing-related queries, including refunds for premium users only. "
        "Use the refund_tool to process refunds when appropriate. "
        "If user is not a premium user, politely say this feature is only for premium users."
    ),
    tools=[refund_tool],
    model=model,
)
# Agent 3
# Technical Agent for technical queries
technical_agent = Agent(
    name="TechnicalAgent",
    instructions=(
        "Handle technical queries, such as service outages or errors. "
        "Use the restart_service tool to restart the service when appropriate."
    ),
    tools=[restart_service],
    model=model,
)
# Agent 4
# Support Agent to triage queries and hand off to specialized agents
support_agent = Agent(
    name="SupportAgent",
    instructions=(
        "Handle all user queries. "
        "For refund-related queries, hand off to the BillingAgent. "
        "For product-related queries (e.g., product name, price, quantity, description), hand off to the ItemInfoAgent. "
        "For technical queries (e.g., service issues, errors), hand off to the TechnicalAgent. "
        "If the user is not a premium user and requests a refund, politely say this feature is only for premium users."
    ),
    tools=[refund_tool, stationary_items, restart_service],
    handoffs=[billing_agent, Item_info_agent, technical_agent],
    output_guardrails=[technical_guardrail],  # Attach the technical guardrail
    model=model,
)

async def main():
    user_context = UserInfo(name="Jane Smith", is_premium=False)

    print("💬 Support Agent")
    print("Type 'quit' to exit.\n")

    while True:
        prompt = input("\nHow can I assist you today? ")
        if prompt.lower() == "quit":
            print("👋 Exiting chat. Goodbye!")
            break

        # Update issue type for context
        if "refund" in prompt.lower():
            user_context.issue_type = "billing"
        elif any(keyword in prompt.lower() for keyword in ["service", "error", "technical", "restart"]):
            user_context.issue_type = "technical"
        else:
            user_context.issue_type = "product"

        print(f"\nIssue Type Detected: {user_context.issue_type}")
        print("=== Processing Request ===")

        # Run the agent with streaming
        result = Runner.run_streamed(
            support_agent,
            input=prompt,
            context=user_context,
            run_config=run_config
        )

        # Stream raw response events
        try:
            print("Agent: ", end="", flush=True)
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)

            # Get final output
            final_result =  result
            if final_result.final_output:
                print(f"\n\nFinal Response: {final_result.final_output}")
            else:
                print("\n\nNo final output received.")
        except OutputGuardrailTripwireTriggered as e:
            print(f"\n\nError: Output guardrail tripped - Incorrect technical query handling: {e}")
            print("Please try again or contact support for assistance.")
        except Exception as e:
            print(f"\n\nError: An unexpected error occurred - {str(e)}")

        print("=== Request Complete ===")

if __name__ == "__main__":
    asyncio.run(main())
