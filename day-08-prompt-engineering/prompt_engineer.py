from dotenv import load_dotenv
import anthropic
import os

load_dotenv(override=True)

api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

def analyze_weak(contract_text: str) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024, 
        messages=[
            {
                "role": "user",
                "content": f"Review this contract and list the risks:\n\n{contract_text}"           
            }
        ]
    )
    return message.content[0].text
def analyze_strong(contract_text: str) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are a licensed real estate attorney with 20 years of experience reviewing residential leases.

Analyze this lease agreement and identify all risky clauses. Follow these rules exactly:
- Identify between 3-7 risks only
- Rate each risk as HIGH, MEDIUM, or LOW
- For each risk use this exact format:

RISK LEVEL: [HIGH/MEDIUM/LOW]
CLAUSE: [clause name]
PLAIN ENGLISH: [one sentence explanation]
ACTION: [what the tenant should do]

Think step by step. First identify unusual clauses, then evaluate legal risk, then format your response.

Lease Agreement:
{contract_text}"""
            }
        ]
    )
    return message.content[0].text

sample_contract = """
RESIDENTIAL LEASE AGREEMENT

1. RENT: Monthly rent is $2,400. Landlord may increase rent with 24 hours written notice.
2. ENTRY: Landlord may enter the property at any time without prior notice.
3. TERMINATION: Landlord may terminate lease with 24 hours notice. Tenant must provide 60 days notice.
4. LIABILITY: Tenant assumes all liability for any injuries regardless of cause, including Landlord negligence.
5. SECURITY DEPOSIT: Landlord may use deposit for any purpose and return remainder within 90 days.
"""

print("=== WEAK PROMPT OUTPUT ===")
print(analyze_weak(sample_contract))
print("\n=== STRONG PROMPT OUTPUT ===")
print(analyze_strong(sample_contract))