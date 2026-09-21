import numpy as np


OTHER = 0
LOSS = 1
STABLE = 2
GAIN = 3
INVALID = 255


def detect_change(
    forest_2021: np.ndarray,
    forest_2026: np.ndarray,
    valid_mask: np.ndarray
):
    if forest_2021.shape != forest_2026.shape:
        raise ValueError(
            f"Mask dimensions do not match: "
            f"2021={forest_2021.shape}, "
            f"2026={forest_2026.shape}"
        )

    if forest_2021.shape != valid_mask.shape:
        raise ValueError(
            f"Valid mask dimensions do not match: "
            f"forest={forest_2021.shape}, "
            f"valid={valid_mask.shape}"
        )

    # Start everything as INVALID
    change_map = np.full(
        forest_2021.shape,
        INVALID,
        dtype=np.uint8
    )

    loss = (
        (forest_2021 == 1) &
        (forest_2026 == 0)
    )

    stable = (
        (forest_2021 == 1) &
        (forest_2026 == 1)
    )

    gain = (
        (forest_2021 == 0) &
        (forest_2026 == 1)
    )

    change_map[valid_mask & loss] = LOSS
    change_map[valid_mask & stable] = STABLE
    change_map[valid_mask & gain] = GAIN

    return change_map


def calculate_change_statistics(
    change_map: np.ndarray
):
    valid = change_map != INVALID

    total_pixels = int(valid.sum())

    loss_pixels = int(
        np.sum(change_map == LOSS)
    )

    stable_pixels = int(
        np.sum(change_map == STABLE)
    )

    gain_pixels = int(
        np.sum(change_map == GAIN)
    )

    if total_pixels == 0:
        return {
            "total_valid_pixels": 0,
            "loss_pixels": 0,
            "stable_pixels": 0,
            "gain_pixels": 0,
            "loss_percentage": 0,
            "stable_percentage": 0,
            "gain_percentage": 0,
        }

    return {
        "total_valid_pixels": total_pixels,
        "loss_pixels": loss_pixels,
        "stable_pixels": stable_pixels,
        "gain_pixels": gain_pixels,

        "loss_percentage":
            loss_pixels / total_pixels * 100,

        "stable_percentage":
            stable_pixels / total_pixels * 100,

        "gain_percentage":
            gain_pixels / total_pixels * 100,
    }