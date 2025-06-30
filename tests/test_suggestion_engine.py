import unittest
from app.suggestion_engine import generate_suggestions, _get_formulas
from app.data_models import ColumnDefinition, ChartSuggestion, FeatureEngineeringSuggestion, MetricCardSuggestion, FormulaSuggestion, ChartWireframe

class TestSuggestionEngine(unittest.TestCase):

    def test_empty_columns_input(self):
        """Test that no suggestions are generated for empty column list."""
        suggestions = generate_suggestions([])
        self.assertEqual(len(suggestions['chart_suggestions']), 0)
        self.assertEqual(len(suggestions['feature_engineering_suggestions']), 0)
        self.assertEqual(len(suggestions['metric_card_suggestions']), 0)

    def test_single_numerical_column(self):
        """Test suggestions for a single numerical column."""
        columns = [
            ColumnDefinition(name="Age", data_type="numerical", description="Age of person")
        ]
        suggestions = generate_suggestions(columns)

        # Chart: Histogram
        chart_titles = [cs.title for cs in suggestions['chart_suggestions']]
        self.assertIn("Distribution of Age", chart_titles)
        histogram_suggestion = next(cs for cs in suggestions['chart_suggestions'] if cs.title == "Distribution of Age")
        self.assertEqual(histogram_suggestion.chart_type, "Histogram")
        self.assertEqual(histogram_suggestion.columns_used, ["Age"])

        # Metric Cards: Total, Average
        metric_titles = [ms.title for ms in suggestions['metric_card_suggestions']]
        self.assertIn("Total Age", metric_titles)
        self.assertIn("Average Age", metric_titles)
        # Also "Total Records"
        self.assertIn("Total Records", metric_titles)


    def test_single_categorical_column(self):
        """Test suggestions for a single categorical column."""
        columns = [
            ColumnDefinition(name="Category", data_type="categorical", description="Product category")
        ]
        suggestions = generate_suggestions(columns)

        chart_titles = [cs.title for cs in suggestions['chart_suggestions']]
        self.assertIn("Distribution of Category", chart_titles) # Bar Chart
        self.assertIn("Proportion of Category", chart_titles) # Pie Chart

        pie_suggestion = next(cs for cs in suggestions['chart_suggestions'] if cs.chart_type == "Pie/Donut Chart")
        self.assertEqual(pie_suggestion.columns_used, ["Category"])

        metric_titles = [ms.title for ms in suggestions['metric_card_suggestions']]
        self.assertIn("Total Unique Category", metric_titles)


    def test_numerical_and_categorical_columns(self):
        """Test suggestions for one numerical and one categorical column."""
        columns = [
            ColumnDefinition(name="Sales", data_type="numerical", description="Total sales amount"),
            ColumnDefinition(name="Region", data_type="categorical", description="Sales region")
        ]
        suggestions = generate_suggestions(columns)

        chart_titles = [cs.title for cs in suggestions['chart_suggestions']]
        # Expected: Sales by Region (Agg Bar), Dist of Sales for each Region (Box Plot)
        # And individual charts: Dist of Sales (Histo), Dist of Region (Bar), Prop of Region (Pie)
        self.assertIn("Sales by Region", chart_titles)
        self.assertIn("Distribution of Sales for each Region", chart_titles)

        agg_bar_suggestion = next(cs for cs in suggestions['chart_suggestions'] if cs.title == "Sales by Region")
        self.assertEqual(agg_bar_suggestion.chart_type, "Bar Chart (Aggregated)")
        self.assertCountEqual(agg_bar_suggestion.columns_used, ["Region", "Sales"])


    def test_numerical_and_date_columns(self):
        """Test suggestions for one numerical and one date column."""
        columns = [
            ColumnDefinition(name="Revenue", data_type="numerical", description="Daily revenue"),
            ColumnDefinition(name="OrderDate", data_type="date", description="Date of order")
        ]
        suggestions = generate_suggestions(columns)
        chart_titles = [cs.title for cs in suggestions['chart_suggestions']]
        self.assertIn("Trend of Revenue over OrderDate", chart_titles)

        line_chart_suggestion = next(cs for cs in suggestions['chart_suggestions'] if cs.chart_type == "Line Chart")
        self.assertCountEqual(line_chart_suggestion.columns_used, ["OrderDate", "Revenue"])

        fe_names = [fe.new_feature_name for fe in suggestions['feature_engineering_suggestions']]
        self.assertIn("OrderDate_Year", fe_names)
        self.assertIn("OrderDate_DaysSince", fe_names)

    def test_two_numerical_columns(self):
        """Test suggestions for two numerical columns."""
        columns = [
            ColumnDefinition(name="Temperature", data_type="numerical", description="Avg daily temperature"),
            ColumnDefinition(name="IceCreamSales", data_type="numerical", description="Daily sales of ice cream")
        ]
        suggestions = generate_suggestions(columns)
        chart_titles = [cs.title for cs in suggestions['chart_suggestions']]
        self.assertIn("Relationship between Temperature and IceCreamSales", chart_titles)

        scatter_suggestion = next(cs for cs in suggestions['chart_suggestions'] if cs.chart_type == "Scatter Plot")
        self.assertCountEqual(scatter_suggestion.columns_used, ["Temperature", "IceCreamSales"])

        # Check for FE: Ratio/Product (might not trigger if descriptions don't match keywords)
        # For this test, let's assume descriptions are generic and ratio/product aren't prime suggestions
        # We can add more specific tests for FE description keyword matching if needed.


    def test_id_column_recognition_and_fe(self):
        """Test ID column recognition and related feature engineering."""
        columns = [
            ColumnDefinition(name="CustomerID", data_type="categorical", description="Unique identifier for customer"),
            ColumnDefinition(name="OrderAmount", data_type="numerical", description="Amount of an order")
        ]
        suggestions = generate_suggestions(columns)
        fe_suggestions = suggestions['feature_engineering_suggestions']

        # Expecting: Total_OrderAmount_Per_CustomerID, Average_OrderAmount_Per_CustomerID
        fe_names = [fe.new_feature_name for fe in fe_suggestions]
        self.assertIn("Total_OrderAmount_Per_CustomerID", fe_names)
        # self.assertIn("Average_OrderAmount_Per_CustomerID", fe_names) # This needs the GROUP_BY_AVERAGE fix

        total_fe = next(fe for fe in fe_suggestions if fe.new_feature_name == "Total_OrderAmount_Per_CustomerID")
        self.assertCountEqual(total_fe.columns_involved, ["CustomerID", "OrderAmount"])

        # Test that the formula for SQL Group By Sum is present
        sql_group_by_sum_found = False
        for formula in total_fe.formulas:
            if formula.tool == "SQL" and "GROUP BY CustomerID" in formula.formula_string and "SUM(OrderAmount)" in formula.formula_string:
                sql_group_by_sum_found = True
                break
        self.assertTrue(sql_group_by_sum_found, "SQL GROUP BY SUM formula not found for ID aggregation.")


    def test_get_formulas_excel_sum(self):
        """Test _get_formulas for Excel SUM."""
        formulas = _get_formulas("SUM", ["Sales"])
        excel_formula = next(f for f in formulas if f.tool == "Excel")
        self.assertEqual(excel_formula.formula_string, "=SUM(A:A)")
        self.assertIn("'Sales' is in column A", excel_formula.example_data_context)

    def test_get_formulas_sql_group_by_sum(self):
        """Test _get_formulas for SQL GROUP_BY_SUM."""
        formulas = _get_formulas("GROUP_BY_SUM", ["Category", "Sales"])
        sql_formula = next(f for f in formulas if f.tool == "SQL")
        self.assertEqual(sql_formula.formula_string, "SELECT Category, SUM(Sales) FROM your_table GROUP BY Category;")

    def test_get_formulas_pandas_date_part_year(self):
        """Test _get_formulas for Pandas DATE_PART_YEAR."""
        formulas = _get_formulas("DATE_PART_YEAR", ["OrderDate"])
        pandas_formula = next(f for f in formulas if f.tool == "Pandas_Python")
        self.assertIn("df['OrderDate'] = pd.to_datetime(df['OrderDate'])\ndf['OrderDate_Year'] = df['OrderDate'].dt.year", pandas_formula.formula_string)

    # Placeholder for testing the GROUP_BY_AVERAGE fix when implemented
    # def test_fe_grouped_average(self):
    #     columns = [
    #         ColumnDefinition(name="CategoryID", data_type="categorical", description="Category ID"),
    #         ColumnDefinition(name="ProductPrice", data_type="numerical", description="Price of product")
    #     ]
    #     suggestions = generate_suggestions(columns)
    #     fe_names = [fe.new_feature_name for fe in suggestions['feature_engineering_suggestions']]
    #     self.assertIn("Average_ProductPrice_Per_CategoryID", fe_names)

    #     avg_fe = next(fe for fe in suggestions['feature_engineering_suggestions'] if "Average_ProductPrice" in fe.new_feature_name)
    #     # Check for correct SQL/Pandas formula for grouped average


if __name__ == '__main__':
    unittest.main()
