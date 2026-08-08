from app.ai.client import GeminiClient

client = GeminiClient()

response = client.generate("Say hello in one sentence.")

print(response)
