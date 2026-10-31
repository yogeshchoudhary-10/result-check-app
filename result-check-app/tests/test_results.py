# tests/test_results.py
# Unit tests for the results.py module.
# Run with:  pytest tests/ -v

import sys
import os

# Ensure the parent directory (app root) is on the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from results import get_result, get_grade_label, get_all_roll_numbers


# ---------------------------------------------------------------------------
# TEST 1: Valid roll number returns correct student data
# ---------------------------------------------------------------------------
class TestGetResultValid:

    def test_valid_roll_returns_dict(self):
        """A known roll number must return a non-None dictionary."""
        result = get_result("101")
        assert result is not None, "Expected a result dict, got None"

    def test_valid_roll_has_required_keys(self):
        """Result dict must contain name, marks, grade, and status."""
        result = get_result("101")
        for key in ("name", "marks", "grade", "status"):
            assert key in result, f"Missing key: {key}"

    def test_valid_roll_correct_name(self):
        """Roll 101 should map to Aarav Sharma."""
        result = get_result("101")
        assert result["name"] == "Aarav Sharma"

    def test_valid_roll_correct_marks(self):
        """Roll 101 should have 87 marks."""
        result = get_result("101")
        assert result["marks"] == 87

    def test_valid_roll_correct_grade(self):
        """Roll 101 should have grade A."""
        result = get_result("101")
        assert result["grade"] == "A"

    def test_valid_roll_pass_status(self):
        """Roll 101 should have status Pass."""
        result = get_result("101")
        assert result["status"] == "Pass"

    def test_another_valid_roll(self):
        """Roll 103 should return Rohit Mehta with A+ grade."""
        result = get_result("103")
        assert result is not None
        assert result["name"] == "Rohit Mehta"
        assert result["grade"] == "A+"

    def test_fail_student(self):
        """Roll 105 should have status Fail."""
        result = get_result("105")
        assert result is not None
        assert result["status"] == "Fail"
        assert result["grade"] == "F"

    def test_roll_number_as_integer_string(self):
        """Roll numbers passed with spaces should still resolve correctly."""
        result = get_result("  102  ")
        assert result is not None
        assert result["name"] == "Priya Patel"


# ---------------------------------------------------------------------------
# TEST 2: Invalid roll number returns None
# ---------------------------------------------------------------------------
class TestGetResultInvalid:

    def test_unknown_roll_returns_none(self):
        """A roll number not in the DB must return None."""
        result = get_result("999")
        assert result is None

    def test_empty_string_returns_none(self):
        """An empty string must return None."""
        result = get_result("")
        assert result is None

    def test_alphabetic_roll_returns_none(self):
        """A non-numeric roll number must return None."""
        result = get_result("ABC")
        assert result is None

    def test_none_like_string_returns_none(self):
        """Roll number 'None' (string) must return None."""
        result = get_result("None")
        assert result is None

    def test_negative_roll_returns_none(self):
        """A negative number string must return None."""
        result = get_result("-1")
        assert result is None


# ---------------------------------------------------------------------------
# TEST 3: get_grade_label
# ---------------------------------------------------------------------------
class TestGetGradeLabel:

    def test_a_plus_label(self):
        assert get_grade_label("A+") == "Outstanding"

    def test_a_label(self):
        assert get_grade_label("A") == "Excellent"

    def test_b_label(self):
        assert get_grade_label("B") == "Good"

    def test_c_label(self):
        assert get_grade_label("C") == "Average"

    def test_d_label(self):
        assert get_grade_label("D") == "Below Average"

    def test_f_label(self):
        assert get_grade_label("F") == "Fail"

    def test_unknown_grade(self):
        assert get_grade_label("Z") == "Unknown"


# ---------------------------------------------------------------------------
# TEST 4: get_all_roll_numbers
# ---------------------------------------------------------------------------
class TestGetAllRollNumbers:

    def test_returns_list(self):
        rolls = get_all_roll_numbers()
        assert isinstance(rolls, list)

    def test_list_not_empty(self):
        rolls = get_all_roll_numbers()
        assert len(rolls) > 0

    def test_list_is_sorted(self):
        rolls = get_all_roll_numbers()
        assert rolls == sorted(rolls)

    def test_known_roll_in_list(self):
        rolls = get_all_roll_numbers()
        assert "101" in rolls


# ---------------------------------------------------------------------------
# TEST 5: Flask app routes (integration-style with test client)
# ---------------------------------------------------------------------------
@pytest.fixture
def client():
    """Provide a Flask test client."""
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestFlaskRoutes:

    def test_home_page_returns_200(self, client):
        """GET / must return HTTP 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_home_page_contains_form(self, client):
        """Home page must contain a form element."""
        response = client.get("/")
        assert b"form" in response.data.lower()

    def test_result_post_valid_roll(self, client):
        """POST /result with roll 101 must return 200 and student name."""
        response = client.post("/result", data={"roll_number": "101"})
        assert response.status_code == 200
        assert b"Aarav Sharma" in response.data

    def test_result_post_invalid_roll(self, client):
        """POST /result with unknown roll must show error message."""
        response = client.post("/result", data={"roll_number": "999"})
        assert response.status_code == 200
        assert b"999" in response.data  # error message mentions the roll

    def test_result_post_empty_roll(self, client):
        """POST /result with empty roll must show error."""
        response = client.post("/result", data={"roll_number": ""})
        assert response.status_code == 200
        assert b"enter" in response.data.lower()

    def test_health_endpoint(self, client):
        """GET /health must return 200 with ok status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
