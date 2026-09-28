# Day 32: Reshaping, Flattening, Transposing & Memory Strides

> **Domain for Concepts:** Satellite Multispectral Sensor Imagery & Thermal Tile Scanning  
> *(All concepts are illustrated using spatial pixel bands so you can apply the principles independently to your own tasks.)*

---

## 1. Array Reshaping (`.reshape()`)

Reshaping changes the dimensional organization of elements without altering their underlying data or order in memory.

### Key Rules of Reshaping:
1. **Conservation of Elements:** The product of the new shape dimensions MUST equal `array.size`.
   - e.g., An array with 12 elements can be shaped into `(3, 4)`, `(4, 3)`, `(2, 6)`, `(2, 2, 3)`, or `(12,)`.
2. **Dimension Inference with `-1`:** You can specify `-1` for at most ONE dimension, and NumPy will automatically compute its size:
   ```python
   data = np.arange(12) # size 12
   matrix = data.reshape(3, -1) # NumPy infers 12 / 3 = 4 columns -> (3, 4)
   ```

### Satellite Grid Example:
```python
import numpy as np

# A raw 1D stream of 12 thermal telemetry values from a drone scan
raw_sensor_stream = np.array([18.2, 19.1, 21.0, 22.4, 23.5, 24.1, 20.8, 19.9, 18.7, 17.5, 16.9, 17.2])

# Reshape into a 2D spatial grid: 3 scan lines (rows) x 4 sensor columns
thermal_tile = raw_sensor_stream.reshape(3, 4)
print("Thermal Tile (3x4):\n", thermal_tile)
print("Shape:", thermal_tile.shape) # (3, 4)
```

---

## 2. Flattening Arrays: `flatten()` vs `ravel()`

When converting multi-dimensional arrays back to 1D, NumPy provides two methods with a critical distinction:

| Method | Returns | Memory Impact | Modifying result affects original? |
|:---|:---|:---|:---:|
| **`arr.flatten()`** | **Copy** (deep clone) | Allocates new memory | ❌ No |
| **`arr.ravel()`** | **View** (shallow reference) | Zero memory allocation (fast) | ⚠️ **Yes** |

### Code Demonstration:
```python
grid = np.array([[10, 20], [30, 40]])

# 1. Using flatten() -> creates a copy
flat_copy = grid.flatten()
flat_copy[0] = 999
print("Original after flatten edit:", grid[0, 0])  # Still 10 (unaffected)

# 2. Using ravel() -> creates a view
flat_view = grid.ravel()
flat_view[0] = 999
print("Original after ravel edit:", grid[0, 0])    # Changed to 999!
```

> 💡 **Best Practice:** Use `.ravel()` when reading or aggregating to avoid memory overhead. Use `.flatten()` when you plan to modify values in-place without corrupting the source dataset.

---

## 3. Transposing Arrays (`.T` and `np.transpose()`)

Transposition flips an array over its diagonal, switching its axes:
- For a 2D matrix of shape `(M, N)`, `matrix.T` results in shape `(N, M)`.
- Row `i` becomes Column `i`.

```python
# Multispectral Satellite Bands: 2 Spectral Channels (Red, NIR) x 3 Spatial Zones
# Channel 0: [0.45, 0.48, 0.52]
# Channel 1: [0.78, 0.82, 0.85]
spectral_bands = np.array([
    [0.45, 0.48, 0.52],
    [0.78, 0.82, 0.85]
])
print("Original Shape (Channels x Zones):", spectral_bands.shape) # (2, 3)

# Transpose so each row represents a Spatial Zone with its 2 channel values
spatial_observations = spectral_bands.T
print("Transposed Shape (Zones x Channels):", spatial_observations.shape) # (3, 2)
print("Zone 0 channels:", spatial_observations[0]) # [0.45, 0.78]
```

---

## 4. Memory Layout & Order: C-Order vs Fortran-Order

NumPy arrays in memory are stored linearly (1D sequential addresses). How 2D coordinates map to 1D memory depends on the order:
- **C-contiguous (`order='C'`):** Row-major (default in C/Python). Consecutive elements of a row are adjacent in memory.
- **Fortran-contiguous (`order='F'`):** Column-major (default in Fortran/MATLAB/R). Consecutive elements of a column are adjacent in memory.

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])

print(matrix.flatten(order='C'))  # [1, 2, 3, 4, 5, 6] (Row by row)
print(matrix.flatten(order='F'))  # [1, 4, 2, 5, 3, 6] (Column by column)
```

---

## 🧠 Key Takeaways for Day 32

1. `.reshape(rows, cols)` preserves data size (`rows * cols == size`).
2. Use `-1` to let NumPy automatically calculate an ambiguous dimension.
3. Use `.ravel()` for high-speed zero-copy 1D flattening; use `.flatten()` when isolation/copying is required.
4. `.T` (or `np.transpose(arr)`) swaps axes, converting rows to columns and vice versa.
