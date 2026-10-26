
from pathlib import Path
import argparse

import numpy as np
import pydicom


def load_dicom(file_path):
    """Read a DICOM file and return its dataset."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    dataset = pydicom.dcmread(path)

    if not hasattr(dataset, "PixelData"):
        raise ValueError("This DICOM file has no PixelData.")

    return dataset


def get_image_array(dataset):
    """Convert DICOM pixel data into a NumPy array."""
    image = np.asarray(dataset.pixel_array)

    if image.ndim != 2:
        raise ValueError(
            "Version 1 supports 2D grayscale images only."
        )

    return image


def get_metadata(dataset):
    """Return basic technical metadata."""
    return {
        "Modality": getattr(dataset, "Modality", "Unknown"),
        "Rows": getattr(dataset, "Rows", "Unknown"),
        "Columns": getattr(dataset, "Columns", "Unknown"),
    }



def display_image(image, title="DICOM Image", output_path="dicom_preview.png"):
    """Save a grayscale image as a PNG file."""
    import matplotlib
    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    plt.figure(figsize=(7, 7))
    plt.imshow(image, cmap="gray")
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()

    print(f"Image saved to: {output_path}")


def convert_to_hounsfield(dataset):
    """Convert stored CT pixel values to Hounsfield units."""
    image = get_image_array(dataset).astype(np.float32)

    slope = float(getattr(dataset, "RescaleSlope", 1))
    intercept = float(getattr(dataset, "RescaleIntercept", 0))

    return image * slope + intercept


def apply_window(image_hu, center, width):
    """Map CT Hounsfield units into a display range of 0–255."""
    if width <= 0:
        raise ValueError("Window width must be positive.")

    lower = center - width / 2
    upper = center + width / 2

    windowed = np.clip(image_hu, lower, upper)
    windowed = (windowed - lower) / (upper - lower)

    return (windowed * 255).astype(np.uint8)


def main():
    parser = argparse.ArgumentParser(
        description="Explore a DICOM medical image."
    )
    parser.add_argument(
        "file",
        help="Path to a DICOM (.dcm) file"
    )
    args = parser.parse_args()

    try:
        dataset = load_dicom(args.file)
        image = get_image_array(dataset)
    except (FileNotFoundError, ValueError, OSError) as error:
        parser.error(str(error))
    except Exception as error:
        parser.error(
            f"Could not read or decode the image: {error}"
        )

    print("DICOM Image Summary")
    print("-------------------")

    for key, value in get_metadata(dataset).items():
        print(f"{key}: {value}")

    print(f"Array shape: {image.shape}")
    print(f"Pixel data type: {image.dtype}")
    print(f"Minimum pixel value: {image.min()}")
    print(f"Maximum pixel value: {image.max()}")
    print(f"Mean pixel value: {image.mean():.2f}")
    print(f"Standard deviation: {image.std():.2f}")
    
    if getattr(dataset, "Modality", "") == "CT":
        image_hu = convert_to_hounsfield(dataset)

        lung_window = apply_window(
            image_hu,
            center=-600,
            width=1500,
        )

        display_image(
            lung_window,
            title="CT Lung Window",
            output_path="dicom_ct_windowed.png",
        )

    display_image(
        image,
        title="Original DICOM Image",
        output_path="dicom_original.png",
    )



if __name__ == "__main__":
    main()
