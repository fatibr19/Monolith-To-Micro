import numpy as np
import json

def row_normalize(matrix):
    """Normalise les lignes de la matrice."""
    row_sums = matrix.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    return matrix / row_sums

def remove_zero_rows(EP_matrix, C_matrix, In_matrix, struct_matrix):
    """Supprime les lignes de zéros et normalise la matrice X."""
    row_mask = ~np.all(EP_matrix == 0, axis=1)
    
    EP_filtered = EP_matrix[row_mask]
    C_filtered = C_matrix[row_mask]
    In_filtered = In_matrix[row_mask]
    struct_filtered = struct_matrix[row_mask][:, row_mask]
    
    n_EP_cols = EP_matrix.shape[1]
    n_C_cols = C_matrix.shape[1]
    
    col_mask_EP = ~np.all(EP_filtered == 0, axis=0)
    col_mask_C = ~np.all(C_filtered == 0, axis=0)
    col_mask_In = ~np.all(In_filtered == 0, axis=0)
    
    EP_filtered = EP_filtered[:, col_mask_EP]
    C_filtered = C_filtered[:, col_mask_C]
    In_filtered = In_filtered[:, col_mask_In]
    
    EP_normalized = row_normalize(EP_filtered)
    C_normalized = row_normalize(C_filtered)
    In_normalized = row_normalize(In_filtered)
    
    X = np.hstack((EP_normalized, C_normalized, In_normalized))
    
    original_row_indices = np.arange(EP_matrix.shape[0])[row_mask]
    original_col_indices = {
        'EP': np.arange(EP_matrix.shape[1])[col_mask_EP],
        'C': np.arange(n_EP_cols, n_EP_cols + n_C_cols)[col_mask_C],
        'In': np.arange(n_EP_cols + n_C_cols, n_EP_cols + n_C_cols + In_matrix.shape[1])[col_mask_In]
    }
    
    index_mapping = {
        'rows': {new_idx: int(orig_idx) for new_idx, orig_idx in enumerate(original_row_indices)},
        'columns': {
            'EP': {new_idx: int(orig_idx) for new_idx, orig_idx in enumerate(original_col_indices['EP'])},
            'C': {new_idx: int(orig_idx) for new_idx, orig_idx in enumerate(original_col_indices['C'])},
            'In': {new_idx: int(orig_idx) for new_idx, orig_idx in enumerate(original_col_indices['In'])}
        }
    }
    
    return X, index_mapping, struct_filtered

def main():
    EP_matrix = np.loadtxt('EP_matrix.csv', delimiter=',')
    C_matrix = np.loadtxt('C_matrix.csv', delimiter=',')
    In_matrix = np.loadtxt('inheritance_matrix.csv', delimiter=',')
    struct_matrix = np.loadtxt('cogcn/cogcn/data/apps/acmeair/struct.csv', delimiter=',')
    
    X, index_mapping, struct_filtered = remove_zero_rows(EP_matrix, C_matrix, In_matrix, struct_matrix)
    
    with open('index_mapping.json', 'w') as f:
        json.dump(index_mapping, f)
    
    np.savetxt('cogcn/cogcn/data/apps/acmeair/content.csv', X, delimiter=',', fmt='%.15f')
    np.savetxt('cogcn/cogcn/data/apps/acmeair/struct.csv', struct_filtered, delimiter=',', fmt='%.15f')
    
    print("Dimensions matrice X :", X.shape)
    print("Dimensions matrice struct :", struct_filtered.shape)

if __name__ == "__main__":
    main()