# main.py
import logging # <--- NEW IMPORT
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel, Field
from fastapi.responses import PlainTextResponse

# Import your application-specific modules
from fastapi import File, UploadFile
from typing import List # Ensure List is imported
from app.suggestion_engine import generate_suggestions
from app.data_models import ColumnDefinition, SuggestionOutput
from app import dataset_parser # Import the new parser module

app = FastAPI(
    title="iviz API",
    description="API for intelligent data visualization suggestions and feature engineering ideas.",
    version="0.1.0"
)

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
#
# UPDATE: Removing this custom handler to let CORSMiddleware handle OPTIONS automatically.
# @app.options("/generate-ideas/")
# async def options_generate_ideas():
#     """
#     Handles the CORS preflight OPTIONS request for the /generate-ideas/ endpoint.
#     """
#     # The CORSMiddleware typically handles adding the necessary Access-Control-Allow-* headers.
#     # We just need to return a 200 OK status to indicate that the request is allowed.
#     return PlainTextResponse(status_code=200)


@app.post("/generate-ideas/", response_model=SuggestionOutput)
async def get_visualization_ideas(columns: List[ColumnDefinition]):
    """
    Generates data visualization and feature engineering ideas based on provided column definitions.
    """
    logger.info(f"Received request for /generate-ideas/ with {len(columns)} column(s).")
    if not columns:
        # This check is for an *empty list* sent in the POST request body.
        # The OPTIONS preflight request (handled by the .options() decorator) sends no body.
        logger.warning("Request to /generate-ideas/ received with no columns.")
        raise HTTPException(status_code=400, detail="No columns provided in the request body.")
    
    try:
        suggestions_dict = generate_suggestions(columns)
        logger.info(f"Successfully generated {len(suggestions_dict['chart_suggestions'])} chart suggestions, "
                    f"{len(suggestions_dict['feature_engineering_suggestions'])} FE suggestions, "
                    f"and {len(suggestions_dict['metric_card_suggestions'])} metric card suggestions.")
        return suggestions_dict # FastAPI will convert this dict to SuggestionOutput
    except Exception as e:
        logger.error(f"Error during suggestion generation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal error occurred while generating suggestions.")

# --- New Endpoint for Dataset Upload ---
@app.post("/upload-dataset/")
async def handle_dataset_upload(dataset: UploadFile = File(...)):
    """
    Accepts a dataset file (CSV or Excel), parses it to infer column definitions.
    """
    if not dataset:
        logger.warning("Upload dataset request received with no file.")
        raise HTTPException(status_code=400, detail="No dataset file provided.")

    filename = dataset.filename
    logger.info(f"Received dataset file: {filename}")
    logger.info(f"Content type: {dataset.content_type}")

    # Basic validation for file type (can be enhanced)
    allowed_content_types = [
        "text/csv",
        "application/vnd.ms-excel", # .xls
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" # .xlsx
    ]
    if dataset.content_type not in allowed_content_types:
        logger.warning(f"Invalid file type uploaded: {filename} ({dataset.content_type})")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {dataset.content_type}. Please upload a CSV or Excel file."
        )

    # Placeholder for parsing logic (to be implemented in next steps)
    # For now, just acknowledge receipt and filename.
    # In a real scenario, here you would:
    # 1. Read dataset.file (it's a SpooledTemporaryFile)
    # 2. Call a parsing function (e.g., from app.dataset_parser)
    # 3. Return the list of ColumnDefinition objects

    try:
        # The file pointer of dataset.file might need to be reset if read multiple times,
        # but for a single pass to the parser, it should be fine.
        # dataset.file is a SpooledTemporaryFile.
        inferred_columns = await dataset_parser.parse_file_to_column_definitions(
            dataset.file, dataset.filename, dataset.content_type
        )
        logger.info(f"Successfully parsed {filename}, inferred {len(inferred_columns)} columns.")
        if not inferred_columns:
            logger.warning(f"No columns were inferred from file {filename}. It might be empty or have an unexpected structure.")
            # Return empty list, frontend can handle this. Or raise HTTPException.
            # For now, let's allow empty list to be returned.
        return inferred_columns
    except ValueError as ve: # Catch parsing errors from our parser
        logger.error(f"Parsing error for {filename}: {ve}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error processing file {filename}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred while processing the file: {e}")


# --- Example of a simple health check endpoint ---
@app.get("/")
async def root():
    return {"message": "iviz API is running!"}