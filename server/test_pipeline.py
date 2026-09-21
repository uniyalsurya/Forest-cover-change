import numpy as np

from app.services.ndvi import (
    calculate_ndvi,
    create_forest_mask
)


red_path = "data/2021/B04-21.jp2"
nir_path = "data/2021/B08-21.jp2"
scl_path = "data/2021/SCL.jp2"


ndvi = calculate_ndvi(
    red_path,
    nir_path,
    scl_path
)

forest_mask = create_forest_mask(
    ndvi,
    threshold=0.3
)


valid_pixels = np.isfinite(ndvi).sum()
forest_pixels = forest_mask.sum()

print("NDVI shape:", ndvi.shape)
print("Valid pixels:", valid_pixels)
print("Forest candidate pixels:", forest_pixels)

forest_percentage = (
    forest_pixels / valid_pixels
) * 100

print(
    "Forest candidate percentage:",
    forest_percentage
)