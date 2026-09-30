"""
Day 33: NumPy Indexing, Slicing, Boolean Masking & Filtering
Domain: Student Grade Engine — Semester Matrix Filtering

LeetCode for today:
  - LC #27 : Remove Element
  - LC #283: Move Zeroes
"""

import numpy as np


def filter_pass_students(
    marks_matrix: np.ndarray, pass_threshold: float
) -> np.ndarray:
    """
    Returns a 2D sub-matrix containing only rows where the student's
    AVERAGE mark across all subjects is >= pass_threshold.

    Parameters:
        marks_matrix   : 2D array of shape (num_students, num_subjects)
        pass_threshold : Minimum average mark to be considered passing

    Returns:
        2D array containing only the passing students' rows.
        Shape: (num_passing_students, num_subjects)

    Hint: You will need to compute row-wise averages first, then build
          a boolean mask from those averages, then apply it.
    """
    return marks_matrix[np.mean(marks_matrix,axis=1)>=pass_threshold]

    # raise NotImplementedError


def top_n_students(
    marks_matrix: np.ndarray, n: int
) -> np.ndarray:
    """
    Returns the rows of the top-n students ranked by their TOTAL marks
    across all subjects (highest first).

    Parameters:
        marks_matrix : 2D array of shape (num_students, num_subjects)
        n            : Number of top students to return

    Returns:
        2D array of shape (n, num_subjects) — top-n rows, sorted descending
        by total marks.

    Hint: Think about how to get the ORDER of rows by their row sums.
          np.argsort returns indices — how do you reverse that order?
          Then use those indices to select rows (fancy indexing).
    """
    scores=np.sum(marks_matrix,axis=1)
    ind=np.argsort(scores)
    return marks_matrix[ind[-n:][::-1]]
    # raise NotImplementedError


def subject_filter(
    marks_matrix: np.ndarray, subject_indices: list
) -> np.ndarray:
    """
    Returns a 2D sub-matrix containing only the specified subject columns,
    for ALL students.

    Parameters:
        marks_matrix    : 2D array of shape (num_students, num_subjects)
        subject_indices : List of integer column indices to extract

    Returns:
        2D array of shape (num_students, len(subject_indices))

    Hint: One clean line using the right indexing style — which type of
          indexing lets you pick arbitrary, non-contiguous columns?
    """
    return marks_matrix[:,subject_indices]
    # raise NotImplementedError


# =====================================================================
# Tests
# =====================================================================
if __name__ == "__main__":
    print("Testing Day 33...")

    # Marks matrix: 6 students x 4 subjects
    marks = np.array([
        [45.0, 52.0, 38.0, 60.0],   # Student 0 — avg 48.75 (fail if threshold=50)
        [78.0, 85.0, 90.0, 88.0],   # Student 1 — avg 85.25
        [50.0, 50.0, 50.0, 50.0],   # Student 2 — avg 50.0  (borderline)
        [30.0, 25.0, 40.0, 35.0],   # Student 3 — avg 32.5  (fail)
        [92.0, 88.0, 95.0, 91.0],   # Student 4 — avg 91.5
        [62.0, 70.0, 68.0, 74.0],   # Student 5 — avg 68.5
    ])

    # --- Test 1: filter_pass_students ---
    passing = filter_pass_students(marks, pass_threshold=50.0)
    assert isinstance(passing, np.ndarray), "Must return ndarray"
    assert passing.shape == (4, 4), f"Expected (4, 4), got {passing.shape}"
    # Students 1, 2, 4, 5 pass (avg >= 50); students 0 and 3 fail
    assert 78.0 in passing[:, 0], "Student 1 (mark 78) should be in result"
    assert 30.0 not in passing[:, 0], "Student 3 (mark 30) must NOT be in result"
    print("[PASSED] filter_pass_students")

    # --- Test 2: top_n_students ---
    top3 = top_n_students(marks, n=3)
    assert isinstance(top3, np.ndarray), "Must return ndarray"
    assert top3.shape == (3, 4), f"Expected (3, 4), got {top3.shape}"
    # Top 3 by total: Student 4 (366), Student 1 (341), Student 5 (274)
    assert top3[0, 0] == 92.0, f"First row should be Student 4, got {top3[0]}"
    assert top3[1, 0] == 78.0, f"Second row should be Student 1, got {top3[1]}"
    assert top3[2, 0] == 62.0, f"Third row should be Student 5, got {top3[2]}"
    print("[PASSED] top_n_students")

    # --- Test 3: subject_filter ---
    # Extract subjects at indices 0 and 3 (first and last)
    filtered = subject_filter(marks, subject_indices=[0, 3])
    assert isinstance(filtered, np.ndarray), "Must return ndarray"
    assert filtered.shape == (6, 2), f"Expected (6, 2), got {filtered.shape}"
    np.testing.assert_array_equal(filtered[:, 0], marks[:, 0])
    np.testing.assert_array_equal(filtered[:, 1], marks[:, 3])

    # Extract only middle two subjects (indices 1 and 2)
    mid_subjects = subject_filter(marks, subject_indices=[1, 2])
    assert mid_subjects.shape == (6, 2), f"Expected (6, 2), got {mid_subjects.shape}"
    np.testing.assert_array_equal(mid_subjects[:, 0], marks[:, 1])
    print("[PASSED] subject_filter")

    print("\nAll Day 33 tests passed!")
