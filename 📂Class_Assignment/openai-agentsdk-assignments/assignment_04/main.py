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

# ==============================
# Setup
# ==============================
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

# ==============================
# Context and Data Models
# ==============================
class UserInfo(BaseModel):
    name: str
    is_premium: bool
    issue_type: Optional[str] = None  # "billing", "product", or "technical"

@dataclass
class Product:
    name: str
    price: int
    quantity: int
    description: str

# ==============================
# Tools
# ==============================
@function_tool
async def stationary_items(wrapper: RunContextWrapper[UserInfo]) -> List[Product]:
    """Provide information about available stationary products."""
    return [
        Product(name="pencil", price=250, quantity=140, description="Pencil is available in just 2 colors"),
        Product(name="eraser", price=29, quantity=50, description="We have Dollar brand of eraser only"),
        Product(name="notebook", price=290, quantity=20, description="We have 500, 600, or 900 pages notebook available only"),
    ]

@function_tool(is_enabled=lambda self, context: isinstance(context, (RunContextWrapper, UserInfo)) and context.is_premium)
async def refund_tool(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Process a refund for the user."""
    if not wrapper.context.is_premium:
        return "Error: Refunds are only available for premium users."
    return f"Refund processed for {wrapper.context.name} (Premium user)."

@function_tool
async def restart_service(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Restart the service for technical issues."""
    return f"Service restarted for {wrapper.context.name}."

# ==============================
# Guardrail Setup
# ==============================
class TechnicalGuardrailOutput(BaseModel):
    is_correct_routing: bool
    reasoning: str
    expected_agent: str
    restart_service_called: bool

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

@output_guardrail
async def technical_guardrail(
    ctx: RunContextWrapper[UserInfo], agent: Agent, output: str
) -> GuardrailFunctionOutput:
    user_query_issue_type = ctx.context.issue_type if ctx.context else "unknown"
    result = await Runner.run(
        guardrail_agent,
        input=f"User query issue type: {user_query_issue_type}\nSupportAgent output: {output}",
        context=ctx.context,
        run_config=run_config
    )

    tripwire_triggered = (
        user_query_issue_type == "technical"
        and (not result.final_output.is_correct_routing or not result.final_output.restart_service_called)
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=tripwire_triggered,
    )

# ==============================
# Agents
# ==============================
Item_info_agent = Agent(
    name="ItemInfoAgent",
    instructions="Handle all queries related to product information. Use the stationary_items tool.",
    tools=[stationary_items],
    model=model,
)

billing_agent = Agent(
    name="BillingAgent",
    instructions="Handle billing-related queries, including refunds for premium users only. Use the refund_tool.",
    tools=[refund_tool],
    model=model,
)

technical_agent = Agent(
    name="TechnicalAgent",
    instructions="Handle technical queries. Use the restart_service tool when appropriate.",
    tools=[restart_service],
    model=model,
)

support_agent = Agent(
    name="SupportAgent",
    instructions=(
        "Handle all user queries. "
        "For refund-related queries, hand off to the BillingAgent. "
        "For product-related queries, hand off to the ItemInfoAgent. "
        "For technical queries, hand off to the TechnicalAgent. "
        "If the user is not a premium user and requests a refund, politely say this feature is only for premium users."
    ),
    tools=[refund_tool, stationary_items, restart_service],
    handoffs=[billing_agent, Item_info_agent, technical_agent],
    output_guardrails=[technical_guardrail],
    model=model,
)

# ==============================
# Helper Functions (Refactor)
# ==============================
def detect_issue_type(prompt: str) -> str:
    """Detect issue type from user prompt."""
    lowered = prompt.lower()
    if "refund" in lowered:
        return "billing"
    elif any(keyword in lowered for keyword in ["service", "error", "technical", "restart"]):
        return "technical"
    return "product"

async def handle_request(prompt: str, user_context: UserInfo):
    """Handle agent streaming, response printing, and error handling."""
    result = Runner.run_streamed(
        support_agent,
        input=prompt,
        context=user_context,
        run_config=run_config
    )

    try:
        print("Agent: ", end="", flush=True)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

        if result.final_output:
            print(f"\n\nFinal Response: {result.final_output}")
        else:
            print("\n\nNo final output received.")
    except OutputGuardrailTripwireTriggered as e:
        print(f"\n\nError: Output guardrail tripped - {e}")
        print("Please try again or contact support.")
    except Exception as e:
        print(f"\n\nError: Unexpected issue - {str(e)}")

    print("=== Request Complete ===")

# ==============================
# Main (Simplified)
# ==============================
async def main():
    user_context = UserInfo(name="Jane Smith", is_premium=False)

    print("💬 Support Agent")
    print("Type 'quit' to exit.\n")

    while True:
        prompt = await asyncio.to_thread(input, "\nHow can I assist you today? ")
        if prompt.lower() == "quit":
            print("👋 Exiting chat. Goodbye!")
            break

        user_context.issue_type = detect_issue_type(prompt)
        print(f"\nIssue Type Detected: {user_context.issue_type}")
        print("=== Processing Request ===")

        await handle_request(prompt, user_context)

if __name__ == "__main__":
    asyncio.run(main())
