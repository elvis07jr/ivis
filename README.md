# iviz - Intelligent Visualization Suggester API

**iviz** is a FastAPI application that provides intelligent suggestions for data visualizations, feature engineering ideas, and key metrics based on user-provided descriptions of their dataset's columns.

The goal is to help users quickly identify potential insights and analyses they can perform on their data.

## Features

*   **Chart Suggestions**: Recommends appropriate chart types (Bar, Line, Scatter, Histogram, Pie, Box Plot) with basic SVG wireframes.
*   **Feature Engineering Ideas**: Suggests new features to create from existing columns (e.g., ratios, products, date extractions, aggregations) along with formulas in Excel, SQL, and Pandas.
*   **Key Metric Cards**: Proposes relevant metrics to track (e.g., totals, averages, unique counts) with formulas and context.
*   **Simple API**: Uses FastAPI for a clean and interactive API (via `/docs`).
*   **Basic Frontend**: Includes an `index.html` for easy interaction with the API.

## Project Structure

```
.
├── app/                    # Main application logic
│   ├── __init__.py
│   ├── data_models.py      # Pydantic models for API requests/responses
│   └── suggestion_engine.py # Core logic for generating suggestions
├── tests/                  # Unit and integration tests
│   ├── __init__.py
│   ├── test_main.py
│   └── test_suggestion_engine.py
├── .gitignore
├── index.html              # Simple frontend for interacting with the API
├── main.py                 # FastAPI application entry point
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## Setup and Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Start the FastAPI server using Uvicorn:**
    ```bash
    uvicorn main:app --reload
    ```
    The `--reload` flag enables auto-reloading when code changes, useful for development.

2.  **Access the API:**
    *   **API Docs (Swagger UI):** Open your browser to [http://localhost:8000/docs](http://localhost:8000/docs)
    *   **Alternative API Docs (ReDoc):** Open your browser to [http://localhost:8000/redoc](http://localhost:8000/redoc)
    *   **Frontend:** Open `index.html` directly in your browser (or serve it via a simple HTTP server). Note that the `fetch` URL in `index.html` is hardcoded to `http://localhost:8000/generate-ideas/`, so the Uvicorn server must be running.

## Running Tests

1.  **Ensure all development dependencies are installed (they should be if you followed the setup).**

2.  **Navigate to the root directory of the project.**

3.  **Run the tests using Python's `unittest` module:**
    ```bash
    python -m unittest discover -s tests -v
    ```
    The `-v` flag enables verbose output.

## How it Works

The user provides a list of column definitions, including:
*   `name`: The column name.
*   `data_type`: Numerical, Categorical, Date, Text, or Boolean.
*   `description`: A natural language description of the column.
*   `semantic_type` (optional): A more specific meaning like Currency, Identifier, etc.

The `suggestion_engine.py` then applies a set of rules based on these inputs to generate various suggestions. SVG wireframes are provided for charts and metric cards, and formulas are given for feature engineering and metric calculations in popular tools like Excel, SQL, and Pandas.
```
