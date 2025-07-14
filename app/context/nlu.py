import os
import httpx
from dotenv import load_dotenv
from pathlib import Path
import requests
import json


#######################################################
    # Initialize Gemini for intent-entity extraction
########################################################
env_path = Path(__file__).resolve().parents[1] / "../env"
load_dotenv(dotenv_path=env_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = ("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent")



#######################################################
        # Query and conversational functions
########################################################

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

    def extract_intent(self, user_message: str) -> dict:
        if self.pending_intent and self.pending_intent.get("needs_clarification"):
            clarification = self.pending_intent["clarification_question"]
            clarification_context = f"""
            The user was previously asked: "{clarification}"
            Their response is: "{user_message}"

            Update the intent and entities accordingly (ONLY from these options send_email, search_web, open_website)Respond ONLY in the following JSON format:

            {{
                "intent": "<intent_name>",
                "entities": {{
                "<key1>": "<value1>",
                "<key2>": "<value2>"
              }},
              "needs_clarification": false,
              "clarification_question": ""
              "agent_thinking": <your thought process in a line>
            }}
            """
            response = query_gemini(clarification_context)
        else:
            prompt = f"""
                You are an assistant that extracts structured intent from user messages to enable browser automation.

                Your job is to:
                1. Identify the user's intent from ONLY these options : send_email, search_web, open_website)
                2. Extract all relevant entities dynamically based on the intent.
                3. Determine whether clarification is needed
                4. If clarification is needed, ask a follow-up question
                5. Also give how you are thinking in one line (eg : user hasn't provided url, asking for it.)

                Respond ONLY in the following JSON format:

                {{
                "intent": "<intent_name>",
                "entities": {{
                "<key1>": "<value1>",
                "<key2>": "<value2>"
            }},
                "needs_clarification": true/false,
                "clarification_question": "<question if needed, else empty string>"
                "agent_thinking": <your thought process in a line>
            }}

            User: "{user_message}"
            """
            response = query_gemini(prompt)

        if response.get("needs_clarification", False):
            self.pending_intent = response
        else:
            self.pending_intent = None  

        return response


# Example usage
# if __name__ == "__main__":
#     agent = ConversationalNLUAgent()
#     while True:
#         user_input = input("User: ")
#         result = agent.extract_intent(user_input)
#         if result["needs_clarification"]:
#             print(f"Agent: {result['clarification_question']}")
#         else:
#             print(f"\n Final Intent Extracted:\n{json.dumps(result, indent=2)}\n")
#             break
