# 📚 Library System Agent

A Python-based conversational library system powered by the OpenAI Agents SDK and Gemini API 🚀. Query book availability, check copy counts, and explore the library catalog with personalized responses and guardrails to keep things on track 📖.

## ✨ Features

- 🔍 **Search Book Tool**: Check if a book (e.g., *Atomic Habits*, *Rich Dad Poor Dad*) exists in the library.
- 📚 **Check Availability Tool**: Find out how many copies of a book are available.
- 🗄️ **Book Database**: Stores book names, authors, and copy counts in a Python dictionary.
- 🧑‍💼 **Dynamic Instructions**: Greets users by name (e.g., “Hello Areeba Irfan!”) for a personal touch.
- 🚨 **Guardrails**: Ensures queries are library-related, rejecting off-topic ones (e.g., “What’s the weather?”).
- 🔄 **Conversational Loop**: Keeps prompting for input until you type “exit” or “quit”.
- 🤝 **Multiple Tool Handling**: Handles combined queries (e.g., “Is *The 10X Rule* available and how many copies?”) with parallel tool calls.
- 🔠 **Case-Insensitive Search**: Matches books regardless of case (e.g., “atomic habits” finds *Atomic Habits*).

## 🛠️ Requirements

- 🐍 Python 3.8+
- ⚡ [uv](https://github.com/astral-sh/uv) for dependency management
- 🔑 Gemini API key (stored in `.env` file)
- 📦 Dependencies: `prompt_toolkit`, `pydantic`, `python-dotenv`, `openai`, and the OpenAI Agents SDK (or custom `agents` library)

## ⚙️ Setup

1. **Clone the Repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd assignment_06
   ```

2. **Set Up Virtual Environment**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   uv add prompt_toolkit pydantic python-dotenv openai
   ```
   *Note*: If using a custom `agents` library (e.g., from GIAIC), ensure it’s included in your project directory or installed separately.

4. **Configure Gemini API Key**:
   - Create a `.env` file in the project root:
     ```env
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
   - Get a key from [Google Cloud Console](https://console.cloud.google.com/) and ensure sufficient quota.

5. **Run the Application**:
   ```bash
   uv run main.py -w
   ```

## 🚀 Usage

- Start the program with `uv run main.py -w` 🖥️.
- Try queries like:
  - “Is *Rich Dad Poor Dad* available? 🔍”
  - “How many copies of *Atomic Habits*? 📚”
  - “List all books 📖”
  - “Is *Think and Grow Rich* available and how many copies? 🤝”
- Exit by typing `exit` or `quit` 👋.
- Non-library queries (e.g., “What’s the weather?”) will be rejected by guardrails 🚫.

**Example Interaction**:
```
Enter your question (type 'exit' to quit): Is Atomic Habits available? 🔍
The book 'Atomic Habits' is available in the library.

Enter your question (type 'exit' to quit): How many copies of Rich Dad Poor Dad? 📚
There are 2 copies of 'Rich Dad Poor Dad' available.

Enter your question (type 'exit' to quit): exit 👋
Goodbye!
```

## 📝 Notes

- **API Quota** ⚠️: If you see a `429` error, check your Gemini API quota in [Google Cloud Console](https://cloud.google.com/vertex-ai/docs/quotas).
- **Case Sensitivity** 🔠: Book searches are case-insensitive (e.g., “atomic habits” matches *Atomic Habits*).
- **Conversation History** 🕰️: Not enabled by default. To add, modify `UserInfo` and `dynamic_instructions` in `main.py`.
- **Troubleshooting** 🐞: For errors like `400 Invalid JSON`, verify the Gemini API endpoint (`base_url`) and `ModelSettings` parameters. Check logs for details.

## 📂 Project Structure

- `main.py`: Core script with the library agent, tools, and conversational loop 🖥️.
- `.env`: Stores the Gemini API key (not tracked in version control) 🔑.
- `BOOK_DATABASE`: In-memory dictionary with books like *Atomic Habits* and *The 10X Rule* 📚.

## 🤝 Contributing

Feel free to submit issues or pull requests to enhance the system (e.g., adding book reservation or conversation history) 🌟.
