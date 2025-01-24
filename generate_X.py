import numpy as np

def load_matrix(filename):
    """Load a matrix from a CSV file."""
    return np.loadtxt(filename, delimiter=',')

def row_normalize(matrix):
    """Perform row-wise normalization."""
    row_sums = matrix.sum(axis=1, keepdims=True)
    # Avoid division by zero
    row_sums[row_sums == 0] = 1
    return matrix / row_sums

def concatenate_matrices(EP_matrix, C_matrix, In_matrix):
    """
    Concatenate EP, C, and In matrices with row normalization.
    
    Args:
    EP_matrix (np.ndarray): Entrypoint matrix
    C_matrix (np.ndarray): Co-occurrence matrix
    In_matrix (np.ndarray): Inheritance matrix
    
    Returns:
    np.ndarray: Concatenated and row-normalized matrix X
    """
    # Normalize each matrix individually
    EP_normalized = row_normalize(EP_matrix)
    C_normalized = row_normalize(C_matrix)
    In_normalized = row_normalize(In_matrix)
    
    # Concatenate matrices horizontally
    X = np.hstack((EP_normalized, C_normalized, In_normalized))
    
    return X

def save_matrix(matrix, filename):
    """Save matrix to a CSV file."""
    np.savetxt(filename, matrix, delimiter=',')

def main():
    # Load matrices
    EP_matrix = load_matrix('EP_matrix.csv')
    C_matrix = load_matrix('C_matrix.csv')
    In_matrix = load_matrix('inheritance_matrix.csv')
    
    # Concatenate and normalize
    X_matrix = concatenate_matrices(EP_matrix, C_matrix, In_matrix)
    
    # Save concatenated matrix
    save_matrix(X_matrix, 'X_matrix.csv')
    
    # Print dimensions for verification
    print("Dimensions of X matrix:", X_matrix.shape)
    print("Entrypoint matrix columns:", EP_matrix.shape[1])
    print("Co-occurrence matrix columns:", C_matrix.shape[1])
    print("Inheritance matrix columns:", In_matrix.shape[1])

if __name__ == "__main__":
    main()