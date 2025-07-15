
# browser-automation

This repository is the codebase for a browser automation tool powered by Natural Language Understanding. It allows users to interact with and automate browser actions using intuitive user commands.

---

## 🚀 Core Features

- Natural language command processing with intent and entity extraction.
- Multi-turn dialogue handling for follow-up prompts and clarifications.
- Built-in agents for common browser tasks like search, email, and navigation (can be expanded).
- Automates browser actions like clicking, typing, and navigation.
- Google authentication for first-time login and consistent user context.


---

## 📦 Project Structure

```bash
|── app/ 
  ├── agents/        # In-built agents for various browser tasks (can be added)
  ├── context/       # NLU module
  ├── protocol/      # API routes and websocket implementation
  ├── controller/    # Agent orchestration and management
  ├── utils/         # Auths and other helper modules
|── webapp/ 
  ├── public/       # Static files
  ├── src/          # Components and source code
```

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python), WebSocket APIs, Playwright for browser automation.  
- **Natural Language Understanding:** Google Gemini API. 
- **Frontend:** React.js with real-time chat interface.
- **Authentication:** Google OAuth2-based user login for browsing.


### Requirements

- Python 3.10+
- `.env` file with:
  - `GEMINI_API_KEY`

### Setup

```bash
# Clone the repository
git clone https://github.com/rulezcasa/browser-automation.git
cd browser-automation

# Install dependencies
pip install -r requirements.txt

# Run the server
cd app
uvicorn app.main:app --reload

# Run the webapp
cd webapp
npm start
```

---

## 🧪 Usage

### Websocket endpoint

| Method | Route                        | Description                           |
| ------ | ---------------------------- | ------------------------------------- |
| CONNECT|          `/chat`             | Connects to the websocket for chat    |

---


## 🧑‍💻 Authors
- [@rulezcasa](https://gitlab.com/rulezcasa) - Maintainer & Developer

---

## 📈 Project Status

🚧 Actively in development – No stable builds or deployed versions available yet.
---
