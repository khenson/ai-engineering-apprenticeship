import os
from anthropic import Anthropic
from pydantic import BaseModel
client = Anthropic()

class ProposalOutput(BaseModel):
    subject_line: str
    opening_paragraph: str
    scope_of_work: str
    investment: str
    closing_paragraph: str

def generate_proposal(customer_name: str, job_type: str, property_details: str, scope: str, price: str) -> ProposalOutput:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are a professional estimator for a home services company.

Generate a professional proposal email for this job. Respond with ONLY a JSON object in this exact format:
{{
    "subject_line": "<email subject line>",
    "opening_paragraph": "<warm professional opening>",
    "scope_of_work": "<detailed scope of work>",
    "investment": "<pricing breakdown>",
    "closing_paragraph": "<call to action closing>"
}}

Customer: {customer_name}
Job Type: {job_type}
Property: {property_details}
Scope: {scope}
Price: {price}"""
            }
        ]
    )
    
    import json
    raw = message.content[0].text.strip().strip("```json").strip("```").strip()
    data = json.loads(raw)
    return ProposalOutput(**data)

proposal = generate_proposal(
    customer_name="Tom Richardson",
    job_type="Full roof replacement",
    property_details="2,800 sq ft home in Austin, TX. 25-year-old shingles with storm damage.",
    scope="Remove existing shingles, inspect decking, replace damaged boards, install 30-year architectural shingles, new underlayment, ridge vent, and drip edge.",
    price="$14,500"
)

print(f"SUBJECT: {proposal.subject_line}")
print(f"\n{proposal.opening_paragraph}")
print(f"\nSCOPE OF WORK:\n{proposal.scope_of_work}")
print(f"\nYOUR INVESTMENT:\n{proposal.investment}")
print(f"\n{proposal.closing_paragraph}")

with open("proposal_tom_richardson.txt", "w") as f:
    f.write(f"SUBJECT: {proposal.subject_line}\n\n")
    f.write(f"{proposal.opening_paragraph}\n\n")
    f.write(f"SCOPE OF WORK:\n{proposal.scope_of_work}\n\n")
    f.write(f"YOUR INVESTMENT:\n{proposal.investment}\n\n")
    f.write(f"{proposal.closing_paragraph}")

print("\nProposal saved to proposal_tom_richardson.txt")