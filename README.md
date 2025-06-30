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
*   **Dataset Upload (CSV/Excel)**: Allows users to upload their dataset to automatically infer column definitions before generating suggestions (requires T&C agreement).
*   **Simple API**: Uses FastAPI for a clean and interactive API (via `/docs`).
*   **Multi-Page Frontend**: Includes a landing page, application page, and pricing page, with a shared static CSS for styling.

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
├── static/                 # Static files (CSS, JS, images)
│   └── css/
│       └── style.css       # Shared CSS styles
├── .gitignore
├── app.html                # Main application page (column input & suggestions)
├── index.html              # Landing page
├── pricing.html            # Pricing page
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

The application consists of a FastAPI backend and a set of HTML/CSS/JS frontend files.

1.  **Start the Backend API Server:**
    Open a terminal, navigate to the project's root directory, and run:
    ```bash
    uvicorn main:app --reload
    ```
    *   This command starts the FastAPI backend server using Uvicorn.
    *   It typically serves the API at `http://localhost:8000`.
    *   The `--reload` flag enables auto-reloading on code changes, which is useful for development.

    > **Important CORS Note:** The application is configured with `allow_origins=["*"]` in `main.py` for development convenience. This allows requests from any origin (e.g., when opening HTML files directly from the filesystem or using a simple local server on a different port).
    > **For production deployment, you MUST change this** to a specific list of your frontend domain(s) to prevent unauthorized access.

2.  **Accessing the Frontend Pages:**
    The frontend consists of `index.html` (landing page), `app.html` (the main application), and `pricing.html`.

    *   **Direct File Access (Simple Method):**
        *   **Landing Page:** Open the `index.html` file directly in your web browser (e.g., by double-clicking it or using `File > Open`).
        *   You can navigate to the "App" (`app.html`) and "Pricing" (`pricing.html`) pages using the navigation bar from the landing page.
        *   The `app.html` page requires the backend API server (Uvicorn) to be running at `http://localhost:8000` to fetch suggestions.

    *   **Using a Local HTTP Server (Recommended for Development):**
        For a more robust development experience that better simulates a deployed environment (especially if you add more complex JavaScript or assets), it's recommended to serve the frontend files using a simple local HTTP server.
        1.  Open another terminal window.
        2.  Navigate to the project's root directory.
        3.  Run Python's built-in HTTP server (or any other simple server):
            ```bash
            python -m http.server 8080
            ```
            (You can use any other available port, e.g., 3000, 5000, if 8080 is taken).
        4.  Then, access the frontend pages in your browser:
            *   **Landing Page:** `http://localhost:8080/` or `http://localhost:8080/index.html`
            *   **Application Page:** `http://localhost:8080/app.html`
            *   **Pricing Page:** `http://localhost:8080/pricing.html`
        Remember, the backend API (Uvicorn on port 8000) still needs to be running separately.

3.  **Accessing the API Documentation:**
    Once the backend server is running, you can access the interactive API documentation:
    *   **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
    *   **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

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

Alternatively, users can upload a CSV or Excel file on the "App" page. After agreeing to placeholder Terms & Conditions, the system will attempt to parse the file, extract column headers, and make rudimentary inferences for data types and descriptions. These inferred definitions then populate the manual input form for review and modification before generating suggestions.

The `suggestion_engine.py` then applies a set of rules based on the provided or inferred column definitions to generate a variety of suggestions. These include SVG wireframes for charts and metric cards, alongside formulas for feature engineering and metric calculations in popular tools like Excel, SQL, and Pandas.
```
