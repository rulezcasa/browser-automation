from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from context.nlu import ConversationalNLUAgent
from controller.orchestrator import run_browser_action

router = APIRouter()
nlu_agent = ConversationalNLUAgent()

@router.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            user_message = await websocket.receive_text()
            response = nlu_agent.extract_intent(user_message)
            
            if response["needs_clarification"]:
                await websocket.send_text(response["agent_thinking"])
                await websocket.send_text(response["clarification_question"])
            else:
                intent = response.get("intent")
                message = ""

                if intent == "send_email":
                    message = "Sure, I can help you send an email."
                elif intent == "search_web":
                    message = "Alright, let's search the web for that."
                elif intent == "open_website":
                    message = "Got it. Opening the website for you."
                else:
                    message = "Intent recognized, proceeding with the task."

                await websocket.send_text(message)

                await run_browser_action(response)
    
    except WebSocketDisconnect:
        print("Client disconnected")



