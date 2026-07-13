from dotenv import load_dotenv
import anthropic
import csv
import os

load_dotenv ()
client = anthropic.Anthropic()
def generate_outreach(name: str, city: str, interest: str) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": f"Write one short, pesonalized outreach sentence for {name} in {city} who is interested in {interest}. Be conversational, not salesy."
            }
        ]
    )
    return message.content[0].text
with open("leads.csv", "r") as file:
        reader = csv.DictReader(file)
        for lead in reader:
            outreach = generate_outreach(
                lead["name"],
                lead["city"],
                lead["interest"]            
            )         
            print(f"{lead['name']}: {outreach}")

                 