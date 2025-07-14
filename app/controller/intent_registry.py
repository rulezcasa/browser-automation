# intent_registry.py
from typing import Callable, Dict

intent_handlers: Dict[str, Callable] = {}

def intent(name: str):
    def wrapper(fn):
        intent_handlers[name] = fn
        return fn
    return wrapper
