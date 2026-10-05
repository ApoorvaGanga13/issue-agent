import os

# agent.loop builds an API client when it is imported; tests never call the API.
os.environ.setdefault("GEMINI_API_KEY", "test-key-not-used")
