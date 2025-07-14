from controller.intent_registry import intent_handlers
import agents.search_web
import agents.open_website
import agents.send_email

async def run_browser_action(intent_data: dict):
    intent_name = intent_data.get("intent")
    entities = intent_data.get("entities", {})

    handler = intent_handlers.get(intent_name)
    if not handler:
        raise ValueError(f"No handler defined for intent '{intent_name}'")

    return await handler(entities)


