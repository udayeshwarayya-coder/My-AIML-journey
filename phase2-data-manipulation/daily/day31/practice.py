"""
Day 31: NumPy Fundamentals — Array Creation, Shapes, Dtypes & Averages
"""

from typing import List
import numpy as np


def create_marks_array(marks_list: List[List[float]]) -> np.ndarray:
    """
    Converts a 2D list of marks into a 2D float64 NumPy array.
    """
    raise NotImplementedError


def calculate_averages(marks_array: np.ndarray, axis: int = 1) -> np.ndarray:
    """
    Computes mean scores across the given axis, rounded to 2 decimal places.
    """
    raise NotImplementedError


def grade_assign(averages: np.ndarray) -> np.ndarray:
    """
    Assigns letter grades ('A', 'B', 'C', 'D', 'F') to an array of averages.
    Scale: >=90: 'A', >=80: 'B', >=70: 'C', >=60: 'D', <60: 'F'.
    """
    raise NotImplementedError


# =====================================================================
# Tests
# =====================================================================
if __name__ == "__main__":
    print("Testing Day 31...")

    # Test 1: create_marks_array
    raw_data = [
        [85.0, 90.0, 78.0],
        [72.0, 68.0, 80.0],
        [95.0, 92.0, 88.0],
        [58.0, 62.0, 54.0]
    ]
    arr = create_marks_array(raw_data)
    assert isinstance(arr, np.ndarray), "Output must be a numpy ndarray"
    assert arr.shape == (4, 3), f"Expected shape (4, 3), got {arr.shape}"
    assert arr.dtype == np.float64, f"Expected dtype float64, got {arr.dtype}"
    print("✓ create_marks_array passed")

    # Test 2: calculate_averages
    student_avgs = calculate_averages(arr, axis=1)
    assert student_avgs.shape == (4,), f"Expected shape (4,), got {student_avgs.shape}"
    expected_student_avgs = np.array([84.33, 73.33, 91.67, 58.0])
    np.testing.assert_almost_equal(student_avgs, expected_student_avgs, decimal=2)

    subject_avgs = calculate_averages(arr, axis=0)
    assert subject_avgs.shape == (3,), f"Expected shape (3,), got {subject_avgs.shape}"
    expected_subject_avgs = np.array([77.5, 78.0, 75.0])
    np.testing.assert_almost_equal(subject_avgs, expected_subject_avgs, decimal=2)
    print("✓ calculate_averages passed")

    # Test 3: grade_assign
    test_scores = np.array([95.0, 89.9, 80.0, 75.5, 69.9, 60.0, 59.9, 45.0])
    grades = grade_assign(test_scores)
    expected_grades = np.array(['A', 'B', 'B', 'C', 'D', 'D', 'F', 'F'])
    np.testing.assert_array_equal(grades, expected_grades)
    print("✓ grade_assign passed")

    print("\nAll Day 31 tests passed!")
