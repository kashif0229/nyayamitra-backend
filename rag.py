# rag.py
import os
import json
import re
from dotenv import load_dotenv
from groq import Groq
from data_loader import search_legal_database

load_dotenv()

# Groq client - free and fast!
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_legal_answer(query: str, case_type: str) -> dict:

    print(f"🔍 Searching legal database for: {query[:50]}...")
    relevant_laws = search_legal_database(query, n_results=5)
    legal_context = "\n\n".join(relevant_laws)

    prompt = f"""
You are NyayaMitra, an AI legal assistant for Indian citizens.

RELEVANT INDIAN LAWS:
{legal_context}

USER'S PROBLEM:
{query}

CASE TYPE: {case_type}

Respond ONLY in this exact JSON format with no extra text:
{{
  "rights_explanation": "Clear 3-4 sentence explanation of user rights with specific law sections mentioned.",
  "legal_sections": ["Section name 1", "Section name 2", "Section name 3"],
  "recommended_steps": [
    "Step 1: First action to take",
    "Step 2: Second action to take",
    "Step 3: Third action to take",
    "Step 4: Fourth action to take"
  ],
  "urgency": "HIGH",
  "summary": "One line summary of situation and main advice"
}}
"""

    print("🤖 Asking Groq AI...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Free, very powerful model
        messages=[
            {
                "role": "system",
                "content": "You are a legal assistant for Indian citizens. Always respond with valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=1000
    )

    response_text = response.choices[0].message.content

    # Extract JSON from response
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)

    if json_match:
        try:
            return json.loads(json_match.group())
        except:
            pass

    # Fallback
    return {
        "rights_explanation": response_text[:300],
        "legal_sections": ["Applicable Indian Law"],
        "recommended_steps": [
            "Step 1: Document your situation thoroughly",
            "Step 2: Visit nearest legal aid center",
            "Step 3: File complaint with appropriate authority",
            "Step 4: Follow up within 30 days"
        ],
        "urgency": "MEDIUM",
        "summary": "Please consult a legal professional for specific advice."
    }