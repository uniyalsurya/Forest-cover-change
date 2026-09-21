import numpy as np
import rasterio

from app.services.masking import create_scl_mask


def calculate_ndvi(
    red_path: str,
    nir_path: str,
    scl_path: str | None = None
):
    """
    Calculate NDVI from Sentinel-2 Red (B04) and
    Near Infrared (B08) bands.

    If SCL is provided, invalid pixels such as clouds
    and cloud shadows are masked.
    """

    with rasterio.open(red_path) as red_src:
        red = red_src.read(1).astype(np.float32)

    with rasterio.open(nir_path) as nir_src:
        nir = nir_src.read(1).astype(np.float32)

    if red.shape != nir.shape:
        raise ValueError(
            f"Band dimensions do not match: "
            f"Red={red.shape}, NIR={nir.shape}"
        )

    denominator = nir + red

    ndvi = np.divide(
        nir - red,
        denominator,
        out=np.zeros_like(nir, dtype=np.float32),
        where=denominator != 0
    )

    # Apply SCL cloud/shadow mask
    if scl_path:
        valid_mask = create_scl_mask(
            scl_path,
            red_path
        )

        ndvi[~valid_mask] = np.nan

    return ndvi


def create_forest_mask(
    ndvi: np.ndarray,
    threshold: float = 0.3
):
    """
    Create a vegetation candidate mask.

    1 = vegetation candidate
    0 = non-vegetation
    """

    return (
        np.isfinite(ndvi) &
        (ndvi >= threshold)
    ).astype(np.uint8)