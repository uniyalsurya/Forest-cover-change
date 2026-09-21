import numpy as np

from app.services.aoi import crop_to_aoi
from app.services.masking import create_scl_mask


def process_year(
    red_path: str,
    nir_path: str,
    scl_path: str,
    threshold: float = 0.3
):
    """
    Process one Sentinel-2 acquisition.

    Steps:
    1. Crop B04 and B08 to the AOI
    2. Calculate NDVI
    3. Create SCL cloud/shadow mask
    4. Remove invalid pixels
    5. Create vegetation candidate mask
    """

    # -----------------------------------------
    # 1. Crop Red and NIR to AOI
    # -----------------------------------------

    red, profile = crop_to_aoi(red_path)
    nir, _ = crop_to_aoi(nir_path)

    if red.shape != nir.shape:
        raise ValueError(
            f"Band dimensions do not match: "
            f"Red={red.shape}, NIR={nir.shape}"
        )

    # -----------------------------------------
    # 2. Calculate NDVI
    # -----------------------------------------

    red = red.astype(np.float32)
    nir = nir.astype(np.float32)

    denominator = nir + red

    ndvi = np.divide(
        nir - red,
        denominator,
        out=np.zeros_like(nir, dtype=np.float32),
        where=denominator != 0
    )

    # -----------------------------------------
    # 3. Create SCL mask
    # -----------------------------------------

    scl_mask = create_scl_mask(
        scl_path,
        red_path
    )

    # -----------------------------------------
    # 4. Make sure dimensions match
    # -----------------------------------------

    if ndvi.shape != scl_mask.shape:
        raise ValueError(
            f"NDVI and SCL dimensions do not match: "
            f"NDVI={ndvi.shape}, SCL={scl_mask.shape}"
        )

    # -----------------------------------------
    # 5. Remove invalid pixels
    # -----------------------------------------

    ndvi[~scl_mask] = np.nan

    # -----------------------------------------
    # 6. Create vegetation candidate mask
    # -----------------------------------------

    vegetation_mask = (
        np.isfinite(ndvi) &
        (ndvi >= threshold)
    ).astype(np.uint8)

    # -----------------------------------------
    # 7. Calculate statistics
    # -----------------------------------------

    valid_pixels = int(np.isfinite(ndvi).sum())
    vegetation_pixels = int(vegetation_mask.sum())

    vegetation_percentage = (
        vegetation_pixels / valid_pixels * 100
        if valid_pixels > 0
        else 0
    )

    return {
        "ndvi": ndvi,
        "vegetation_mask": vegetation_mask,
        "profile": profile,
        "valid_pixels": valid_pixels,
        "vegetation_pixels": vegetation_pixels,
        "vegetation_percentage": vegetation_percentage,
    }