"""
Test correlation matrix logic
"""

import numpy as np

def test_correlation_matrix_sync():
    """Test that correlation matrix syncing works"""
    
    # Initialize
    n_assets = 3
    corr_matrix = np.array([
        [1.0, 0.5, 0.4],
        [0.5, 1.0, 0.25],
        [0.4, 0.25, 1.0]
    ])
    
    print("Initial correlation matrix:")
    print(corr_matrix)
    
    # Simulate user changing (0, 2) from 0.4 to 0.35
    i, j = 0, 2
    new_val = 0.35
    
    print(f"\nUser changes ({i}, {j}) from {corr_matrix[i, j]:.2f} to {new_val:.2f}")
    
    # Update both positions
    corr_matrix[i, j] = new_val
    corr_matrix[j, i] = new_val
    
    print("\nUpdated correlation matrix:")
    print(corr_matrix)
    
    # Verify symmetry
    print("\nVerify symmetry:")
    print(f"corr[{i}, {j}] = {corr_matrix[i, j]:.2f}")
    print(f"corr[{j}, {i}] = {corr_matrix[j, i]:.2f}")
    print(f"Symmetric: {np.allclose(corr_matrix, corr_matrix.T)}")
    
    # Verify diagonal
    print(f"\nDiagonal all 1.0: {np.allclose(np.diag(corr_matrix), 1.0)}")

if __name__ == "__main__":
    test_correlation_matrix_sync()
