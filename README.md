# 🍩 Donut Computer Vision Pipeline

A classical computer vision pipeline for segmenting **donut bodies** and **their inner holes** from industrial conveyor belt images using OpenCV and NumPy.

The pipeline is designed to work under challenging industrial conditions such as uneven lighting, conveyor reflections, flour residue, background machinery, and partially visible donuts, without using deep learning models.

---

## Project Overview

This project detects and segments:

- Donut bodies
- Donut holes

using a sequence of classical image processing techniques including:

- Color channel enhancement
- Intensity normalization
- Gaussian smoothing
- Otsu thresholding
- Morphological operations
- Contour hierarchy analysis
- Area-based contour filtering

---

## Tech Stack

- Python
- OpenCV
- NumPy

---

## Repository Structure

```text
.
├── README.md
├── requirements.txt
├── run.py
├── docs/
│   ├── SETUP.md
│   ├── METHODOLOGY.md
│   ��── POSTPROCESSING.md
│   └── RESULTS.md
├── input_samples/
└── output_samples/
```

### Directory Descriptions

- **docs/** – Complete documentation
  - **SETUP.md** – Installation and execution instructions
  - **METHODOLOGY.md** – Complete processing pipeline
  - **POSTPROCESSING.md** – Mask refinement and constraint handling
  - **RESULTS.md** – Experimental results, limitations, and discussion
- **src/** – Source code modules (pipeline implementation)
- **input_samples/** – Sample input images for testing
- **output_samples/** – Sample output results
- **run.py** – Main script to execute the pipeline
- **requirements.txt** – Python dependencies

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/MUnssRahim/Donut-ComputerVision-pipeline.git
cd Donut-ComputerVision-pipeline
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Download the Dataset

The industrial image dataset is available on Google Drive:

https://drive.google.com/drive/folders/1TmYb-5OsvrAGDtW-S9UiKJ9RRMq3jZLd?usp=sharing

### Configure the Input Directory

Open **`run.py`** and update:

```python
INPUT_DIR = r"path/to/your/image_folder"
```

### Run the Pipeline

```bash
python run.py
```

---

## Output

The pipeline automatically creates the following directory:

```text
Donutstest/
├── masks_donut/
├── masks_hole/
└── overlays/
```

- **masks_donut/** – Binary masks of the segmented donut bodies.
- **masks_hole/** – Binary masks of the detected donut holes.
- **overlays/** – Original images with segmentation overlays (Green: donut body, Red: donut hole).

---

## Documentation

For detailed information, see the documentation files in the `docs/` directory:

- **[SETUP.md](docs/SETUP.md)** – Installation and execution instructions
- **[METHODOLOGY.md](docs/METHODOLOGY.md)** – Complete processing pipeline
- **[POSTPROCESSING.md](docs/POSTPROCESSING.md)** – Mask refinement and constraint handling
- **[RESULTS.md](docs/RESULTS.md)** – Experimental results, limitations, and discussion

---

## Notes

- Built entirely using classical computer vision.
- No deep learning models are used.
- Output folders are created automatically during execution.
- Invalid images are skipped without stopping the pipeline.
- One donut mask, one hole mask, and one overlay image are generated for every input image.
