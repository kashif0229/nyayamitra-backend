# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from data_loader import load_legal_data
from rag import get_legal_answer
from classifier import classify_case, get_category_display_name
from document_generator import generate_document

# Create the FastAPI app
app = FastAPI(
    title="NyayaMitra AI Backend",
    description="AI-Powered Legal Aid System for India",
    version="1.0.0"
)

# CORS — This allows your React frontend to talk to this backend
# Without this, the browser will block the request!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# This runs ONCE when the server starts — loads legal data into ChromaDB
@app.on_event("startup")
async def startup_event():
    print("🚀 NyayaMitra backend starting...")
    load_legal_data()
    print("✅ Ready to serve!")


# This is the request format — what the frontend sends us
class LegalQuery(BaseModel):
    query: str                    # The user's problem description
    category: Optional[str] = None  # Optional: pre-selected category from frontend
    user_name: Optional[str] = "[APPLICANT]"  # Optional: user's name


# This is the main endpoint — frontend calls this when user hits submit
@app.post("/api/legal-query")
async def process_legal_query(request: LegalQuery):
    
    # Validate: don't process empty queries
    if not request.query or len(request.query.strip()) < 10:
        raise HTTPException(status_code=400, detail="Query too short. Please describe your problem in more detail.")
    
    try:
        # Step 1: Classify what type of legal problem this is
        case_type = classify_case(request.query)
        
        # Use frontend-selected category if provided
        if request.category:
            category_map = {
                "Criminal / FIR": "criminal_fir",
                "Consumer Rights": "consumer_rights",
                "RTI": "rti",
                "Labor Rights": "labor_rights",
                "Women & Family": "women_family"
            }
            case_type = category_map.get(request.category, case_type)
        
        display_category = get_category_display_name(case_type)
        print(f"📋 Case type detected: {display_category}")
        
        # Step 2: Get AI-powered legal answer using RAG
        ai_answer = get_legal_answer(request.query, display_category)
        
        # Step 3: Generate the appropriate legal document
        document = generate_document(case_type, request.query, request.user_name)
        
        # Step 4: Return everything to the frontend
        return {
            "success": True,
            "case_type": display_category,
            "rights_explanation": ai_answer.get("rights_explanation", ""),
            "legal_sections": ai_answer.get("legal_sections", []),
            "recommended_steps": ai_answer.get("recommended_steps", []),
            "urgency": ai_answer.get("urgency", "MEDIUM"),
            "summary": ai_answer.get("summary", ""),
            "generated_document": document,
            "legal_aid_centers": get_legal_aid_centers()  # Static for now
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


# Simple test endpoint — visit this in browser to check server is running
@app.get("/")
async def root():
    return {"message": "NyayaMitra AI Backend is running! 🚀", "status": "healthy"}


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}


def get_legal_aid_centers():
    """Returns static legal aid center data for demo"""
    return [
        {
            "name": "District Legal Services Authority",
            "distance": "2.3 km",
            "phone": "+91-11-23383637",
            "address": "District Court Complex, Saket"
        },
        {
            "name": "Delhi High Court Legal Aid",
            "distance": "5.1 km",
            "phone": "+91-11-23078293",
            "address": "Sher Shah Road, New Delhi"
        },
        {
            "name": "NALSA Helpline",
            "distance": "Call anytime",
            "phone": "15100",
            "address": "National Legal Services Authority (Toll Free)"
        }
    ]


# Run the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)