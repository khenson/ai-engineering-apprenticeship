from dotenv import load_dotenv
import anthropic
import os

load_dotenv()

client = anthropic.Anthropic()
def analyze_contract(file_path: str) -> str:
    with open(file_path, "r") as file:
        contract_text = file.read()

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"You are a real estate attorney reviewing a lease agreement for a tenant. Identify all risky, unusual, or potentially illegal clauses. For each issue found, explain the risk in plain English and rate it HIGH, MEDIUM, or LOW risk.\n\nLease Agreement:\n{contract_text}"
            }
        ]
    )
    return message.content[0].text

result = analyze_contract("sample_lease.txt")
print(result)
