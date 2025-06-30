# app/suggestion_engine.py
from typing import List, Dict, Any
from .data_models import (
    ColumnDefinition, ChartSuggestion, FeatureEngineeringSuggestion,
    MetricCardSuggestion, FormulaSuggestion, ChartWireframe
)

# --- WIREFRAME GENERATION FUNCTIONS ---
def _get_generic_svg_wireframe(chart_type: str, title: str) -> str:
    """Returns a very basic SVG wireframe based on chart type."""
    svg_map = {
        "Bar Chart": f"""
        <svg width="250" height="150" viewBox="0 0 250 150" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="20" width="200" height="110" fill="#f0f0f0" stroke="#ccc" stroke-width="1"/>
            <line x1="40" y1="110" x2="40" y2="90" stroke="#007bff" stroke-width="15"/>
            <line x1="70" y1="110" x2="70" y2="70" stroke="#007bff" stroke-width="15"/>
            <line x1="100" y1="110" x2="100" y2="100" stroke="#007bff" stroke-width="15"/>
            <line x1="130" y1="110" x2="130" y2="60" stroke="#007bff" stroke-width="15"/>
            <line x1="160" y1="110" x2="160" y2="80" stroke="#007bff" stroke-width="15"/>
            <line x1="190" y1="110" x2="190" y2="50" stroke="#007bff" stroke-width="15"/>
            <text x="25" y="35" font-family="Arial" font-size="12" fill="#555">{title}</text>
            <text x="110" y="125" font-family="Arial" font-size="10" fill="#888" text-anchor="middle">Categories</text>
            <text x="10" y="70" font-family="Arial" font-size="10" fill="#888" transform="rotate(-90 10 70)">Value</text>
        </svg>
        """,
        "Line Chart": f"""
        <svg width="250" height="150" viewBox="0 0 250 150" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="20" width="200" height="110" fill="#f0f0f0" stroke="#ccc" stroke-width="1"/>
            <polyline points="40,100 70,60 100,80 130,50 160,90 190,40 220,70" stroke="#007bff" stroke-width="2" fill="none"/>
            <circle cx="40" cy="100" r="3" fill="#007bff"/>
            <circle cx="70" cy="60" r="3" fill="#007bff"/>
            <circle cx="100" cy="80" r="3" fill="#007bff"/>
            <circle cx="130" cy="50" r="3" fill="#007bff"/>
            <circle cx="160" cy="90" r="3" fill="#007bff"/>
            <circle cx="190" cy="40" r="3" fill="#007bff"/>
            <circle cx="220" cy="70" r="3" fill="#007bff"/>
            <text x="25" y="35" font-family="Arial" font-size="12" fill="#555">{title}</text>
            <text x="120" y="125" font-family="Arial" font-size="10" fill="#888" text-anchor="middle">Time</text>
            <text x="10" y="70" font-family="Arial" font-size="10" fill="#888" transform="rotate(-90 10 70)">Value</text>
        </svg>
        """,
        "Scatter Plot": f"""
        <svg width="250" height="150" viewBox="0 0 250 150" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="20" width="200" height="110" fill="#f0f0f0" stroke="#ccc" stroke-width="1"/>
            <circle cx="50" cy="80" r="3" fill="#007bff"/>
            <circle cx="70" cy="40" r="3" fill="#007bff"/>
            <circle cx="100" cy="100" r="3" fill="#007bff"/>
            <circle cx="120" cy="60" r="3" fill="#007bff"/>
            <circle cx="150" cy="90" r="3" fill="#007bff"/>
            <circle cx="180" cy="50" r="3" fill="#007bff"/>
            <circle cx="210" cy="70" r="3" fill="#007bff"/>
            <text x="25" y="35" font-family="Arial" font-size="12" fill="#555">{title}</text>
            <text x="120" y="125" font-family="Arial" font-size="10" fill="#888" text-anchor="middle">X-Axis</text>
            <text x="10" y="70" font-family="Arial" font-size="10" fill="#888" transform="rotate(-90 10 70)">Y-Axis</text>
        </svg>
        """,
        "Histogram": f"""
        <svg width="250" height="150" viewBox="0 0 250 150" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="20" width="200" height="110" fill="#f0f0f0" stroke="#ccc" stroke-width="1"/>
            <rect x="40" y="90" width="20" height="20" fill="#007bff"/>
            <rect x="65" y="70" width="20" height="40" fill="#007bff"/>
            <rect x="90" y="50" width="20" height="60" fill="#007bff"/>
            <rect x="115" y="80" width="20" height="30" fill="#007bff"/>
            <rect x="140" y="60" width="20" height="50" fill="#007bff"/>
            <rect x="165" y="95" width="20" height="15" fill="#007bff"/>
            <text x="25" y="35" font-family="Arial" font-size="12" fill="#555">{title}</text>
            <text x="120" y="125" font-family="Arial" font-size="10" fill="#888" text-anchor="middle">Bins</text>
            <text x="10" y="70" font-family="Arial" font-size="10" fill="#888" transform="rotate(-90 10 70)">Frequency</text>
        </svg>
        """,
        "Pie/Donut Chart": f"""
        <svg width="250" height="150" viewBox="0 0 250 150" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="20" width="200" height="110" fill="#f0f0f0" stroke="#ccc" stroke-width="1"/>
            <circle cx="120" cy="75" r="40" fill="#f0f0f0" stroke="#007bff" stroke-width="2"/>
            <path d="M120 75 L 160 75 A 40 40 0 0 1 140 105 Z" fill="#007bff"/>
            <path d="M120 75 L 140 105 A 40 40 0 0 1 95 105 Z" fill="#28a745"/>
            <path d="M120 75 L 95 105 A 40 40 0 0 1 80 50 Z" fill="#ffc107"/>
            <path d="M120 75 L 80 50 A 40 40 0 0 1 160 75 Z" fill="#dc3545"/>
            <text x="25" y="35" font-family="Arial" font-size="12" fill="#555">{title}</text>
            <text x="120" y="75" font-family="Arial" font-size="10" fill="#fff" text-anchor="middle">Chart</text>
        </svg>
        """,
        "Box Plot / Violin Plot": f"""
        <svg width="250" height="150" viewBox="0 0 250 150" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="20" width="200" height="110" fill="#f0f0f0" stroke="#ccc" stroke-width="1"/>
            <rect x="50" y="60" width="20" height="40" fill="#007bff" stroke="#0056b3" stroke-width="1"/>
            <line x1="60" y1="60" x2="60" y2="40" stroke="#0056b3" stroke-width="1"/>
            <line x1="60" y1="100" x2="60" y2="120" stroke="#0056b3" stroke-width="1"/>
            <line x1="50" y1="80" x2="70" y2="80" stroke="#0056b3" stroke-width="2"/>
            <rect x="100" y="70" width="20" height="30" fill="#28a745" stroke="#1c7438" stroke-width="1"/>
            <line x1="110" y1="70" x2="110" y2="50" stroke="#1c7438" stroke-width="1"/>
            <line x1="110" y1="100" x2="110" y2="115" stroke="#1c7438" stroke-width="1"/>
            <line x1="100" y1="85" x2="120" y2="85" stroke="#1c7438" stroke-width="2"/>
            <text x="25" y="35" font-family="Arial" font-size="12" fill="#555">{title}</text>
            <text x="60" y="125" font-family="Arial" font-size="10" fill="#888" text-anchor="middle">Cat 1</text>
            <text x="110" y="125" font-family="Arial" font-size="10" fill="#888" text-anchor="middle">Cat 2</text>
            <text x="10" y="70" font-family="Arial" font-size="10" fill="#888" transform="rotate(-90 10 70)">Value</text>
        </svg>
        """,
        "Metric Card": f"""
        <svg width="250" height="100" viewBox="0 0 250 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="10" y="10" width="230" height="80" rx="8" ry="8" fill="#e9f5ff" stroke="#007bff" stroke-width="1"/>
            <text x="25" y="35" font-family="Arial" font-size="12" fill="#555" font-weight="bold">{title}</text>
            <text x="125" y="65" font-family="Arial" font-size="28" fill="#007bff" text-anchor="middle" font-weight="bold">$X,XXX</text>
            <text x="125" y="85" font-family="Arial" font-size="10" fill="#888" text-anchor="middle">Value Placeholder</text>
        </svg>
        """
    }
    return svg_map.get(chart_type, svg_map["Bar Chart"])


# --- FORMULA GENERATION FUNCTIONS ---
def _get_formulas(operation: str, cols: List[str], agg_type: str = "SUM") -> List[FormulaSuggestion]:
    formulas = []
    col1 = cols[0] if cols else "ColA"
    col2 = cols[1] if len(cols) > 1 else "ColB"

    # Excel Formulas
    if operation == "SUM":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=SUM(A:A)", example_data_context=f"Assuming '{col1}' is in column A."))
    elif operation == "AVERAGE":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=AVERAGE(A:A)", example_data_context=f"Assuming '{col1}' is in column A."))
    elif operation == "COUNT":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=COUNTA(A:A)", example_data_context=f"Assuming '{col1}' is in column A."))
    elif operation == "DIVIDE":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=A2/B2", example_data_context=f"Assuming '{col1}' is in A2 and '{col2}' is in B2. Adjust cell references as needed."))
    elif operation == "MULTIPLY":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=A2*B2", example_data_context=f"Assuming '{col1}' is in A2 and '{col2}' is in B2. Adjust cell references as needed."))
    elif operation == "SQRT":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=SQRT(A2)", example_data_context=f"Assuming '{col1}' is in A2. Adjust cell reference as needed."))
    elif operation == "GROUP_BY_SUM":
        # For Excel, this implies PivotTable or SUMIFS
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"Use PivotTable: Rows={col1}, Values={col2} (Sum)", example_data_context=f"For grouped sum, a PivotTable is recommended."))
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=SUMIFS(Sum_Range, Criteria_Range, Criteria)", example_data_context=f"For dynamic grouped sum (e.g., SUMIFS(C:C, A:A, 'Category1'))."))
    elif operation == "GROUP_BY_AVERAGE":
        # For Excel, this implies PivotTable or AVERAGEIFS
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"Use PivotTable: Rows={col1}, Values={col2} (Average)", example_data_context=f"For grouped average, a PivotTable is recommended."))
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=AVERAGEIFS(Average_Range, Criteria_Range, Criteria)", example_data_context=f"For dynamic grouped average (e.g., AVERAGEIFS(C:C, A:A, 'Category1'))."))
    elif operation == "DATE_PART_YEAR":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=YEAR(A2)", example_data_context=f"Assuming '{col1}' is a date in A2."))
    elif operation == "DATE_PART_MONTH":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=MONTH(A2)", example_data_context=f"Assuming '{col1}' is a date in A2."))
    elif operation == "DATE_PART_DAYOFWEEK":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=WEEKDAY(A2)", example_data_context=f"Assuming '{col1}' is a date in A2. Returns a number (1=Sunday or 1=Monday based on system)."))
    elif operation == "DATE_PART_QUARTER":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=ROUNDUP(MONTH(A2)/3,0)", example_data_context=f"Assuming '{col1}' is a date in A2."))
    elif operation == "DATE_DIFF_DAYS":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=TODAY()-A2", example_data_context=f"Assuming '{col1}' is a date in A2."))
    elif operation == "COUNT_UNIQUE":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=SUM(1/COUNTIF(A:A,A:A))", example_data_context=f"Array formula (Ctrl+Shift+Enter) to count unique values in column A. For newer Excel: =COUNTA(UNIQUE(A:A))"))
    elif operation == "TEXT_LENGTH":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=LEN(A2)", example_data_context=f"Assuming '{col1}' is a text in A2."))
    elif operation == "TEXT_WORD_COUNT":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=LEN(TRIM(A2))-LEN(SUBSTITUTE(A2,\" \",\"\"))+1", example_data_context=f"Assuming '{col1}' is a text in A2. Counts words based on spaces."))
    elif operation == "BOOLEAN_COUNT_TRUE":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=COUNTIF(A:A,TRUE)", example_data_context=f"Assuming '{col1}' (boolean) is in column A."))
    elif operation == "BOOLEAN_PERCENT_TRUE":
        formulas.append(FormulaSuggestion(tool="Excel", formula_string=f"=COUNTIF(A:A,TRUE)/COUNTA(A:A)", example_data_context=f"Assuming '{col1}' (boolean) is in column A. Format as percentage."))


    # SQL Formulas
    if operation == "SUM":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"SELECT SUM({col1}) FROM your_table;"))
    elif operation == "AVERAGE":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"SELECT AVG({col1}) FROM your_table;"))
    elif operation == "COUNT":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"SELECT COUNT(*) FROM your_table;"))
    elif operation == "DIVIDE":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"({col1} / {col2}) AS new_feature_name"))
    elif operation == "MULTIPLY":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"({col1} * {col2}) AS new_feature_name"))
    elif operation == "SQRT":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"SQRT({col1}) AS new_feature_name"))
    elif operation == "GROUP_BY_SUM":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"SELECT {col1}, SUM({col2}) FROM your_table GROUP BY {col1};"))
    elif operation == "GROUP_BY_AVERAGE":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"SELECT {col1}, AVG({col2}) FROM your_table GROUP BY {col1};"))
    elif operation == "DATE_PART_YEAR":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"EXTRACT(YEAR FROM {col1}) AS {col1}_year")) # Or YEAR({col1}) depending on DB
    elif operation == "DATE_PART_MONTH":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"EXTRACT(MONTH FROM {col1}) AS {col1}_month")) # Or MONTH({col1}) depending on DB
    elif operation == "DATE_PART_DAYOFWEEK":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"EXTRACT(DOW FROM {col1}) AS {col1}_dayofweek")) # Or DAYOFWEEK({col1}), varies by DB (0=Sun, 1=Mon etc)
    elif operation == "DATE_PART_QUARTER":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"EXTRACT(QUARTER FROM {col1}) AS {col1}_quarter")) # Or QUARTER({col1}) depending on DB
    elif operation == "DATE_DIFF_DAYS":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"DATEDIFF(day, {col1}, GETDATE()) AS days_since_{col1}")) # Or NOW() depending on DB
    elif operation == "COUNT_UNIQUE":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"SELECT COUNT(DISTINCT {col1}) FROM your_table;"))
    elif operation == "TEXT_LENGTH":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"LENGTH({col1}) AS {col1}_length")) # Or LEN({col1}) depending on DB
    elif operation == "TEXT_WORD_COUNT":
         # SQL word count is highly DB-dependent and often complex or requires UDFs.
         # Example for some DBs (very basic, splits by space):
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"LENGTH({col1}) - LENGTH(REPLACE({col1}, ' ', '')) + 1 AS {col1}_word_count", example_data_context="Basic word count, may vary by SQL dialect and complexity of text."))
    elif operation == "BOOLEAN_COUNT_TRUE":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"SUM(CASE WHEN {col1} THEN 1 ELSE 0 END) AS count_true_{col1}", example_data_context="Assumes boolean is TRUE/FALSE or 1/0."))
    elif operation == "BOOLEAN_PERCENT_TRUE":
        formulas.append(FormulaSuggestion(tool="SQL", formula_string=f"AVG(CASE WHEN {col1} THEN 1.0 ELSE 0.0 END) AS percent_true_{col1}", example_data_context="Assumes boolean is TRUE/FALSE or 1/0. Format as percentage."))


    # Pandas (Python) Formulas
    if operation == "SUM":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['{col1}'].sum()"))
    elif operation == "AVERAGE":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['{col1}'].mean()"))
    elif operation == "COUNT":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf.shape[0]")) # Total rows
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['{col1}'].count()")) # Count non-nulls
    elif operation == "DIVIDE":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['New_Feature'] = df['{col1}'] / df['{col2}']"))
    elif operation == "MULTIPLY":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['New_Feature'] = df['{col1}'] * df['{col2}']"))
    elif operation == "SQRT":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import numpy as np\ndf['New_Feature'] = np.sqrt(df['{col1}'])"))
    elif operation == "GROUP_BY_SUM":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf.groupby('{col1}')['{col2}'].sum()"))
    elif operation == "GROUP_BY_AVERAGE":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf.groupby('{col1}')['{col2}'].mean()"))
    elif operation == "DATE_PART_YEAR":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['{col1}'] = pd.to_datetime(df['{col1}'])\ndf['{col1}_Year'] = df['{col1}'].dt.year"))
    elif operation == "DATE_PART_MONTH":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['{col1}'] = pd.to_datetime(df['{col1}'])\ndf['{col1}_Month'] = df['{col1}'].dt.month"))
    elif operation == "DATE_PART_DAYOFWEEK":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['{col1}'] = pd.to_datetime(df['{col1}'])\ndf['{col1}_DayOfWeek'] = df['{col1}'].dt.dayofweek")) # Monday=0, Sunday=6
    elif operation == "DATE_PART_QUARTER":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['{col1}'] = pd.to_datetime(df['{col1}'])\ndf['{col1}_Quarter'] = df['{col1}'].dt.quarter"))
    elif operation == "DATE_DIFF_DAYS":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['{col1}'] = pd.to_datetime(df['{col1}'])\ndf['DaysSince'] = (pd.to_datetime('today') - df['{col1}']).dt.days"))
    elif operation == "COUNT_UNIQUE":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['{col1}'].nunique()"))
    elif operation == "TEXT_LENGTH":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['{col1}_Length'] = df['{col1}'].str.len()"))
    elif operation == "TEXT_WORD_COUNT":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['{col1}_WordCount'] = df['{col1}'].str.split().str.len()"))
    elif operation == "BOOLEAN_COUNT_TRUE":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['{col1}'].sum() # Assumes True=1, False=0 or boolean column"))
    elif operation == "BOOLEAN_PERCENT_TRUE":
        formulas.append(FormulaSuggestion(tool="Pandas_Python", formula_string=f"import pandas as pd\ndf['{col1}'].mean() # Assumes True=1, False=0 or boolean column. Format as percentage."))


    return formulas


def generate_suggestions(columns: List[ColumnDefinition]) -> Dict[str, Any]:
    """
    Analyzes column definitions and generates chart, feature engineering, and metric card suggestions.
    """
    chart_suggestions = []
    feature_engineering_suggestions = []
    metric_card_suggestions = []

    # --- Initial Parsing of Columns (THIS WAS THE MISSING PART) ---
    numerical_cols = [col for col in columns if col.data_type == "numerical"]
    categorical_cols = [col for col in columns if col.data_type == "categorical"]
    date_cols = [col for col in columns if col.data_type == "date"]
    text_cols = [col for col in columns if col.data_type == "text"]
    boolean_cols = [col for col in columns if col.data_type == "boolean"]

    # Helper for identifying ID columns more robustly
    # This checks if the column name or description indicates it's an identifier
    id_cols = [
        col for col in columns
        if col.semantic_type == "identifier" or \
           (col.data_type == "numerical" and ("id" in col.name.lower() or "identifier" in col.description.lower())) or \
           (col.data_type == "categorical" and ("id" in col.name.lower() or "identifier" in col.description.lower() or "unique" in col.description.lower()))
    ]
    # Ensure uniqueness if a column matches multiple conditions
    unique_id_cols_names = {col.name for col in id_cols}
    id_cols = [col for col in columns if col.name in unique_id_cols_names]


    # --- CHART SUGGESTIONS ---

    # Rule 1: Single Categorical Column
    for cat_col in categorical_cols:
        title_dist = f"Distribution of {cat_col.name}"
        chart_suggestions.append(
            ChartSuggestion(
                title=title_dist,
                chart_type="Bar Chart",
                columns_used=[cat_col.name],
                how_to=f"Use '{cat_col.name}' on the X-axis and count of rows on the Y-axis. This shows the frequency of each category.",
                wireframe=ChartWireframe(svg_data=_get_generic_svg_wireframe("Bar Chart", title_dist))
            )
        )
        title_prop = f"Proportion of {cat_col.name}"
        chart_suggestions.append(
            ChartSuggestion(
                title=title_prop,
                chart_type="Pie/Donut Chart",
                columns_used=[cat_col.name],
                how_to=f"Use '{cat_col.name}' to segment the pie, with the size of slices representing the count of each category. Best for 2-5 categories.",
                wireframe=ChartWireframe(svg_data=_get_generic_svg_wireframe("Pie/Donut Chart", title_prop))
            )
        )

    # Rule 2: Numerical + Categorical Column (for comparison)
    for num_col in numerical_cols:
        for cat_col in categorical_cols:
            if num_col.name != cat_col.name:
                title_agg = f"{num_col.name} by {cat_col.name}"
                chart_suggestions.append(
                    ChartSuggestion(
                        title=title_agg,
                        chart_type="Bar Chart (Aggregated)",
                        columns_used=[cat_col.name, num_col.name],
                        how_to=f"Use '{cat_col.name}' on the X-axis and the {'SUM' if num_col.semantic_type == 'currency' else 'SUM or AVERAGE'} of '{num_col.name}' on the Y-axis. " +
                                 f"This compares {'total' if num_col.semantic_type == 'currency' else 'a numerical'} value across different categories." +
                                 (f" Consider currency formatting for '{num_col.name}'." if num_col.semantic_type == 'currency' else ""),
                        wireframe=ChartWireframe(svg_data=_get_generic_svg_wireframe("Bar Chart", title_agg))
                    )
                )
                title_dist_cat_num = f"Distribution of {num_col.name} for each {cat_col.name}"
                chart_suggestions.append(
                    ChartSuggestion(
                        title=title_dist_cat_num,
                        chart_type="Box Plot / Violin Plot",
                        columns_used=[cat_col.name, num_col.name],
                        how_to=f"Use '{cat_col.name}' to define groups on the X-axis, and '{num_col.name}' for the Y-axis. This shows the spread, median, and outliers for the numerical value within each category.",
                        wireframe=ChartWireframe(svg_data=_get_generic_svg_wireframe("Box Plot / Violin Plot", title_dist_cat_num))
                    )
                )

    # Rule 3: Numerical + Date Column (for trends)
    for num_col in numerical_cols:
        for date_col in date_cols:
            title_trend = f"Trend of {num_col.name} over {date_col.name}"
            chart_suggestions.append(
                ChartSuggestion(
                    title=title_trend,
                    chart_type="Line Chart",
                    columns_used=[date_col.name, num_col.name],
                    how_to=f"Use '{date_col.name}' on the X-axis (aggregated by Day, Month, Year) and the SUM or AVERAGE of '{num_col.name}' on the Y-axis. This visualizes changes over time.",
                    wireframe=ChartWireframe(svg_data=_get_generic_svg_wireframe("Line Chart", title_trend))
                )
            )

    # Rule 4: Two Numerical Columns (for relationships)
    if len(numerical_cols) >= 2:
        for i in range(len(numerical_cols)):
            for j in range(i + 1, len(numerical_cols)):
                num_col1 = numerical_cols[i]
                num_col2 = numerical_cols[j]
                title_rel = f"Relationship between {num_col1.name} and {num_col2.name}"
                chart_suggestions.append(
                    ChartSuggestion(
                        title=title_rel,
                        chart_type="Scatter Plot",
                        columns_used=[num_col1.name, num_col2.name],
                        how_to=f"Use '{num_col1.name}' on the X-axis and '{num_col2.name}' on the Y-axis. Each point represents a record, showing correlation or clusters.",
                        wireframe=ChartWireframe(svg_data=_get_generic_svg_wireframe("Scatter Plot", title_rel))
                    )
                )

    # Rule 5: Single Numerical Column (for distribution)
    for num_col in numerical_cols:
        title_hist = f"Distribution of {num_col.name}"
        chart_suggestions.append(
            ChartSuggestion(
                title=title_hist,
                chart_type="Histogram",
                columns_used=[num_col.name],
                how_to=f"Group '{num_col.name}' into bins and count the occurrences in each bin. Shows the shape and spread of the data.",
                wireframe=ChartWireframe(svg_data=_get_generic_svg_wireframe("Histogram", title_hist))
            )
        )

    # --- FEATURE ENGINEERING SUGGESTIONS ---

    # Rule FE1: Ratio/Product of two numerical columns
    if len(numerical_cols) >= 2:
        for i in range(len(numerical_cols)):
            for j in range(i + 1, len(numerical_cols)):
                num_col1 = numerical_cols[i]
                num_col2 = numerical_cols[j]
                
                # Suggest Ratio if appropriate keywords are in descriptions
                if any(k in num_col1.description.lower() for k in ["amount", "value", "revenue", "cost", "price"]) and \
                   any(k in num_col2.description.lower() for k in ["units", "quantity", "count", "items"]):
                    feature_engineering_suggestions.append(
                        FeatureEngineeringSuggestion(
                            new_feature_name=f"{num_col1.name}_Per_{num_col2.name}",
                            description=f"Calculate the ratio of '{num_col1.name}' to '{num_col2.name}'. Useful for 'price per unit', 'revenue per customer', etc. Reveals efficiency or specific rates.",
                            columns_involved=[num_col1.name, num_col2.name],
                            potential_charts=["Histogram", "Line Chart (over time if a date column exists)", "Scatter Plot"],
                            formulas=_get_formulas("DIVIDE", [num_col1.name, num_col2.name])
                        )
                    )
                
                # Suggest Product if relevant
                if any(k in num_col1.description.lower() for k in ["price", "cost"]) and \
                   any(k in num_col2.description.lower() for k in ["quantity", "units"]):
                    feature_engineering_suggestions.append(
                        FeatureEngineeringSuggestion(
                            new_feature_name=f"Total_{num_col1.name}_x_{num_col2.name}",
                            description=f"Calculate the product of '{num_col1.name}' and '{num_col2.name}'. Useful for 'total sales' (price * quantity), 'total cost' etc.",
                            columns_involved=[num_col1.name, num_col2.name],
                            potential_charts=["Bar Chart (aggregated)", "Line Chart"],
                            formulas=_get_formulas("MULTIPLY", [num_col1.name, num_col2.name])
                        )
                    )
    
    # Advanced FE: Sqrt for skewed data
    for num_col in numerical_cols:
        # Simple heuristic: if description mentions "distribution" or "skewed"
        if "distribution" in num_col.description.lower() or "skewed" in num_col.description.lower():
            feature_engineering_suggestions.append(
                FeatureEngineeringSuggestion(
                    new_feature_name=f"SQRT_{num_col.name}",
                    description=f"Apply a square root transformation to '{num_col.name}'. Useful for normalizing highly skewed numerical data, making patterns more visible in charts.",
                    columns_involved=[num_col.name],
                    potential_charts=["Histogram", "Box Plot"],
                    formulas=_get_formulas("SQRT", [num_col.name])
                )
            )

    # Rule FE2: Time-based features from Date Column
    for date_col in date_cols:
        feature_engineering_suggestions.append(
            FeatureEngineeringSuggestion(
                new_feature_name=f"{date_col.name}_Year",
                description=f"Extract the year from '{date_col.name}'. Useful for yearly aggregation and comparison.",
                columns_involved=[date_col.name],
                potential_charts=["Bar Chart (Yearly Trend)", "Line Chart"],
                formulas=_get_formulas("DATE_PART_YEAR", [date_col.name])
            )
        )
        feature_engineering_suggestions.append(
            FeatureEngineeringSuggestion(
                new_feature_name=f"{date_col.name}_Month",
                description=f"Extract the month from '{date_col.name}'. Useful for monthly trends or seasonality analysis.",
                columns_involved=[date_col.name],
                potential_charts=["Bar Chart (Monthly Trend)", "Box Plot per Month"],
                formulas=_get_formulas("DATE_PART_MONTH", [date_col.name])
            )
        )
        feature_engineering_suggestions.append(
            FeatureEngineeringSuggestion(
                new_feature_name=f"{date_col.name}_DayOfWeek",
                description=f"Extract the day of the week from '{date_col.name}'. Useful for weekly patterns.",
                columns_involved=[date_col.name],
                potential_charts=["Bar Chart (Day of Week Trend)", "Box Plot per DayOfWeek"],
                formulas=_get_formulas("DATE_PART_DAYOFWEEK", [date_col.name])
            )
        )
        feature_engineering_suggestions.append(
            FeatureEngineeringSuggestion(
                new_feature_name=f"{date_col.name}_Quarter",
                description=f"Extract the quarter from '{date_col.name}'. Useful for quarterly business cycle analysis.",
                columns_involved=[date_col.name],
                potential_charts=["Bar Chart (Quarterly Trend)", "Line Chart"],
                formulas=_get_formulas("DATE_PART_QUARTER", [date_col.name])
            )
        )
        feature_engineering_suggestions.append(
            FeatureEngineeringSuggestion(
                new_feature_name=f"{date_col.name}_DaysSince",
                description=f"Calculate days elapsed since '{date_col.name}'. Useful for recency analysis (e.g., 'Days Since Last Purchase').",
                columns_involved=[date_col.name],
                potential_charts=["Histogram", "Scatter Plot"],
                formulas=_get_formulas("DATE_DIFF_DAYS", [date_col.name])
            )
        )

    # Rule FE3: Aggregation of numerical columns for IDs/Categorical
    for id_col in id_cols:
        for num_col in numerical_cols:
            if "order" in num_col.description.lower() or "sales" in num_col.description.lower() or "amount" in num_col.description.lower():
                # Aggregated Total
                feature_engineering_suggestions.append(
                    FeatureEngineeringSuggestion(
                        new_feature_name=f"Total_{num_col.name}_Per_{id_col.name}",
                        description=f"Calculate the sum of '{num_col.name}' grouped by each unique '{id_col.name}'. Useful for identifying total contribution per entity.",
                        columns_involved=[id_col.name, num_col.name],
                        potential_charts=["Bar Chart (Top N)", "Histogram"],
                        formulas=_get_formulas("GROUP_BY_SUM", [id_col.name, num_col.name])
                    )
                )
            # Average aggregation
            if "count" not in num_col.description.lower() and (
                "order" in num_col.description.lower() or "sales" in num_col.description.lower() or "amount" in num_col.description.lower()
            ):
                feature_engineering_suggestions.append(
                    FeatureEngineeringSuggestion(
                        new_feature_name=f"Average_{num_col.name}_Per_{id_col.name}",
                        description=f"Calculate the average of '{num_col.name}' grouped by each unique '{id_col.name}'. Useful for understanding average values per entity.",
                        columns_involved=[id_col.name, num_col.name],
                        potential_charts=["Bar Chart", "Histogram"],
                        formulas=_get_formulas("GROUP_BY_AVERAGE", [id_col.name, num_col.name])
                    )
                )

    # Rule FE4: Text-based features (Length, Word Count)
    for text_col in text_cols:
        feature_engineering_suggestions.append(
            FeatureEngineeringSuggestion(
                new_feature_name=f"{text_col.name}_Length",
                description=f"Calculate the character length of the text in '{text_col.name}'. Useful for understanding text size variability.",
                columns_involved=[text_col.name],
                potential_charts=["Histogram", "Box Plot"],
                formulas=_get_formulas("TEXT_LENGTH", [text_col.name])
            )
        )
        feature_engineering_suggestions.append(
            FeatureEngineeringSuggestion(
                new_feature_name=f"{text_col.name}_WordCount",
                description=f"Estimate the number of words in the text in '{text_col.name}'. Useful for content analysis.",
                columns_involved=[text_col.name],
                potential_charts=["Histogram", "Box Plot"],
                formulas=_get_formulas("TEXT_WORD_COUNT", [text_col.name])
            )
        )

    # --- METRIC CARD SUGGESTIONS ---

    # Rule MC1: Overall Sum/Average for Numerical Columns
    for num_col in numerical_cols:
        # Total Sum
        metric_card_suggestions.append(
            MetricCardSuggestion(
                title=f"Total {num_col.name}",
                metric_name=f"Total {num_col.name}",
                columns_used=[num_col.name],
                calculation_how_to=f"Sum all values in the '{num_col.name}' column.",
                formulas=_get_formulas("SUM", [num_col.name]),
                context=f"Displays the grand total of '{num_col.name}' across your entire dataset." +
                        (f" As this column is marked as currency, this represents a monetary total." if num_col.semantic_type == 'currency' else ""),
                wireframe=ChartWireframe(svg_data=_get_generic_svg_wireframe("Metric Card", f"Total {num_col.name}"))
            )
        )
        # Overall Average
        # Avoid suggesting average for currency if it's something like 'TotalTransactionAmount' and the sum is already suggested.
        # However, average price, average discount amount etc. make sense.
        # Heuristic: Suggest average unless semantic_type is currency AND ('total' or 'sum') is in name/description, implying it's an already summed value.
        is_pre_summed_currency = num_col.semantic_type == 'currency' and \
                                 any(kw in num_col.name.lower() for kw in ['total', 'sum', 'amount']) or \
                                 any(kw in num_col.description.lower() for kw in ['total value', 'sum of'])

        if not is_pre_summed_currency:
            metric_card_suggestions.append(
                MetricCardSuggestion(
                    title=f"Average {num_col.name}",
                    metric_name=f"Average {num_col.name}",
                    columns_used=[num_col.name],
                    calculation_how_to=f"Calculate the average of all values in the '{num_col.name}' column.",
                    formulas=_get_formulas("AVERAGE", [num_col.name]),
                    context=f"Displays the overall average of '{num_col.name}' across your dataset." +
                            (f" As this column is marked as currency, this represents an average monetary value (e.g., average price, average spend)." if num_col.semantic_type == 'currency' else ""),
                    wireframe=ChartWireframe(svg_data=_get_generic_svg_wireframe("Metric Card", f"Average {num_col.name}"))
                )
            )

    # Rule MC2: Count of Categorical/ID Columns or general records
    # Count of unique values for categorical/ID columns
    for col_for_unique_count in categorical_cols + id_cols:
        metric_card_suggestions.append(
            MetricCardSuggestion(
                title=f"Total Unique {col_for_unique_count.name}",
                metric_name=f"Unique {col_for_unique_count.name} Count",
                columns_used=[col_for_unique_count.name],
                calculation_how_to=f"Count the number of unique entries in the '{col_for_unique_count.name}' column.",
                formulas=_get_formulas("COUNT_UNIQUE", [col_for_unique_count.name]),
                context=f"Indicates the total number of distinct '{col_for_unique_count.name}' instances or unique entities in your data.",
                wireframe=ChartWireframe(svg_data=_get_generic_svg_wireframe("Metric Card", f"Unique {col_for_unique_count.name} Count"))
            )
        )

    # Total record count (can derive from any column that always has a value)
    if columns: # If there's at least one column
        first_col_name = columns[0].name
        metric_card_suggestions.append(
            MetricCardSuggestion(
                title="Total Records",
                metric_name="Total Rows in Dataset",
                columns_used=[first_col_name], # Just using the first column name as a placeholder
                calculation_how_to="Count the total number of rows/records in your dataset.",
                formulas=_get_formulas("COUNT", [first_col_name]),
                context="Represents the total size of your dataset.",
                wireframe=ChartWireframe(svg_data=_get_generic_svg_wireframe("Metric Card", "Total Records"))
            )
        )

    # Rule MC3: Metrics for Boolean Columns
    for bool_col in boolean_cols:
        metric_card_suggestions.append(
            MetricCardSuggestion(
                title=f"Count of True for {bool_col.name}",
                metric_name=f"Count True ({bool_col.name})",
                columns_used=[bool_col.name],
                calculation_how_to=f"Count the number of TRUE values in the '{bool_col.name}' column.",
                formulas=_get_formulas("BOOLEAN_COUNT_TRUE", [bool_col.name]),
                context=f"Shows how many records have the '{bool_col.name}' flag set to true.",
                wireframe=ChartWireframe(svg_data=_get_generic_svg_wireframe("Metric Card", f"Count True: {bool_col.name}"))
            )
        )
        metric_card_suggestions.append(
            MetricCardSuggestion(
                title=f"Percentage of True for {bool_col.name}",
                metric_name=f"% True ({bool_col.name})",
                columns_used=[bool_col.name],
                calculation_how_to=f"Calculate the percentage of TRUE values in the '{bool_col.name}' column out of all entries for that column.",
                formulas=_get_formulas("BOOLEAN_PERCENT_TRUE", [bool_col.name]),
                context=f"Shows the proportion of records where '{bool_col.name}' is true. Useful for conversion rates, flag prevalence, etc.",
                wireframe=ChartWireframe(svg_data=_get_generic_svg_wireframe("Metric Card", f"% True: {bool_col.name}"))
            )
        )


    # Deduplicate suggestions (simple by title/name for now)
    deduplicated_charts = {}
    for chart in chart_suggestions:
        key = (chart.title, chart.chart_type, tuple(sorted(chart.columns_used)))
        deduplicated_charts[key] = chart
    
    deduplicated_features = {}
    for fe in feature_engineering_suggestions:
        # Key includes name, sorted columns involved, and description for better uniqueness
        key = (fe.new_feature_name, tuple(sorted(fe.columns_involved)), fe.description)
        deduplicated_features[key] = fe

    deduplicated_metrics = {}
    for mc in metric_card_suggestions:
        key = (mc.title, mc.metric_name, tuple(sorted(mc.columns_used)))
        deduplicated_metrics[key] = mc

    return {
        "chart_suggestions": list(deduplicated_charts.values()),
        "feature_engineering_suggestions": list(deduplicated_features.values()),
        "metric_card_suggestions": list(deduplicated_metrics.values())
    }