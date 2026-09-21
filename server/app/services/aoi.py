import rasterio
from rasterio.mask import mask
from rasterio.warp import transform_geom
from shapely.geometry import box, mapping


WEST = 72.901068
SOUTH = 19.202079
EAST = 72.911453
NORTH = 19.214318


def crop_to_aoi(image_path: str):

    aoi = box(
        WEST,
        SOUTH,
        EAST,
        NORTH
    )

    with rasterio.open(image_path) as src:

        # Convert AOI from WGS84 (EPSG:4326)
        # to the satellite image CRS
        aoi_projected = transform_geom(
            "EPSG:4326",
            src.crs,
            mapping(aoi)
        )

        cropped, transform = mask(
            src,
            [aoi_projected],
            crop=True
        )

        profile = src.profile.copy()

        profile.update({
            "height": cropped.shape[1],
            "width": cropped.shape[2],
            "transform": transform
        })

    return cropped[0], profile