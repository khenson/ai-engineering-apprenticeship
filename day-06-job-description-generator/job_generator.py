from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv(dotenv_path=".env", verbose=True)

client = OpenAI()

def generate_job_description(company: str, role: str, requirements: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[
            {
                "role": "system",
                "content": "You are an expert HR professional who writes compelling, specific job descriptions for construction and trades companies."
            },
            {
                "role": "user",
                "content": f"Write a complete job description for a {role} position at {company}. Requirements: {requirements}"
            }
        ]
    )
    return response.choices[0].message.content
result = generate_job_description(
    company="Apex Construction Group",
    role="Commercial Electrician",
    requirements="5+ years commercial experience, journeyman license, willing to travel"
)

print(result)
