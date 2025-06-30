# app/data_models.py
from pydantic import BaseModel, Field
from typing import List, Literal, Dict, Any, Optional

# --- Input Model ---
class ColumnDefinition(BaseModel):
    """
    Defines the structure for a single column provided by the user.
    """
    name: str = Field(..., description="The name of the column (e.g., 'Sales', 'Customer ID').")
    data_type: Literal["numerical", "categorical", "date", "text", "boolean"] = Field(
        ..., description="The inferred data type of the column."
    )
    description: str = Field(
        ..., description="A brief description of what the column represents (e.g., 'Total revenue from a transaction', 'Unique identifier for a customer')."
    )

# --- Output Models ---

class ChartWireframe(BaseModel):
    """
    Represents the SVG data for a chart wireframe.
    """
    svg_data: str = Field(..., description="SVG data string for the wireframe image.")

class FormulaSuggestion(BaseModel):
    """
    Provides a formula for a specific tool (e.g., Excel, SQL, Pandas).
    """
    tool: Literal["Excel", "SQL", "Pandas_Python"] = Field(..., description="The tool for which the formula is provided.")
    formula_string: str = Field(..., description="The actual formula string for the tool.")
    example_data_context: Optional[str] = Field(
        None, description="Contextual example of data (e.g., 'A2, B2' for Excel) or usage instructions."
    )

class ChartSuggestion(BaseModel):
    """
    Represents a suggested chart visualization.
    """
    title: str = Field(..., description="A suggested title for the chart.")
    chart_type: str = Field(..., description="The type of chart (e.g., 'Bar Chart', 'Line Chart', 'Scatter Plot').")
    columns_used: List[str] = Field(..., description="List of original columns used to create this chart.")
    how_to: str = Field(..., description="Instructions on how to create this chart using the specified columns.")
    wireframe: ChartWireframe = Field(..., description="SVG data for the wireframe of this chart.")


class FeatureEngineeringSuggestion(BaseModel):
    """
    Represents a suggested new feature derived from existing columns.
    """
    new_feature_name: str = Field(..., description="Suggested name for the new engineered feature.")
    description: str = Field(
        ..., description="Explanation of what this new feature represents and why it's useful."
    )
    columns_involved: List[str] = Field(..., description="Original columns involved in creating this new feature.")
    potential_charts: List[str] = Field(..., description="Chart types that could effectively use this new feature.")
    formulas: List[FormulaSuggestion] = Field(
        ..., description="Formulas to create this new feature in various tools."
    )

class MetricCardSuggestion(BaseModel):
    """
    Represents a suggested key performance indicator (KPI) or metric.
    """
    title: str = Field(..., description="Title for the metric card (e.g., 'Total Sales', 'Avg. Order Value').")
    metric_name: str = Field(..., description="The name of the metric to display (e.g., 'Total Revenue', 'Average Order Value').")
    columns_used: List[str] = Field(..., description="Original columns used to derive this metric.")
    calculation_how_to: str = Field(..., description="Instructions on how to calculate this metric.")
    formulas: List[FormulaSuggestion] = Field(
        ..., description="Formulas to calculate this metric in various tools."
    )
    context: Optional[str] = Field(
        None, description="Context or interpretation for the metric (e.g., 'Displays overall sales performance')."
    )

class SuggestionOutput(BaseModel):
    """
    The complete output structure containing all types of suggestions.
    """
    chart_suggestions: List[ChartSuggestion] = Field(..., description="List of suggested chart ideas.")
    feature_engineering_suggestions: List[FeatureEngineeringSuggestion] = Field(
        ..., description="List of suggested feature engineering ideas."
    )
    metric_card_suggestions: List[MetricCardSuggestion] = Field(
        ..., description="List of suggested metric card ideas."
    )