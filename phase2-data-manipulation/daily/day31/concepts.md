# Day 31: NumPy Fundamentals — Arrays, Dimensions, Shapes & Dtypes

> **Domain for Concepts:** Meteorological Weather Station Telemetry  
> *(All concepts are illustrated using sensor measurements so you can apply the principles independently to your own tasks.)*

---

## 1. Why NumPy? (The Power of `ndarray`)

Standard Python lists store references to arbitrary objects scattered in memory. This introduces overhead (type checking, pointer dereferencing, cache misses).

NumPy's core object is the **`ndarray`** (N-dimensional array):
- **Contiguous Memory:** Elements are stored in contiguous memory blocks.
- **Homogeneous:** Every element shares the exact same data type (`dtype`), enabling low-level SIMD (Single Instruction, Multiple Data) CPU vectorization.
- **Zero Overhead Loops:** Arithmetic operations are executed at compiled C speed.

```python
import numpy as np

# Python list of hourly sensor temperatures (°C)
temp_list = [21.5, 23.0, 22.8, 19.4, 25.1]

# Convert to a 1D NumPy array
temp_arr = np.array(temp_list, dtype=np.float64)

print(temp_arr)        # [21.5 23.  22.8 19.4 25.1]
print(type(temp_arr))  # <class 'numpy.ndarray'>
```

---

## 2. Array Anatomy: Shape, Dtype, Dimensions & Size

Every `ndarray` possesses essential metadata attributes:

| Attribute | Meaning | Example for 2D Grid (3 stations, 4 readings) |
|:---|:---|:---|
| `.ndim` | Number of array dimensions (axes) | `2` |
| `.shape` | Tuple indicating the size of each dimension `(rows, cols)` | `(3, 4)` |
| `.size` | Total number of elements across all dimensions | `12` |
| `.dtype` | Memory data type of the elements | `float64` or `int32` |
| `.itemsize`| Memory size of a single element in bytes | `8` bytes (for float64) |

```python
# 3 weather stations recording 4 sensor readings each:
# [Temperature, Humidity %, Pressure kPa, Wind Speed km/h]
sensor_telemetry = np.array([
    [24.0, 65.0, 101.3, 12.5],
    [18.5, 82.0, 100.8, 25.0],
    [31.2, 45.0, 101.9,  8.2]
], dtype=np.float32)

print("Dimensions (.ndim):", sensor_telemetry.ndim)   # 2
print("Shape (.shape):", sensor_telemetry.shape)       # (3, 4) -> 3 rows, 4 columns
print("Total elements (.size):", sensor_telemetry.size) # 12
print("Data type (.dtype):", sensor_telemetry.dtype)   # float32
```

---

## 3. Data Types (`dtype`) and Precision Casting

NumPy supports precise numerical types to optimize memory and computation:
- **Integers:** `np.int8`, `np.int16`, `np.int32`, `np.int64`, `np.uint8` (unsigned 0-255, common in images).
- **Floats:** `np.float16`, `np.float32`, `np.float64` (default in Python 64-bit systems).
- **Booleans:** `np.bool_` (`True` / `False`).
- **Strings:** `np.str_` (fixed-width Unicode).

### Explicit Type Casting with `.astype()`:
Converting between data types is done using `.astype()`, which creates a copy of the array with the new dtype:

```python
# Raw barometric readings recorded as floats
barometer_readings = np.array([101.3, 99.8, 102.7, 100.1])

# Cast to integer millibars
integer_mb = barometer_readings.astype(np.int32)
print(integer_mb)        # [101  99 102 100]
print(integer_mb.dtype)  # int32
```

---

## 4. Understanding the `axis` Parameter

The concept of an `axis` in NumPy is fundamental:
- **1D Array:** Has only `axis=0` (traverses along the elements).
- **2D Array:**
  - `axis=0` runs **vertically down columns** (aggregates each column across all rows).
  - `axis=1` runs **horizontally across rows** (aggregates each row across all columns).

```python
# Matrix of 3 stations (rows) x 4 hourly wind measurements (columns):
wind_matrix = np.array([
    [10.0, 15.0, 20.0, 25.0],  # Station A
    [ 5.0,  5.0, 10.0, 10.0],  # Station B
    [30.0, 25.0, 20.0, 15.0]   # Station C
])

# Mean across axis=1 (mean per station across all hours):
station_means = np.mean(wind_matrix, axis=1)
print("Mean per station (axis=1):", station_means)
# Output: [17.5, 7.5, 22.5] (Length = 3)

# Mean across axis=0 (mean per hour across all stations):
hourly_means = np.mean(wind_matrix, axis=0)
print("Mean per hour (axis=0):", hourly_means)
# Output: [15.0, 15.0, 16.666..., 16.666...] (Length = 4)
```

---

## 5. Conditional Vector Mapping (Without Python `for` Loops)

In standard Python, if-else logic on lists requires list comprehensions or loops. In NumPy, conditional categorization is vectorized via `np.where()` or array-based condition lists using `np.select()`:

```python
# Air Quality Index (AQI) values:
aqi_readings = np.array([35, 82, 145, 210, 45, 175])

# Binary classification with np.where(condition, value_if_true, value_if_false):
status_binary = np.where(aqi_readings > 100, "Unhealthy", "Good")
print(status_binary)
# ['Good' 'Good' 'Unhealthy' 'Unhealthy' 'Good' 'Unhealthy']

# Multi-tier categorical classification using np.select:
conditions = [
    aqi_readings <= 50,
    (aqi_readings > 50) & (aqi_readings <= 100),
    aqi_readings > 100
]
tier_labels = ["Low Risk", "Moderate", "Alert"]

classified_tiers = np.select(conditions, tier_labels, default="Unknown")
print(classified_tiers)
# ['Low Risk' 'Moderate' 'Alert' 'Alert' 'Low Risk' 'Alert']
```

---

## 🧠 Key Takeaways for Today

1. `np.array(data, dtype=...)` creates contiguous, homogeneous arrays.
2. Check your array dimensions with `.ndim` and matrix sizing with `.shape`.
3. In 2D arrays, `axis=1` collapses across columns (produces a value per row), while `axis=0` collapses across rows (produces a value per column).
4. Use `np.where()` or `np.select()` for high-performance vectorized categorization without slow Python loops.
