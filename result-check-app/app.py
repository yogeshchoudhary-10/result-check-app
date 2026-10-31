# app.py - Flask application for Result-Check Website
from flask import Flask, render_template, request, redirect, url_for
from results import get_result, get_grade_label

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Home page — displays the roll number input form."""
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    """
    Handle form submission.
    Look up the roll number and render the result page.
    """
    roll_number = request.form.get("roll_number", "").strip()

    if not roll_number:
        return render_template(
            "index.html",
            error="Please enter a roll number."
        )

    student = get_result(roll_number)

    if student is None:
        return render_template(
            "index.html",
            error=f"No record found for roll number: {roll_number}",
            searched=roll_number
        )

    grade_label = get_grade_label(student["grade"])
    return render_template(
        "result.html",
        roll_number=roll_number,
        student=student,
        grade_label=grade_label
    )


@app.route("/health", methods=["GET"])
def health():
    """Health-check endpoint used by the deploy stage."""
    return {"status": "ok", "service": "result-check-app"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
