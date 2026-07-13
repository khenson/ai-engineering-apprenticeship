from dotenv import load_dotenv
load_dotenv()

import anthropic

client = anthropic.Anthropic()

def generate_names(service: str, location: str, outcome: str) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Generate 5 short, brandable business names for a {service} company in {location}. The customer outcome is: {outcome}. Return only the names, one per line, no explanations."
            }
        ]
    )
    return message.content[0].text

result = generate_names("Home Watch Service", "Western North Carolina", "protect your home while you're away")
print(result)


