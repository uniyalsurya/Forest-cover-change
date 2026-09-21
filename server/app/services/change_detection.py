import numpy as np


# Change classes
OTHER = 0
LOSS = 1
STABLE = 2
GAIN = 3


def detect_change(
    forest_2021: np.ndarray,
    forest_2026: np.ndarray
):
    """
    Compare two vegetation masks pixel-by-pixel.

    Classes:
        0 = Other / non-vegetation
        1 = Vegetation loss
        2 = Stable vegetation
        3 = Vegetation gain
    """

    if forest_2021.shape != forest_2026.shape:
        raise ValueError(
            f"Mask dimensions do not match: "
            f"2021={forest_2021.shape}, "
            f"2026={forest_2026.shape}"
        )

    change_map = np.zeros(
        forest_2021.shape,
        dtype=np.uint8
    )

    # Vegetation in 2021 AND NOT vegetation in 2026
    loss = (
        (forest_2021 == 1) &
        (forest_2026 == 0)
    )

    # Vegetation in both years
    stable = (
        (forest_2021 == 1) &
        (forest_2026 == 1)
    )

    # NOT vegetation in 2021 AND vegetation in 2026
    gain = (
        (forest_2021 == 0) &
        (forest_2026 == 1)
    )

    change_map[loss] = LOSS
    change_map[stable] = STABLE
    change_map[gain] = GAIN

    return change_map


def calculate_change_statistics(change_map: np.ndarray):
    """
    Calculate pixel counts and percentages
    for each change class.
    """

    total_pixels = change_map.size

    loss_pixels = np.sum(change_map == LOSS)
    stable_pixels = np.sum(change_map == STABLE)
    gain_pixels = np.sum(change_map == GAIN)

    return {
        "loss_pixels": int(loss_pixels),
        "stable_pixels": int(stable_pixels),
        "gain_pixels": int(gain_pixels),

        "loss_percentage": (
            loss_pixels / total_pixels * 100
        ),

        "stable_percentage": (
            stable_pixels / total_pixels * 100
        ),

        "gain_percentage": (
            gain_pixels / total_pixels * 100
        ),
    }