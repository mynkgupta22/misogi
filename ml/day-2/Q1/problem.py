# -------------------------------------
# Vector Operations
# -------------------------------------

def add_vectors(a, b):
    """Add two vectors element-wise."""
    if len(a) != len(b):
        raise ValueError("Vectors must be of same length")
    return [a[i] + b[i] for i in range(len(a))]


def dot_product(a, b):
    """Compute the dot product of two vectors."""
    if len(a) != len(b):
        raise ValueError("Vectors must be of same length")
    return sum(a[i] * b[i] for i in range(len(a)))


def are_orthogonal(a, b):
    """Check if two vectors are orthogonal (dot product is zero)."""
    return dot_product(a, b) == 0


# Sample input for vector operations
a = [1, 2, 3]
b = [4, 5, 6]

print("Vector Operations")
print("------------------")
print(f"Sum: {add_vectors(a, b)}")              # Output: [5, 7, 9]
print(f"Dot Product: {dot_product(a, b)}")       # Output: 32
print(f"Orthogonal: {are_orthogonal(a, b)}")     # Output: False


# -------------------------------------
# Matrix Multiplication
# -------------------------------------

def multiply_matrices(A, B):
    """Multiply two matrices A x B."""
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    # Check if matrix multiplication is possible
    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions for matrix multiplication")

    # Initialize result matrix with zeros
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    # Nested loop for matrix multiplication
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):  # or rows_B
                result[i][j] += A[i][k] * B[k][j]
    return result


# Sample input for matrix multiplication
A = [[1, 2],
     [3, 4]]

B = [[5, 6],
     [7, 8]]

print("\nMatrix Multiplication")
print("----------------------")
product = multiply_matrices(A, B)
print("Result:")
for row in product:
    print(row)
# Expected Output:
# [19, 22]
# [43, 50]
