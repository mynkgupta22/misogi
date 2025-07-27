"""
mlmath - A mini machine learning math utility library

This library provides basic mathematical functions useful for ML and data science:
- dot_product
- matrix_multiply
- conditional_probability
"""

def dot_product(a, b):
    """
    Compute the dot product of two equal-length vectors.

    Args:
        a (list): First vector
        b (list): Second vector

    Returns:
        float: Dot product of a and b

    Raises:
        ValueError: If vectors are not of same length

    Example:
        >>> dot_product([1, 2, 3], [4, 5, 6])
        32
    """
    if len(a) != len(b):
        raise ValueError("Vectors must be of same length")

    return sum(a[i] * b[i] for i in range(len(a)))


def matrix_multiply(A, B):
    """
    Multiply two matrices using nested loops.

    Args:
        A (list of lists): First matrix (m x n)
        B (list of lists): Second matrix (n x p)

    Returns:
        list of lists: Resulting matrix (m x p)

    Raises:
        ValueError: If matrices are not compatible for multiplication

    Example:
        >>> A = [[1, 2], [3, 4]]
        >>> B = [[5, 6], [7, 8]]
        >>> matrix_multiply(A, B)
        [[19, 22], [43, 50]]
    """
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):  # same as rows_B
                result[i][j] += A[i][k] * B[k][j]

    return result


def conditional_probability(events):
    """
    Calculate conditional probability: P(A|B) = P(A and B) / P(B)

    Args:
        events (dict): Dictionary with keys "A_and_B" and "B", values are probabilities (floats)

    Returns:
        float: Conditional probability P(A|B)

    Raises:
        ValueError: If P(B) is zero or missing values

    Example:
        >>> events = {"A_and_B": 0.12, "B": 0.3}
        >>> conditional_probability(events)
        0.4
    """
    try:
        p_a_and_b = events["A_and_B"]
        p_b = events["B"]
        if p_b == 0:
            raise ValueError("P(B) cannot be zero")
        return p_a_and_b / p_b
    except KeyError:
        raise ValueError("Missing required keys: 'A_and_B' and 'B'")

