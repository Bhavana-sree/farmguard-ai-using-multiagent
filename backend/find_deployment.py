import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

base_url = os.environ.get("AZURE_BASE_URL")
api_key = os.environ.get("AZURE_API_KEY")

print(f"Base URL: {base_url}")

client = AzureOpenAI(
    azure_endpoint=base_url,
    api_key=api_key,
    api_version="2024-02-15-preview"
)

# List common deployment names to try
test_names = ["gpt-4o-mini", "gpt-4", "gpt-35-turbo", "gpt-35", "gpt-4o"]

for model_name in test_names:
    print(f"\nTesting deployment: {model_name}")
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Say hi"}],
            max_tokens=5
        )
        print(f"✅ SUCCESS! Your deployment name is: {model_name}")
        print(f"   Response: {response.choices[0].message.content}")
        break
    except Exception as e:
        if "DeploymentNotFound" in str(e):
            print(f"   ❌ Not found: {model_name}")
        else:
            print(f"   ❌ Other error: {e}")