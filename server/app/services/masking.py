import numpy as np
import rasterio
from rasterio.mask import mask
from rasterio.warp import transform_geom
from rasterio.enums import Resampling
from shapely.geometry import box, mapping


# Copernicus Browser AOI
WEST = 72.901068
SOUTH = 19.202079
EAST = 72.911453
NORTH = 19.214318


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
    Create an SCL mask for the same AOI and grid
    as the cropped B04 image.

    True  = usable pixel
    False = cloud/shadow/bad pixel
    """

    # AOI is defined in latitude/longitude
    aoi = box(
        WEST,
        SOUTH,
        EAST,
        NORTH
    )

    with rasterio.open(reference_path) as ref:

        # Convert AOI from WGS84 to the B04 CRS
        aoi_ref = transform_geom(
            "EPSG:4326",
            ref.crs,
            mapping(aoi)
        )

        # Crop B04 to determine the exact target shape
        _, ref_transform = mask(
            ref,
            [aoi_ref],
            crop=True
        )

        ref_height, ref_width = mask(
            ref,
            [aoi_ref],
            crop=True
        )[0].shape[1:]

    with rasterio.open(scl_path) as src:

        # Convert AOI to SCL's CRS
        aoi_scl = transform_geom(
            "EPSG:4326",
            src.crs,
            mapping(aoi)
        )

        # Crop SCL to AOI
        scl_cropped, scl_transform = mask(
            src,
            [aoi_scl],
            crop=True
        )

        scl_cropped = scl_cropped[0]

        # Create 10m output grid
        scl_resampled = np.empty(
            (ref_height, ref_width),
            dtype=np.uint8
        )

        # Resample SCL 20m → 10m
        with rasterio.MemoryFile() as memfile:

            profile = src.profile.copy()

            profile.update({
                "height": scl_cropped.shape[0],
                "width": scl_cropped.shape[1],
                "transform": scl_transform
            })

            with memfile.open(**profile) as temp:

                temp.write(scl_cropped, 1)

                temp.read(
                    1,
                    out=scl_resampled,
                    resampling=Resampling.nearest
                )

    # Mark unwanted SCL classes as invalid
    valid_mask = ~np.isin(
        scl_resampled,
        list(INVALID_SCL_CLASSES)
    )

    return valid_mask