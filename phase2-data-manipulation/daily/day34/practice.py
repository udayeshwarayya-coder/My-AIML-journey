"""
Day 34: NumPy Aggregations & Statistics
Domain: Student Grade Engine - Score Analysis & Normalization

LeetCode for today:
  - LC #53 : Maximum Subarray
  - LC #152: Maximum Product Subarray
"""

import numpy as np


def subject_statistics(marks_matrix: np.ndarray) -> dict:
    """
    Computes per-subject statistics across all students.

    Parameters:
        marks_matrix : 2D array of shape (num_students, num_subjects)

    Returns:
        A dict with keys: 'mean', 'std', 'min', 'max'
        Each value is a 1D array of shape (num_subjects,) computed along axis=0.

    Example:
        marks = [[80, 70], [90, 60]]
        -> mean = [85.0, 65.0], std = [5.0, 5.0], min = [80, 60], max = [90, 70]
    """
    raise NotImplementedError


def top_subject_per_student(marks_matrix: np.ndarray) -> np.ndarray:
    """
    Returns the INDEX of the best-scoring subject for each student.

    Parameters:
        marks_matrix : 2D array of shape (num_students, num_subjects)

    Returns:
        1D array of shape (num_students,) - column index of the highest mark per row.

    Example:
        marks = [[70, 90, 80], [85, 60, 95]]
        -> [1, 2]
    """
    raise NotImplementedError


def normalize_marks(marks_matrix: np.ndarray) -> np.ndarray:
    """
    Normalizes each student's marks to a 0-100 scale using min-max normalization.
    Normalization is done PER STUDENT (row-wise), not globally.

    Formula:
        normalized = (row - row_min) / (row_max - row_min) * 100

    Parameters:
        marks_matrix : 2D array of shape (num_students, num_subjects)

    Returns:
        2D array of same shape with values in range [0.0, 100.0].

    Hint: mind broadcasting when subtracting row-wise min/max.
    """
    raise NotImplementedError


def grade_distribution(marks_matrix: np.ndarray) -> np.ndarray:
    """
    Clips all marks to [0, 100], then returns the cumulative sum of all
    marks (flattened) sorted in ascending order.

    Parameters:
        marks_matrix : 2D array of shape (num_students, num_subjects)

    Returns:
        1D array - cumulative sum of sorted clipped marks.
    """
    raise NotImplementedError


# =====================================================================
# Tests
# =====================================================================
if __name__ == "__main__":
    print("Testing Day 34...")

    marks = np.array([
        [72.0, 88.0, 65.0, 90.0],   # Student 0
        [95.0, 78.0, 82.0, 70.0],   # Student 1
        [60.0, 55.0, 50.0, 45.0],   # Student 2
        [85.0, 92.0, 88.0, 96.0],   # Student 3
        [40.0, 105.0, 78.0, -5.0],  # Student 4 - has invalid values for clip test
    ])

    # --- Test 1: subject_statistics ---
    stats = subject_statistics(marks)
    assert isinstance(stats, dict), "Must return a dict"
    assert set(stats.keys()) == {"mean", "std", "min", "max"}, "Keys must be mean, std, min, max"
    for key in stats:
        assert stats[key].shape == (4,), f"stats['{key}'] must have shape (4,)"
    np.testing.assert_almost_equal(stats["mean"][0], np.mean(marks[:, 0]))
    np.testing.assert_almost_equal(stats["min"][3],  np.min(marks[:, 3]))
    np.testing.assert_almost_equal(stats["max"][1],  np.max(marks[:, 1]))
    print("[PASSED] subject_statistics")

    # --- Test 2: top_subject_per_student ---
    best = top_subject_per_student(marks)
    assert isinstance(best, np.ndarray), "Must return ndarray"
    assert best.shape == (5,), f"Expected shape (5,), got {best.shape}"
    assert best[0] == 3, f"Student 0's best subject is index 3 (90), got {best[0]}"
    assert best[1] == 0, f"Student 1's best subject is index 0 (95), got {best[1]}"
    assert best[3] == 3, f"Student 3's best subject is index 3 (96), got {best[3]}"
    print("[PASSED] top_subject_per_student")

    # --- Test 3: normalize_marks ---
    clean_marks = marks[:4]   # exclude student 4 for normalization test
    normed = normalize_marks(clean_marks)
    assert isinstance(normed, np.ndarray), "Must return ndarray"
    assert normed.shape == clean_marks.shape, "Shape must be preserved"
    row_mins = np.min(normed, axis=1)
    row_maxs = np.max(normed, axis=1)
    np.testing.assert_array_almost_equal(row_mins, np.zeros(4))
    np.testing.assert_array_almost_equal(row_maxs, np.full(4, 100.0))
    print("[PASSED] normalize_marks")

    # --- Test 4: grade_distribution ---
    dist = grade_distribution(marks)
    assert isinstance(dist, np.ndarray), "Must return ndarray"
    assert dist.ndim == 1, "Must be 1D"
    assert dist.shape[0] == marks.size, f"Expected {marks.size} elements, got {dist.shape[0]}"
    assert np.all(np.diff(dist) >= 0), "Cumulative sum must be non-decreasing"
    clipped_sorted = np.sort(np.clip(marks, 0, 100).ravel())
    np.testing.assert_almost_equal(dist[0], clipped_sorted[0])
    print("[PASSED] grade_distribution")

    print("\nAll Day 34 tests passed!")
