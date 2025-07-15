import os
import json
import requests
from dotenv import load_dotenv
from pathlib import Path

#######################################################
# Initialize Gemini for intent-entity extraction
#######################################################
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


def query_gemini(prompt: str) -> dict:
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    params = {"key": GEMINI_API_KEY}
    headers = {"Content-Type": "application/json"}

    response = requests.post(GEMINI_URL, params=params, headers=headers, json=payload)
    response.raise_for_status()
    content = response.json()

    raw_text = content["candidates"][0]["content"]["parts"][0]["text"]
    cleaned_text = raw_text.strip().strip("```json").strip("```").strip()
    return json.loads(cleaned_text)


class ConversationalNLUAgent:
    def __init__(self):
        self.pending_intent = None
        self.history = []  # Store last few messages
        self.max_history = 5
        self.collected_entities = {}  # Accumulated entities across turns

    def _update_history(self, role: str, message: str):
        self.history.append({"role": role, "message": message})
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def _build_history_text(self):
        return "\n".join([f"{entry['role'].capitalize()}: {entry['message']}" for entry in self.history])

    def extract_intent(self, user_message: str) -> dict:
        self._update_history("user", user_message)
        history_text = self._build_history_text()

        if self.pending_intent and self.pending_intent.get("needs_clarification"):
            clarification = self.pending_intent["clarification_question"]

            prompt = f"""
You are continuing a previous conversation.

Conversation History:
{history_text}

Previously known entities:
{json.dumps(self.collected_entities)}

Previous Clarification Request: "{clarification}"
User Response: "{user_message}"

Update the intent and entities accordingly (ONLY from these options: send_email (ensure recipient, body, and subject), search_web, open_website).

Respond ONLY in the following JSON format:

{{
  "intent": "<intent_name>",
  "entities": {{
    "<key1>": "<value1>",
    "<key2>": "<value2>"
  }},
  "needs_clarification": false,
  "clarification_question": "",
  "agent_thinking": "<your thought process in a line>"
}}
"""
            response = query_gemini(prompt)
        else:
            prompt = f"""
You are an assistant that extracts structured intent from user messages to enable browser automation.

Conversation History:
{history_text}

Your job is to:
1. Identify the user's intent from ONLY these options: send_email (ensure recipient, subject, body), search_web, open_website.
2. Extract relevant entities.
3. Determine whether clarification is needed.
4. If clarification is needed, ask a follow-up question.
5. Include your internal thought process as a single line.

Respond ONLY in the following JSON format:

{{
  "intent": "<intent_name>",
  "entities": {{
    "<key1>": "<value1>",
    "<key2>": "<value2>"
  }},
  "needs_clarification": true/false,
  "clarification_question": "<question if needed, else empty string>",
  "agent_thinking": "<your thought process in a line>"
}}
"""
            response = query_gemini(prompt)

        # Merge new entities into collected memory
        self.collected_entities.update(response.get("entities", {}))

        # Check for missing required entities in send_email
        if response["intent"] == "send_email":
            required = ["recipient", "subject", "body"]
            missing = [key for key in required if key not in self.collected_entities]

            if missing:
                response["needs_clarification"] = True
                response["clarification_question"] = (
                    f"Please provide the following missing fields: {', '.join(missing)}."
                )
                response["agent_thinking"] += f" | Missing fields: {', '.join(missing)}"
                self.pending_intent = response
                self._update_history("bot", response["clarification_question"])
                return response

        # If clarification is needed
        if response.get("needs_clarification", False):
            self.pending_intent = response
            self._update_history("bot", response["clarification_question"])
        else:
            # Final resolved intent with complete entities
            response["entities"] = self.collected_entities.copy()
            self.pending_intent = None
            self.collected_entities = {}

        return response


