import numpy as np
from PIL import Image


OTHER = 0
LOSS = 1
STABLE = 2
GAIN = 3
INVALID = 255


def create_change_image(change_map, output_path):
    """
    Create a transparent RGBA visualization.

    Loss   = Red
    Stable = Yellow
    Gain   = Green
    Other/Invalid = Transparent
    """

    height, width = change_map.shape

    # RGBA image
    image = np.zeros(
        (height, width, 4),
        dtype=np.uint8
    )

    # Vegetation loss -> RED
    image[change_map == LOSS] = [
        255, 0, 0, 180
    ]

    # Stable vegetation -> YELLOW
    image[change_map == STABLE] = [
        255, 255, 0, 140
    ]

    # Vegetation gain -> GREEN
    image[change_map == GAIN] = [
        0, 255, 0, 180
    ]

    # Other and invalid remain:
    # [0, 0, 0, 0] = transparent

    Image.fromarray(
        image,
        mode="RGBA"
    ).save(output_path)

    return output_path