DICOM Image Explorer

A beginner-friendly Python project for reading, inspecting, and visualizing DICOM medical images. Developed as part of my learning journey in computer vision, medical imaging, and AI.

Features

Read DICOM files using pydicom.
Extract pixel data into NumPy arrays.
Display 2D grayscale images.
Inspect basic technical metadata.
Handle missing files and unsupported image dimensions.
Run automated unit tests using pytest.
Technologies
Python
pydicom
NumPy
Matplotlib
pytest
Project Structure
    dicom-image-explorer/
    ├── dicom_explorer.py
    ├── requirements.txt
    ├── README.md
    ├── .gitignore
    └── tests/
        └── test_dicom_explorer.py

Installation

Clone the repository, enter the project directory, and create a virtual environment.


python -m venv .venv


Activate the environment and install dependencies:


python -m pip install -r requirements.txt

Usage

Run the viewer with a local DICOM file:


python dicom_explorer.py path/to/image.dcm


The program prints basic metadata and displays the image in a separate window.

Testing

python -m pytest -v

Current Limitations
Supports 2D grayscale images only.
Does not yet implement CT windowing or modality-specific pixel transformations.
Does not perform cancer detection or clinical diagnosis.
Has not yet been validated against a clinical imaging workflow.
Planned Improvements
Add CT windowing and intensity transformations.
Support image stacks and selected multi-frame DICOM files.
Add image normalization and preprocessing tools.
Evaluate image-processing methods on appropriate public research datasets.
Explore machine learning and explainable computer vision.
Responsible Use

This project is for educational and research purposes only. It is not a medical device and must not be used to make clinical decisions.

Do not upload patient-identifiable DICOM data to this repository. Follow dataset licenses, access conditions, and applicable privacy requirements.

Author

MSc student in Artificial Intelligence and Robotics, exploring computer vision and medical image analysis.ARIAN_yk