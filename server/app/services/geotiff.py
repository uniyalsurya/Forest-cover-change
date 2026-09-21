import rasterio


def save_change_map(
    change_map,
    reference_profile,
    output_path
):
    """
    Save the change classification map as a GeoTIFF.

    Classes:
        0 = Other
        1 = Vegetation loss
        2 = Stable vegetation
        3 = Vegetation gain
    """

    profile = reference_profile.copy()

    profile.update({
        "driver": "GTiff",
        "dtype": "uint8",
        "count": 1,
        "compress": "lzw"
    })

    with rasterio.open(output_path, "w", **profile) as dst:
        dst.write(change_map, 1)

    return output_path