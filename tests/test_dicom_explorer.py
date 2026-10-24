
import numpy as np
import pytest

from dicom_explorer import convert_to_hounsfield, apply_window


class FakeDataset:
    """A small stand-in for a DICOM dataset."""

    def __init__(self, pixels, slope=1, intercept=0):
        self.pixel_array = np.array(pixels)
        self.RescaleSlope = slope
        self.RescaleIntercept = intercept


def test_convert_to_hounsfield():
    dataset = FakeDataset(
        [[0, 100], [200, 300]],
        slope=2,
        intercept=-1000,
    )

    result = convert_to_hounsfield(dataset)

    expected = np.array(
        [[-1000, -800], [-600, -400]],
        dtype=np.float32,
    )

    np.testing.assert_allclose(result, expected)


def test_apply_window():
    image = np.array([-100, 0, 100])

    result = apply_window(image, center=0, width=200)

    expected = np.array([0, 127, 255], dtype=np.uint8)

    np.testing.assert_array_equal(result, expected)


def test_apply_window_rejects_zero_width():
    with pytest.raises(ValueError, match="positive"):
        apply_window(np.array([0]), center=0, width=0)
