# 🐝 Agentic Honeypot API - Now with Extra Swagger! 🐝
# Easter Egg Edition: "The INVALID_REQUEST_BODY Destroyer" 💪

from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware  # 🌐 CORS to the rescue!
from app.schemas import HoneypotRequest, HoneypotResponse, ExtractedIntelligence
from app.auth import verify_api_key
from app.detector import detect_scam
from app.extractor import extract_intelligence
from app.agent import agent_decision, calculate_risk
from app.errors import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

app = FastAPI(
    title="Agentic Honeypot API",
    description="🐝 Catching scammers since 2026! A FastAPI that detects scams and extracts intelligence.",
    version="1.0.0"
)

# 🌍 CORS Middleware - Let the hackathon platform talk to us!
# Without this, browsers block requests faster than we block scammers 🚫
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register global exception handlers
# 🛡️ The Exception Avengers - Assembling to protect the API!
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# Constants for input safety
MAX_MESSAGE_LENGTH = 5000

# 🏠 Health check endpoint - "Is anyone home?"
@app.get("/")
def root():
    return {
        "status": "online",
        "message": "🐝 Honeypot API is buzzing! Use POST /api/honeypot/analyze to catch scammers.",
        "version": "1.0.0"
    }

# 💊 Health check endpoint - For monitoring
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "All systems go! 🚀"}


@app.post("/api/honeypot/analyze", response_model=HoneypotResponse)
def analyze_message(
    payload: HoneypotRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    🎯 The Scam Detector Endpoint
    
    Analyzes messages for scam indicators and extracts intelligence.
    
    **Required Headers:**
    - `x-api-key`: Your API key
    
    **Request Body:**
    - `message` (required): The message to analyze
    - `conversation_id` (optional): Tracking ID
    
    **Returns:**
    - Scam detection results with extracted intelligence
    """
    
    # === Input Safety Guards ===
    # 🧹 The message should already be validated by Pydantic, but let's be extra safe!
    message = payload.message.strip()

    # 🛡️ Handle excessively long messages (truncate safely)
    if len(message) > MAX_MESSAGE_LENGTH:
        message = message[:MAX_MESSAGE_LENGTH]

    # === Core Analysis ===
    # 🔍 Let's see what this message is really about...
    detection = detect_scam(message)

    # 🟢 If NOT a scam → return early (false alarm, move along!)
    if not detection.get("is_scam"):
        return {
            "scam_detected": False,
            "confidence": detection.get("confidence", 0.1),
            "message": "No scam indicators detected",
            "status": "success"
        }

    # 🔴 Scam detected → extract intelligence (gotcha! 🎯)
    scam_type = detection.get("scam_type")
    intel = extract_intelligence(message)
    risk = calculate_risk(intel, scam_type)
    agent_meta = agent_decision(scam_type, risk)

    return {
        "scam_detected": True,
        "scam_type": detection.get("scam_type"),
        "confidence": detection.get("confidence"),
        "extracted_intelligence": intel,
        "agent_metadata": agent_meta,
        "risk_score": risk,
        "status": "success"
    }

# 🎊 Easter Egg Achievement: "The API Perfectionist" 🎊
# CORS enabled ✅
# Validation tightened ✅  
# Error handling rock-solid ✅
# Documentation on point ✅
# Scammers caught ✅
# Hackathon won... pending! 🏆