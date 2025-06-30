import unittest
from fastapi.testclient import TestClient
from main import app # Assuming your FastAPI app instance is named 'app' in main.py
from app.data_models import ColumnDefinition, SuggestionOutput # For response validation

class TestMainAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_root_health_check(self):
        """Test the root endpoint health check."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "iviz API is running!"})

    def test_generate_ideas_empty_input(self):
        """Test /generate-ideas/ with an empty list of columns."""
        response = self.client.post("/generate-ideas/", json=[])
        self.assertEqual(response.status_code, 400) # Expecting bad request
        self.assertIn("No columns provided", response.json()["detail"])

    def test_generate_ideas_valid_input(self):
        """Test /generate-ideas/ with valid column definitions."""
        columns_data = [
            {"name": "Sales", "data_type": "numerical", "description": "Total sales amount"},
            {"name": "Region", "data_type": "categorical", "description": "Sales region"}
        ]
        response = self.client.post("/generate-ideas/", json=columns_data)
        self.assertEqual(response.status_code, 200)

        # Validate response structure using Pydantic model
        response_data = response.json()
        try:
            SuggestionOutput(**response_data)
        except Exception as e:
            self.fail(f"Response validation failed: {e}")

        # Basic checks on content (more detailed checks are in unit tests)
        self.assertIn("chart_suggestions", response_data)
        self.assertIn("feature_engineering_suggestions", response_data)
        self.assertIn("metric_card_suggestions", response_data)

        self.assertTrue(len(response_data["chart_suggestions"]) > 0)
        # Example: Check if a specific chart title is present based on input
        # This depends on the exact rules in suggestion_engine
        chart_titles = [cs["title"] for cs in response_data["chart_suggestions"]]
        self.assertIn("Sales by Region", chart_titles)


    def test_generate_ideas_invalid_column_data_type(self):
        """Test /generate-ideas/ with an invalid data_type in one column."""
        columns_data = [
            {"name": "Sales", "data_type": "numericc", "description": " typo in numerical"}, # Invalid data_type
            {"name": "Region", "data_type": "categorical", "description": "Sales region"}
        ]
        response = self.client.post("/generate-ideas/", json=columns_data)
        self.assertEqual(response.status_code, 422) # Unprocessable Entity due to Pydantic validation
        # FastAPI's default 422 error provides details about the validation error
        # We can check for presence of error details
        self.assertIn("detail", response.json())
        self.assertTrue(any("Input should be 'numerical', 'categorical', 'date', 'text' or 'boolean'" in err["msg"]
                            for err in response.json()["detail"]))


    def test_generate_ideas_missing_field(self):
        """Test /generate-ideas/ with a missing required field in one column."""
        columns_data = [
            {"name": "Sales", "description": "Missing data_type"}, # Missing data_type
            {"name": "Region", "data_type": "categorical", "description": "Sales region"}
        ]
        response = self.client.post("/generate-ideas/", json=columns_data)
        self.assertEqual(response.status_code, 422) # Unprocessable Entity
        self.assertIn("detail", response.json())
        self.assertTrue(any(err["type"] == "missing" and "data_type" in err["loc"]
                            for err in response.json()["detail"]))

    def test_options_generate_ideas_cors_preflight(self):
        """Test the OPTIONS request for /generate-ideas/ (CORS preflight)."""
        headers = {
            "Origin": "http://example.com",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        }
        response = self.client.options("/generate-ideas/", headers=headers) # Add headers
        self.assertEqual(response.status_code, 200)
        self.assertIn("access-control-allow-origin", response.headers)
        self.assertIn("access-control-allow-methods", response.headers)
        self.assertIn("access-control-allow-headers", response.headers)
        # Check that the actual origin is reflected or * if allow_origins=["*"]
        self.assertTrue(response.headers["access-control-allow-origin"] == "http://example.com" or \
                        response.headers["access-control-allow-origin"] == "*")


if __name__ == '__main__':
    unittest.main()
