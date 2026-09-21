from app.services.visualization import create_change_image
from app.services.analysis import process_year

from app.services.change_detection import (
    detect_change,
    calculate_change_statistics,
)

from app.services.geotiff import save_change_map


# =========================
# 2021
# =========================

result_2021 = process_year(
    "data/2021/B04-21.jp2",
    "data/2021/B08-21.jp2",
    "data/2021/SCL.jp2",
)


# =========================
# 2026
# =========================

result_2026 = process_year(
    "data/2026/B04-26.jp2",
    "data/2026/B08-26.jp2",
    "data/2026/SCL-26.jp2",
)


# =========================
# YEARLY RESULTS
# =========================

print("\n========== YEARLY RESULTS ==========")

print(
    f"2021 vegetation candidate: "
    f"{result_2021['vegetation_percentage']:.2f}%"
)

print(
    f"2026 vegetation candidate: "
    f"{result_2026['vegetation_percentage']:.2f}%"
)


# =========================
# COMMON VALID AREA
# =========================

common_valid_mask = (
    result_2021["valid_mask"] &
    result_2026["valid_mask"]
)

print("\n========== VALID PIXELS ==========")

print(
    f"2021 valid pixels: "
    f"{result_2021['valid_pixels']}"
)

print(
    f"2026 valid pixels: "
    f"{result_2026['valid_pixels']}"
)

print(
    f"Common valid pixels: "
    f"{int(common_valid_mask.sum())}"
)


# =========================
# CHANGE DETECTION
# =========================

change_map = detect_change(
    result_2021["vegetation_mask"],
    result_2026["vegetation_mask"],
    common_valid_mask
)


# =========================
# STATISTICS
# =========================

stats = calculate_change_statistics(
    change_map
)

print("\n========== CHANGE RESULTS ==========")

print(
    f"Valid comparison pixels: "
    f"{stats['total_valid_pixels']}"
)

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


# =========================
# SAVE GEOTIFF
# =========================

output_path = (
    "data/change_map_2021_2026.tif"
)

save_change_map(
    change_map,
    result_2021["profile"],
    output_path
)

image_output_path = (
    "data/change_map_2021_2026_overlay.png"
)

create_change_image(
    change_map,
    image_output_path
)

print(
    f"Visualization saved to: "
    f"{image_output_path}"
)
print(
    f"\nChange map saved to: "
    f"{output_path}"
)