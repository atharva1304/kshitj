# 🔐 The API Key Bouncer - Easter Egg Edition! 🔐
# "No key? No entry!" - Since 2026 💪

from fastapi import Header, HTTPException
import os
import time


# 🔑 Grab the API key from environment (or use test key for local dev)
API_KEY = os.getenv("API_KEY", "test-key")

def verify_api_key(x_api_key: str = Header(None, description="Your API key for authentication")):
    """
    🛡️ The Gatekeeper Function
    
    Verifies that the request has a valid API key in the x-api-key header.
    
    Without this, you shall not pass! 🧙‍♂️
    """
    
    # 🚫 No key provided? Sorry, access denied!
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "message": "Missing x-api-key header. Please provide a valid API key. 🔑"
            }
        )
    
    # 🔍 Key provided but wrong? Nice try, but no!
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "message": "Invalid API key. Access denied. 🚫"
            }
        )
    
    # ✅ Valid key! Welcome aboard! 🎉
    return x_api_key

# 🎊 Easter Egg Achievement: "The Security Guard" 🎊
# Keeping unauthorized requests out since 2026!
# Scammers blocked: ∞
# Valid users welcomed: All of them! 🎉