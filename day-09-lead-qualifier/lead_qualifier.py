from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel
import os

load_dotenv()

client = Anthropic()
class LeadQualification(BaseModel):
    score: int
    tier: str
    reasoning: str
    next_action: str
    estimated_value: str

def qualify_lead(lead_info: str) -> LeadQualification:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are an expert sales qualifier for a roofing company.
                
Analyze this lead and respond with ONLY a JSON object in this exact format:
{{
    "score": <number 1-10>,
    "tier": "<HIGH, MEDIUM, or LOW>",
    "reasoning": "<one sentence explanation>",
    "next_action": "<specific next step>",
    "estimated_value": "<estimated job value in dollars>"
}}

Lead information:
{lead_info}"""
            }
        ]
    )
    
    import json
    raw = message.content[0].text.strip().strip("```json").strip("```").strip()
    data = json.loads(raw)
    return LeadQualification(**data)
leads = [
    "John called about storm damage to his roof. Has a 3,000 sq ft home in Austin. Insurance claim already approved. Wants estimate this week.",
    "Someone emailed asking about roof prices generally. No address given. Mentioned they might need work done sometime next year.",
    "Maria called, roof is actively leaking into her living room. Has a 2,500 sq ft home. Needs someone out today. Has homeowners insurance."
]

for lead in leads:
    result = qualify_lead(lead)
    print(f"\nScore: {result.score}/10")
    print(f"Tier: {result.tier}")
    print(f"Reasoning: {result.reasoning}")
    print(f"Next Action: {result.next_action}")
    print(f"Estimated Value: {result.estimated_value}")
    print("-" * 40)