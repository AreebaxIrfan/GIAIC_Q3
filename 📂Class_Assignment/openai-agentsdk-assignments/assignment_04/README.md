# Multi-Agent Support System (Gemini AI)
A Python-based multi-agent support system using Gemini API and OpenAI Agents SDK. It handles billing, product, and technical queries with guardrails for correctness.

# 🚀 Features
Agents: Support, Billing, Product Info, Technical

# Tools:

stationary_items → Product details

refund_tool → Refunds (premium only)

restart_service → Service restart

Guardrails: Ensures technical queries are routed correctly

Streaming responses for real-time chat

#⚙️ Setup
```
bash

git clone <repo_url>
cd project-folder
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
Create .env:

ini
GEMINI_API_KEY=your_gemini_api_key_here
```
▶️ Run
```
bash

python main.py
```
🧪 Example
```

How can I assist you today? I need a refund
Issue Type Detected: billing
Agent: Refund is not processed for Jane Smith (only for Premium user).
```
📌 Dependencies
```
Python 3.9+

OpenAI Agents SDK

Pydantic

python-dotenv
```
