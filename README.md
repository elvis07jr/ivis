# iviz - Intelligent Visualization Suggester API

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#) <!-- Placeholder -->
[![Coverage Status](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](#) <!-- Placeholder -->
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](#) <!-- Placeholder, matches app version -->

**iviz** is a FastAPI application that provides intelligent suggestions for data visualizations, feature engineering ideas, and key metrics based on user-provided descriptions of their dataset's columns.

The goal is to help users quickly identify potential insights and analyses they can perform on their data.

---

## ✨ Features

*   **Chart Suggestions**: Recommends appropriate chart types (Bar, Line, Scatter, Histogram, Pie, Box Plot) with basic SVG wireframes.
*   **Feature Engineering Ideas**: Suggests new features to create from existing columns (e.g., ratios, products, date extractions, aggregations) along with formulas in Excel, SQL, and Pandas.
*   **Key Metric Cards**: Proposes relevant metrics to track (e.g., totals, averages, unique counts) with formulas and context.
*   **Simple API**: Uses FastAPI for a clean and interactive API (via `/docs`).
*   **Basic Frontend**: Includes an `index.html` for easy interaction with the API.

---

## 📂 Project Structure

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

---

## 🚀 Setup and Installation

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
    > **Note:** Using a virtual environment is highly recommended to avoid conflicts with system-wide packages.

---

## ▶️ Running the Application

1.  **Start the FastAPI server using Uvicorn:**
    ```bash
    uvicorn main:app --reload
    ```
    The `--reload` flag enables auto-reloading when code changes, useful for development.

    > **Important CORS Note:** The application is configured with `allow_origins=["*"]` for development convenience, allowing requests from any origin (e.g., when opening `index.html` directly from the filesystem).
    > **For production, you MUST change this** in `main.py` to a specific list of your frontend domain(s) to prevent unauthorized access.

2.  **Access the API:**
    *   **API Docs (Swagger UI):** Open your browser to [http://localhost:8000/docs](http://localhost:8000/docs)
    *   **Alternative API Docs (ReDoc):** Open your browser to [http://localhost:8000/redoc](http://localhost:8000/redoc)
    *   **Application Page:** Open `app.html` directly in your browser (or serve it via a simple HTTP server). Note that the `fetch` URL in `app.html` is hardcoded to `http://localhost:8000/generate-ideas/`, so the Uvicorn server must be running. (The main entry point will soon be `index.html` - the new landing page).

---

## ✅ Running Tests

1.  **Ensure all development dependencies are installed (they should be if you followed the setup).**

2.  **Navigate to the root directory of the project.**

3.  **Run the tests using Python's `unittest` module:**
    ```bash
    python -m unittest discover -s tests -v
    ```
    The `-v` flag enables verbose output.

---

## 🛠️ How it Works

The user provides a list of column definitions, including:
*   `name`: The column name.
*   `data_type`: Numerical, Categorical, Date, Text, or Boolean.
*   `description`: A natural language description of the column.
*   `semantic_type` (optional): A more specific meaning like Currency, Identifier, etc.

Based on these inputs, the `suggestion_engine.py` applies a set of rules to generate a variety of suggestions. These include SVG wireframes for charts and metric cards, alongside formulas for feature engineering and metric calculations in popular tools like Excel, SQL, and Pandas.
```
