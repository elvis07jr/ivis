import csv
import pandas as pd
from io import StringIO, BytesIO
from typing import List, Dict, Any, IO
from app.data_models import ColumnDefinition # Assuming ColumnDefinition is accessible

# Helper to infer basic data type - very rudimentary for now
def _infer_data_type(header: str) -> str:
    """
    Rudimentary data type inference based on header name.
    Can be significantly improved by analyzing actual data.
    """
    header_lower = header.lower()
    if "id" in header_lower or "code" in header_lower or "identifier" in header_lower:
        return "categorical" # Or numerical if it looks like a number, but safer as categorical from just header
    if "date" in header_lower or "time" in header_lower:
        return "date"
    # Add more heuristics if needed, e.g., for typical numerical names like 'amount', 'value', 'quantity'
    # For now, default to text if not obviously something else
    return "text"


async def parse_csv_to_column_definitions(file_io: IO[bytes], filename: str) -> List[ColumnDefinition]:
    """
    Parses a CSV file stream and returns a list of ColumnDefinition objects.
    """
    definitions = []
    try:
        # Read the file content as string
        content = (await file_io.read()).decode('utf-8-sig') # Use utf-8-sig to handle BOM
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(content.splitlines()[0]) # Sniff first line for dialect

        # Use csv.reader with sniffed dialect
        reader = csv.reader(StringIO(content), dialect=dialect)
        headers = next(reader, None)

        if headers:
            for header in headers:
                header = header.strip()
                if header: # Ensure header is not empty
                    definitions.append(
                        ColumnDefinition(
                            name=header,
                            data_type=_infer_data_type(header), # Rudimentary type inference
                            description=f"Column '{header}' from uploaded CSV '{filename}'."
                            # semantic_type can be inferred later or left None
                        )
                    )
        else:
            # Handle empty CSV or CSV with no headers (though typically they have one)
            # For now, return empty if no headers
            pass

    except Exception as e:
        print(f"Error parsing CSV file {filename}: {e}") # Replace with proper logging
        raise ValueError(f"Could not parse CSV file: {e}")
    return definitions


async def parse_excel_to_column_definitions(file_io: IO[bytes], filename: str) -> List[ColumnDefinition]:
    """
    Parses an Excel file stream (first sheet) and returns a list of ColumnDefinition objects.
    """
    definitions = []
    try:
        # Pandas read_excel can take a file-like object (BytesIO for bytes)
        # We need to ensure the file pointer is at the beginning if it was read before.
        # However, UploadFile.file is typically a SpooledTemporaryFile, which should be fine.
        xls_content = await file_io.read()
        df = pd.read_excel(BytesIO(xls_content), sheet_name=0, nrows=1) # Read only header row for efficiency

        if not df.empty:
            for header in df.columns:
                header_str = str(header).strip() # Ensure header is string and stripped
                if header_str:
                    definitions.append(
                        ColumnDefinition(
                            name=header_str,
                            data_type=_infer_data_type(header_str), # Rudimentary type inference
                            description=f"Column '{header_str}' from uploaded Excel file '{filename}' (first sheet)."
                        )
                    )
    except Exception as e:
        print(f"Error parsing Excel file {filename}: {e}") # Replace with proper logging
        raise ValueError(f"Could not parse Excel file: {e}")
    return definitions


async def parse_file_to_column_definitions(file_io: IO[bytes], filename: str, content_type: str) -> List[ColumnDefinition]:
    """
    Detects file type and calls the appropriate parser.
    """
    logger.info(f"Attempting to parse file: {filename}, content type: {content_type}")
    if "csv" in content_type:
        return await parse_csv_to_column_definitions(file_io, filename)
    elif "excel" in content_type or "spreadsheetml" in content_type or "ms-excel" in content_type:
        return await parse_excel_to_column_definitions(file_io, filename)
    else:
        logger.error(f"Unsupported file type: {content_type} for file {filename}")
        raise ValueError(f"Unsupported file type: {content_type}. Please upload CSV or Excel.")

# Add logger instance if not already available globally (e.g. from main)
import logging
logger = logging.getLogger(__name__)
if not logger.handlers: # Configure if not already configured by main app
    logging.basicConfig(level=logging.INFO)
