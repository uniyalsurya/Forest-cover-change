import numpy as np

from app.services.aoi import crop_to_aoi
from app.services.masking import create_scl_mask


red_path = "data/2026/B04-26.jp2"
nir_path = "data/2026/B08-26.jp2"
scl_path = "data/2026/SCL-26.jp2"


# --------------------------------------------------
# 1. Crop B04 and B08 to our AOI
# --------------------------------------------------

red, red_profile = crop_to_aoi(red_path)
nir, nir_profile = crop_to_aoi(nir_path)

print("Red AOI shape:", red.shape)
print("NIR AOI shape:", nir.shape)


# --------------------------------------------------
# 2. Calculate NDVI
# --------------------------------------------------

red = red.astype(np.float32)
nir = nir.astype(np.float32)

denominator = nir + red

ndvi = np.divide(
    nir - red,
    denominator,
    out=np.zeros_like(nir, dtype=np.float32),
    where=denominator != 0
)

print("NDVI range:", np.nanmin(ndvi), np.nanmax(ndvi))
print("Mean NDVI:", np.nanmean(ndvi))


# --------------------------------------------------
# 3. Create SCL mask for the AOI
# --------------------------------------------------

scl_mask = create_scl_mask(
    scl_path,
    red_path
)

print("SCL mask shape:", scl_mask.shape)


# --------------------------------------------------
# 4. Make sure everything matches
# --------------------------------------------------

if ndvi.shape != scl_mask.shape:
    raise ValueError(
        f"Shape mismatch: "
        f"NDVI={ndvi.shape}, "
        f"SCL={scl_mask.shape}"
    )


# --------------------------------------------------
# 5. Remove invalid pixels
# --------------------------------------------------

ndvi[~scl_mask] = np.nan


# --------------------------------------------------
# 6. Calculate vegetation candidate percentage
# --------------------------------------------------

forest_mask = (
    np.isfinite(ndvi) &
    (ndvi >= 0.3)
)

valid_pixels = np.isfinite(ndvi).sum()
vegetation_pixels = forest_mask.sum()

vegetation_percentage = (
    vegetation_pixels / valid_pixels
) * 100


print("Valid pixels:", valid_pixels)
print("Vegetation candidate pixels:", vegetation_pixels)
print(
    "Vegetation candidate percentage:",
    vegetation_percentage
)