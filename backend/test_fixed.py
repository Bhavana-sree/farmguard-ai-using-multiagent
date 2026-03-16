import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

base_url = os.environ.get("AZURE_BASE_URL")
api_key = os.environ.get("AZURE_API_KEY")
model = os.environ.get("AZURE_MODEL")

print(f"Base URL: {base_url}")
print(f"Model: {model}")

# Remove /openai/v1 if present
if base_url and base_url.endswith('/openai/v1'):
    base_url = base_url.replace('/openai/v1', '')
    print(f"Fixed URL: {base_url}")

client = AzureOpenAI(
    azure_endpoint=base_url,
    api_key=api_key,
    api_version="2024-02-15-preview"
)

try:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=10
    )
    print("✅ Success!", response.choices[0].message.content)
except Exception as e:
    print(f"❌ Error: {e}")