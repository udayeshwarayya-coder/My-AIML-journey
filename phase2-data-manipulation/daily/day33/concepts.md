
# Day 33: Array Indexing, Slicing, Boolean Masking & Filtering

> **Domain for Concepts:** Atmospheric Weather Station — Hourly Sensor Readings
> *(All concepts illustrated using weather data so examples stay fully separate from your practice tasks.)*

---

## 1. Basic Indexing & Slicing

NumPy uses zero-based indexing. For multi-dimensional arrays, each axis is indexed separately using `[row, col]` notation.

### 1D Slicing — `arr[start:stop:step]`

```python
import numpy as np

# 24 hourly temperature readings (°C) from a weather station
hourly_temp = np.array([18, 19, 21, 20, 17, 16, 15, 14, 13, 13, 14, 16,
                         20, 24, 26, 27, 28, 27, 25, 23, 22, 21, 20, 19])

# First 6 hours (midnight to 6 AM)
early_morning = hourly_temp[:6]           # [18, 19, 21, 20, 17, 16]

# Every 3rd hour reading
sparse_sample = hourly_temp[::3]          # [18, 20, 13, 16, 28, 21]

# Last 4 readings reversed
night_reversed = hourly_temp[-4:][::-1]   # [19, 20, 21, 22]
```

### 2D Slicing — `arr[row_slice, col_slice]`

```python
# 5 days x 6 sensor columns: temp, humidity, wind, pressure, UV, rain
station_matrix = np.array([
    [22.1, 68, 12.4, 1013, 3, 0.0],
    [24.3, 72,  8.1, 1010, 5, 2.3],
    [19.8, 85, 15.2, 1008, 1, 8.7],
    [26.5, 60,  5.0, 1015, 7, 0.0],
    [23.0, 74, 10.8, 1012, 4, 1.1],
])

# All rows, only temperature and humidity (columns 0 and 1)
temp_humidity = station_matrix[:, :2]

# Rows 1-3, wind and pressure (columns 2 and 3)
mid_wind_pres = station_matrix[1:4, 2:4]

# Every 2nd day UV index (column 4)
alt_day_uv = station_matrix[::2, 4]     # [3, 1, 4]
```

---

## 2. Boolean Masking

A boolean mask is an array of True/False values the same shape as the original.
Indexing with a mask returns only elements where the condition is True.

```python
# Hourly wind speed readings (km/h)
wind_speed = np.array([12, 8, 25, 34, 19, 5, 42, 38, 22, 10])

# Mask: True where wind exceeds 20 km/h
strong_wind_mask = wind_speed > 20
# [False, False, True, True, False, False, True, True, True, False]

# Apply mask to extract matching values
strong_winds = wind_speed[strong_wind_mask]        # [25, 34, 42, 38, 22]

# Compound conditions — wrap each in ()
moderate = wind_speed[(wind_speed >= 15) & (wind_speed <= 30)]   # [25, 19, 22]
extreme  = wind_speed[(wind_speed > 35) | (wind_speed < 6)]      # [5, 42, 38]
```

> WARNING: Always wrap each condition in () when using & or |.
> Using Python's `and`/`or` directly on arrays raises a ValueError.

---

## 3. np.where() — Vectorized Conditional Selection

np.where(condition, value_if_true, value_if_false) applies element-wise without any loop.

```python
rainfall = np.array([0.0, 2.3, 8.7, 0.0, 1.1, 15.4, 0.0, 6.2])

# Label days
labels = np.where(rainfall > 0, "Rainy", "Dry")
# ['Dry', 'Rainy', 'Rainy', 'Dry', 'Rainy', 'Rainy', 'Dry', 'Rainy']

# Cap extreme readings at 10mm
capped = np.where(rainfall > 10, 10.0, rainfall)
# [0.0, 2.3, 8.7, 0.0, 1.1, 10.0, 0.0, 6.2]
```

---

## 4. Fancy (Advanced) Indexing

Fancy indexing uses an integer array to select elements at arbitrary positions
(not necessarily contiguous). It ALWAYS returns a copy, never a view.

```python
hourly_temp = np.array([18, 19, 21, 20, 17, 16, 15, 14, 13, 13,
                         14, 16, 20, 24, 26, 27, 28, 27, 25, 23, 22, 21, 20, 19])

# Pick readings at specific hours of interest
peak_hours = [6, 12, 16, 20]
peak_temps = hourly_temp[peak_hours]     # [15, 20, 27, 22]

# 2D: select specific rows by a list of indices
station_matrix = np.array([
    [22.1, 68, 12.4],
    [24.3, 72,  8.1],
    [19.8, 85, 15.2],
    [26.5, 60,  5.0],
    [23.0, 74, 10.8],
])
selected_days = station_matrix[[0, 2, 4]]   # rows 0, 2, 4 only
```

> TIP: Slicing (arr[1:4]) returns a VIEW. Fancy indexing (arr[[1,2,4]]) returns a COPY.

---

## 5. Getting Index Positions: argmax, argmin, argsort

When you need WHERE a value is, not just what it is.

```python
pressure = np.array([1013, 1008, 1005, 1015, 1010, 1003, 1012])

np.argmax(pressure)    # 3  -> index of highest pressure day
np.argmin(pressure)    # 5  -> index of lowest pressure day
np.argsort(pressure)   # [5, 2, 1, 4, 6, 0, 3] -> indices that would sort the array
```

---

## Key Takeaways for Day 33

1. arr[start:stop:step] for slicing; arr[row, col] syntax for 2D.
2. Boolean masks use conditions and combine with & / | inside ().
3. np.where(cond, x, y) is a vectorized if-else with zero loops.
4. Fancy indexing with an integer array always returns a COPY (not a view).
5. np.argmax / np.argmin / np.argsort return INDEX positions, not values.
