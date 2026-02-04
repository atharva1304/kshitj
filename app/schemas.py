# 🐝 Honeypot Schemas - Easter Egg Edition! 🐝
# Now with 100% more request validation and 0% tolerance for garbage! 🗑️

from pydantic import BaseModel, Field, validator
from typing import List, Optional

class HoneypotRequest(BaseModel):
    # 🎯 THE FIX: Made message REQUIRED with proper validation!
    # The hackathon platform was sending garbage and we were saying "sure, whatever!" 
    # Not anymore! 💪
    message: str = Field(
        ...,  # This means REQUIRED - no empty strings allowed!
        min_length=1,  # Must have at least 1 character
        max_length=5000,  # Reasonable limit
        description="The message to analyze for scam indicators"
    )
    conversation_id: Optional[str] = Field(
        None,
        max_length=200,
        description="Optional conversation tracking ID"
    )
    
    # 🧹 The Message Janitor - Cleaning up whitespace since 2026!
    @validator('message')
    def message_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('message cannot be empty or whitespace-only')
        return v.strip()  # Auto-trim whitespace like a boss! ✨

class ExtractedIntelligence(BaseModel):
    """
    🕵️ Intelligence extracted from scam messages
    (aka the good stuff we caught from the bad guys!)
    """
    upi_ids: List[str] = []
    bank_accounts: List[str] = []
    ifsc_codes: List[str] = []
    phishing_links: List[str] = []
    phone_numbers: List[str] = []

class HoneypotResponse(BaseModel):
    """
    🎯 What we send back after catching scammers
    (or telling them 'nice try, but no')
    """
    scam_detected: bool
    confidence: float = Field(..., ge=0.0, le=1.0)  # Between 0 and 1
    scam_type: Optional[str] = None
    extracted_intelligence: Optional[ExtractedIntelligence] = None
    risk_score: Optional[float] = Field(None, ge=0.0, le=10.0)  # 0-10 scale
    agent_metadata: Optional[dict] = None
    message: Optional[str] = None
    status: str

# 🎊 Easter Egg Achievement: "The Validator" 🎊
# No more accepting empty messages like a broken vending machine!
# Scammers: 0, Your validation: 1 💪