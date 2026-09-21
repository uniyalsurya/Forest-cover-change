import numpy as np
import rasterio
from rasterio.enums import Resampling


# Sentinel-2 SCL classes that we DON'T want
INVALID_SCL_CLASSES = {
    0,   # No data
    1,   # Saturated / defective
    3,   # Cloud shadow
    8,   # Cloud medium probability
    9,   # Cloud high probability
    10,  # Cirrus
    11,  # Snow / ice
}


def create_scl_mask(scl_path: str, reference_path: str):
    """
    Read Sentinel-2 SCL and resample it to the resolution/grid
    of the reference image (B04/B08).

    Returns:
        valid_mask:
            True  = usable pixel
            False = cloud/shadow/bad pixel
    """

    # Open B04 (10m) as the reference grid
    with rasterio.open(reference_path) as ref:
        reference_shape = (ref.height, ref.width)
        reference_transform = ref.transform

    # Open SCL (20m) and resample to B04's 10m grid
    with rasterio.open(scl_path) as src:
        scl = src.read(
            1,
            out_shape=reference_shape,
            resampling=Resampling.nearest
        )

    # True = usable pixel
    valid_mask = ~np.isin(scl, list(INVALID_SCL_CLASSES))

    return valid_mask