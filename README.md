🌐 Webscrapper
📌 Overview

This project demonstrates how to build an AI-powered web scraping agent using:

MCP (Model Context Protocol) servers
Local LLM (LLaMA 3.2 via Ollama)
Playwright for browser automation
File system tools for data handling

The agent can autonomously browse the internet, interact with web pages, and retrieve information intelligently.

🚀 Features
🤖 Uses a local LLM (llama3.2) via Ollama
🌍 Autonomous web browsing agent
🧠 Smart decision-making using MCP tools
🛠️ Integration with:
Fetch MCP server
Playwright MCP server
Filesystem MCP server
🔄 Async execution with Python
🧰 Tech Stack
Python
OpenAI SDK (configured for local LLM)
Ollama (LLaMA 3.2)
MCP (Model Context Protocol)
Playwright
Node.js (for MCP servers)
⚙️ Setup Instructions
1. Clone the Repository
git clone https://github.com/your-username/your-repo.git
cd your-repo
2. Create Virtual Environment
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
3. Install Dependencies
pip install openai python-dotenv
npm install -g npx
4. Install & Run Ollama
Install Ollama from official website
Pull the model:
ollama pull llama3.2
5. Start Ollama Server
ollama serve
🔑 Environment Variables

Set the following in your script or .env file:

OPENAI_API_KEY=ollama
OPENAI_BASE_URL=http://localhost:11434/v1
▶️ Usage

Run the notebook or script:

python webscraping.py

Example task:

result = await Runner.run(agent, "find the most popular song on the internet")
print(result.final_output)
🧠 How It Works
Connects to a local LLM via OpenAI-compatible API
Initializes MCP servers:
Fetch (for HTTP requests)
Playwright (browser automation)
Filesystem (file handling)
Creates an intelligent agent
Agent autonomously:
Browses websites


Extracts relevant information
Returns final answer
