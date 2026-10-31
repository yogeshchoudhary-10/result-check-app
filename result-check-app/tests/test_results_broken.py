# tests/test_results_broken.py
# ============================================================
# PURPOSE: Intentional test failure demo for pipeline report.
# This file intentionally contains WRONG assertions to show
# that the CI/CD pipeline halts at the test stage and never
# proceeds to build or push the Docker image.
#
# To demonstrate:
#   1. Rename this to test_results.py (or add to conftest)
#   2. Push to GitHub
#   3. Screenshot the failing pipeline
#   4. Revert to the passing version
# ============================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from results import get_result


class TestIntentionallyBroken:

    def test_BROKEN_wrong_name(self):
        """
        INTENTIONALLY BROKEN: expects wrong name 'John Doe'
        for roll 101, which should be 'Aarav Sharma'.
        This will FAIL and stop the pipeline before build.
        """
        result = get_result("101")
        # ❌ Wrong assertion on purpose
        assert result["name"] == "John Doe", (
            "Pipeline guard: this assertion is intentionally wrong "
            "to demonstrate that CI stops here."
        )

    def test_BROKEN_wrong_marks(self):
        """
        INTENTIONALLY BROKEN: expects marks = 100 for roll 101,
        actual value is 87.
        """
        result = get_result("101")
        # ❌ Wrong marks on purpose
        assert result["marks"] == 100, (
            "Expected 100 but got actual marks — intentional failure."
        )
