# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel, Field
from fastapi.responses import PlainTextResponse # <--- NEW IMPORT

# Import your application-specific modules
from app.suggestion_engine import generate_suggestions
from app.data_models import ColumnDefinition, SuggestionOutput

app = FastAPI(
    title="iviz API",
    description="API for intelligent data visualization suggestions and feature engineering ideas.",
    version="0.1.0"
)

# --- CORS Configuration ---
# IMPORTANT: For development, we're using allow_origins=["*"] for simplicity
# to avoid CORS issues. In a production environment, you MUST replace "*"
# with your actual frontend domain(s) for security reasons.
# Example: allow_origins=["https://yourfrontend.com", "https://app.yourfrontend.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development. CHANGE THIS FOR PRODUCTION!
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers (Content-Type, Authorization, etc.)
)

# --- API Endpoints ---

# Explicitly handle OPTIONS preflight request for the /generate-ideas/ endpoint.
# The browser sends an OPTIONS request first to check CORS permissions.
# This handler ensures it gets a 200 OK response with the correct headers,
# allowing the actual POST request to proceed.
@app.options("/generate-ideas/")
async def options_generate_ideas():
    """
    Handles the CORS preflight OPTIONS request for the /generate-ideas/ endpoint.
    """
    # The CORSMiddleware typically handles adding the necessary Access-Control-Allow-* headers.
    # We just need to return a 200 OK status to indicate that the request is allowed.
    return PlainTextResponse(status_code=200)


@app.post("/generate-ideas/", response_model=SuggestionOutput)
async def get_visualization_ideas(columns: List[ColumnDefinition]):
    """
    Generates data visualization and feature engineering ideas based on provided column definitions.
    """
    if not columns:
        # This check is for an *empty list* sent in the POST request body.
        # The OPTIONS preflight request (handled by the .options() decorator) sends no body.
        raise HTTPException(status_code=400, detail="No columns provided in the request body.")
    
    suggestions = generate_suggestions(columns)
    return suggestions

# --- Example of a simple health check endpoint ---
@app.get("/")
async def root():
    return {"message": "iviz API is running!"}