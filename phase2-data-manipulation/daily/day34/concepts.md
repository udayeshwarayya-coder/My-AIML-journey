# Day 34: NumPy Aggregations & Statistics

> **Domain for Concepts:** Climate Research Station — Monthly Temperature Records
> *(All concepts illustrated using climate data so examples stay fully separate from your practice tasks.)*

---

## 1. Basic Aggregations (Global)

These functions collapse the entire array into a single scalar.

```python
import numpy as np

# Monthly average temperatures (°C) for one year at a research station
monthly_temp = np.array([3.1, 4.2, 8.5, 13.4, 18.7, 23.1,
                          26.4, 25.8, 20.2, 14.1, 7.6, 3.9])

np.sum(monthly_temp)      # 168.9  — total sum
np.mean(monthly_temp)     # 14.075 — arithmetic average
np.min(monthly_temp)      # 3.1    — coldest month
np.max(monthly_temp)      # 26.4   — hottest month
np.std(monthly_temp)      # ~8.18  — spread of temperatures
np.var(monthly_temp)      # ~66.9  — variance (std^2)
```

---

## 2. Axis-Wise Aggregations (2D Arrays)

For 2D arrays, `axis=0` collapses **rows** (result per column), `axis=1` collapses **columns** (result per row).

```
axis=0 : operates DOWN the rows  (per-column result)
axis=1 : operates ACROSS columns (per-row result)
```

```python
# 4 stations x 6 months (Jan-Jun) temperature grid
station_temps = np.array([
    [2.1,  4.5,  9.0, 14.0, 19.2, 24.1],   # Station A
    [5.0,  6.8, 11.2, 16.5, 21.3, 25.8],   # Station B
    [-1.2, 1.0,  6.4, 12.8, 18.0, 22.5],   # Station C
    [3.5,  5.1,  8.9, 13.7, 18.8, 23.6],   # Station D
])

# Mean temperature PER MONTH (across all 4 stations) -> shape (6,)
monthly_mean = np.mean(station_temps, axis=0)
# [2.35, 4.35, 8.875, 14.25, 19.325, 24.0]

# Mean temperature PER STATION (across all 6 months) -> shape (4,)
station_mean = np.mean(station_temps, axis=1)
# [12.15, 14.43, 9.92, 12.27]

# Max temp per station (hottest month each station experienced)
station_max = np.max(station_temps, axis=1)   # [24.1, 25.8, 22.5, 23.6]
```

---

## 3. Cumulative Aggregations

`np.cumsum` and `np.cumprod` build running totals along an axis.

```python
rainfall = np.array([12.3, 8.0, 22.5, 5.1, 18.9, 30.2])

# Running total of rainfall through the months
cumulative_rain = np.cumsum(rainfall)
# [12.3, 20.3, 42.8, 47.9, 66.8, 97.0]

# Cumulative product — useful for growth factors/multipliers
growth_factors = np.array([1.02, 1.05, 0.98, 1.03])
np.cumprod(growth_factors)
# [1.02, 1.071, 1.0496, 1.0811]
```

---

## 4. Percentiles & Quantiles

Percentiles let you understand the distribution without assuming normality.

```python
annual_temps = np.array([3.1, 4.2, 8.5, 13.4, 18.7, 23.1,
                          26.4, 25.8, 20.2, 14.1, 7.6, 3.9])

np.percentile(annual_temps, 25)   # Q1 -> 5.525
np.percentile(annual_temps, 50)   # Q2 -> 13.75 (median)
np.percentile(annual_temps, 75)   # Q3 -> 21.65
np.percentile(annual_temps, 90)   # 90th -> 25.32

# IQR (Interquartile Range) — robust spread measure
iqr = np.percentile(annual_temps, 75) - np.percentile(annual_temps, 25)
# 16.125
```

---

## 5. np.median() vs np.mean()

`median` is robust to outliers; `mean` is sensitive to extremes.

```python
temps_with_outlier = np.array([14, 15, 13, 16, 14, 15, 99])  # 99 = sensor error

np.mean(temps_with_outlier)    # ~26.57 — severely skewed by 99
np.median(temps_with_outlier)  # 15.0   — unaffected by the spike
```

> TIP: When data may have sensor errors or outliers, prefer `median` over `mean`.

---

## 6. np.clip() — Constraining Values to a Range

`np.clip(arr, min_val, max_val)` caps values below `min_val` or above `max_val`.
Useful for outlier removal or range enforcement.

```python
raw_humidity = np.array([45, 102, 78, -5, 88, 110, 60])

# Physical humidity must be 0-100; clip invalid sensor readings
valid_humidity = np.clip(raw_humidity, 0, 100)
# [45, 100, 78, 0, 88, 100, 60]
```

---

## Key Takeaways for Day 34

1. Global aggregations (`sum`, `mean`, `std`, `min`, `max`) return a single scalar.
2. `axis=0` collapses rows (result per column); `axis=1` collapses columns (result per row).
3. `np.cumsum` builds a running total; `np.cumprod` builds a running product.
4. `np.percentile(arr, q)` returns the value below which q% of data falls.
5. Use `median` instead of `mean` when your data may contain outliers.
6. `np.clip(arr, a_min, a_max)` enforces value boundaries element-wise.
