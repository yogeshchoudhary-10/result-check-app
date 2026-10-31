# results.py - Core result data and lookup logic
# This module is kept separate so it can be independently unit-tested.

RESULTS_DB = {
    "101": {"name": "Aarav Sharma",   "marks": 87, "grade": "A", "status": "Pass"},
    "102": {"name": "Priya Patel",    "marks": 72, "grade": "B", "status": "Pass"},
    "103": {"name": "Rohit Mehta",    "marks": 95, "grade": "A+","status": "Pass"},
    "104": {"name": "Sneha Iyer",     "marks": 58, "grade": "C", "status": "Pass"},
    "105": {"name": "Karan Joshi",    "marks": 34, "grade": "F", "status": "Fail"},
    "106": {"name": "Ananya Singh",   "marks": 81, "grade": "A", "status": "Pass"},
    "107": {"name": "Vikram Nair",    "marks": 66, "grade": "B", "status": "Pass"},
    "108": {"name": "Divya Reddy",    "marks": 49, "grade": "D", "status": "Pass"},
    "109": {"name": "Arjun Gupta",    "marks": 90, "grade": "A+","status": "Pass"},
    "110": {"name": "Meera Bose",     "marks": 77, "grade": "B", "status": "Pass"},
}


def get_result(roll_number: str):
    """
    Look up a student result by roll number.

    Args:
        roll_number (str): The student's roll number.

    Returns:
        dict: A dictionary with keys 'name', 'marks', 'grade', 'status'
              if the roll number exists, otherwise None.
    """
    roll_number = str(roll_number).strip()
    return RESULTS_DB.get(roll_number, None)


def get_grade_label(grade: str) -> str:
    """
    Return a human-readable label for a grade letter.
    """
    labels = {
        "A+": "Outstanding",
        "A":  "Excellent",
        "B":  "Good",
        "C":  "Average",
        "D":  "Below Average",
        "F":  "Fail",
    }
    return labels.get(grade, "Unknown")


def get_all_roll_numbers() -> list:
    """Return a sorted list of all registered roll numbers."""
    return sorted(RESULTS_DB.keys())
