from app.services.analysis import process_year
from app.services.change_detection import (
    detect_change,
    calculate_change_statistics,
)


# ==========================================
# 2021
# ==========================================

result_2021 = process_year(
    "data/2021/B04-21.jp2",
    "data/2021/B08-21.jp2",
    "data/2021/SCL.jp2",
)


# ==========================================
# 2026
# ==========================================

result_2026 = process_year(
    "data/2026/B04-26.jp2",
    "data/2026/B08-26.jp2",
    "data/2026/SCL-26.jp2",
)


# ==========================================
# Print yearly results
# ==========================================

print("\n========== YEARLY RESULTS ==========")

print(
    f"2021 vegetation candidate: "
    f"{result_2021['vegetation_percentage']:.2f}%"
)

print(
    f"2026 vegetation candidate: "
    f"{result_2026['vegetation_percentage']:.2f}%"
)


# ==========================================
# Change detection
# ==========================================

change_map = detect_change(
    result_2021["vegetation_mask"],
    result_2026["vegetation_mask"],
)


# ==========================================
# Statistics
# ==========================================

stats = calculate_change_statistics(
    change_map
)


print("\n========== CHANGE RESULTS ==========")

print(
    f"Loss pixels: "
    f"{stats['loss_pixels']}"
)

print(
    f"Stable pixels: "
    f"{stats['stable_pixels']}"
)

print(
    f"Gain pixels: "
    f"{stats['gain_pixels']}"
)

print(
    f"Loss percentage: "
    f"{stats['loss_percentage']:.2f}%"
)

print(
    f"Stable percentage: "
    f"{stats['stable_percentage']:.2f}%"
)

print(
    f"Gain percentage: "
    f"{stats['gain_percentage']:.2f}%"
)