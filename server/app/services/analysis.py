import numpy as np

from app.services.aoi import crop_to_aoi
from app.services.masking import create_scl_mask


def process_year(
    red_path: str,
    nir_path: str,
    scl_path: str,
    threshold: float = 0.3
):
    red, profile = crop_to_aoi(red_path)
    nir, _ = crop_to_aoi(nir_path)

    if red.shape != nir.shape:
        raise ValueError(
            f"Band dimensions do not match: "
            f"Red={red.shape}, NIR={nir.shape}"
        )

    red = red.astype(np.float32)
    nir = nir.astype(np.float32)

    denominator = nir + red

    ndvi = np.divide(
        nir - red,
        denominator,
        out=np.zeros_like(nir, dtype=np.float32),
        where=denominator != 0
    )

    # Remove invalid pixels using Sentinel-2 SCL
    scl_mask = create_scl_mask(
        scl_path,
        red_path
    )

    if ndvi.shape != scl_mask.shape:
        raise ValueError(
            f"NDVI and SCL mask dimensions do not match: "
            f"NDVI={ndvi.shape}, SCL={scl_mask.shape}"
        )

    # Valid pixels for this year
    valid_mask = (
        np.isfinite(ndvi) &
        scl_mask
    )

    # Ignore invalid pixels
    ndvi[~valid_mask] = np.nan

    # Vegetation candidate
    vegetation_mask = (
        valid_mask &
        (ndvi >= threshold)
    ).astype(np.uint8)

    valid_pixels = int(valid_mask.sum())

    vegetation_pixels = int(
        vegetation_mask.sum()
    )

    vegetation_percentage = (
        vegetation_pixels / valid_pixels * 100
        if valid_pixels > 0
        else 0
    )

    return {
        "ndvi": ndvi,
        "vegetation_mask": vegetation_mask,
        "valid_mask": valid_mask,
        "profile": profile,
        "valid_pixels": valid_pixels,
        "vegetation_pixels": vegetation_pixels,
        "vegetation_percentage": vegetation_percentage,
    }