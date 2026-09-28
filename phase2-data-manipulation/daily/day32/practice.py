"""
Day 32: NumPy Reshaping, Flattening, Transposing & Memory Strides
Domain: Student Grade Engine — Semester Matrix Restructuring
"""

import numpy as np


def reshape_semester_data(
    flat_marks: np.ndarray, num_students: int, num_subjects: int
) -> np.ndarray:
    """
    Reshapes a flat 1D array of semester marks into a 2D matrix of shape (num_students, num_subjects).

    Raises:
        ValueError: If the total number of elements does not match num_students * num_subjects.
    """
    raise NotImplementedError


def flatten_all_marks(
    marks_tensor: np.ndarray, return_copy: bool = True
) -> np.ndarray:
    """
    Flattens a multi-dimensional array of marks into a 1D array.

    Parameters:
        marks_tensor (np.ndarray): Multi-dimensional array of marks.
        return_copy (bool): If True, modifications to the returned array must not
                            affect the original array. If False, the returned array
                            must share memory with the original array.
    """
    raise NotImplementedError


def subject_wise_view(marks_matrix: np.ndarray) -> np.ndarray:
    """
    Converts a 2D student-major marks matrix of shape (num_students, num_subjects)
    into a subject-major matrix of shape (num_subjects, num_students).
    """
    raise NotImplementedError


# =====================================================================
# Tests
# =====================================================================
if __name__ == "__main__":
    print("Testing Day 32...")

    # Test 1: reshape_semester_data
    flat_data = np.array([85.0, 90.0, 78.0, 92.0, 88.0, 76.0, 60.0, 75.0, 80.0, 95.0, 89.0, 94.0])
    reshaped = reshape_semester_data(flat_data, num_students=4, num_subjects=3)
    assert isinstance(reshaped, np.ndarray), "Output must be a numpy ndarray"
    assert reshaped.shape == (4, 3), f"Expected shape (4, 3), got {reshaped.shape}"
    assert reshaped[0, 0] == 85.0 and reshaped[3, 2] == 94.0, "Values do not match expected positions"

    # Test 1b: dimension mismatch validation
    try:
        reshape_semester_data(flat_data, num_students=5, num_subjects=3)
        assert False, "Should have raised ValueError for mismatched element count"
    except ValueError:
        pass
    print("[PASSED] reshape_semester_data")

    # Test 2: flatten_all_marks (copy vs view)
    source_matrix = np.array([[10.0, 20.0], [30.0, 40.0]])

    # Copy check
    flat_copy = flatten_all_marks(source_matrix, return_copy=True)
    assert flat_copy.shape == (4,), f"Expected shape (4,), got {flat_copy.shape}"
    flat_copy[0] = 999.0
    assert source_matrix[0, 0] == 10.0, "Modifying copy should NOT affect original matrix"

    # View check
    flat_view = flatten_all_marks(source_matrix, return_copy=False)
    assert flat_view.shape == (4,), f"Expected shape (4,), got {flat_view.shape}"
    flat_view[0] = 777.0
    assert source_matrix[0, 0] == 777.0, "Modifying view MUST affect original matrix"
    print("[PASSED] flatten_all_marks")

    # Test 3: subject_wise_view
    test_marks = np.array([
        [85.0, 90.0, 78.0],
        [72.0, 68.0, 80.0],
        [95.0, 92.0, 88.0],
        [58.0, 62.0, 54.0]
    ])  # Shape: (4 students, 3 subjects)
    subject_view = subject_wise_view(test_marks)
    assert subject_view.shape == (3, 4), f"Expected shape (3, 4), got {subject_view.shape}"
    # Row 0 of subject_view should be subject 0 scores across all 4 students: [85, 72, 95, 58]
    expected_subj_0 = np.array([85.0, 72.0, 95.0, 58.0])
    np.testing.assert_array_equal(subject_view[0], expected_subj_0)
    print("[PASSED] subject_wise_view")

    print("\nAll Day 32 tests passed!")
