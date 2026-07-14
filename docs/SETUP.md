# Setup and Execution Guide

## Requirements

- Python 3.9 or later
- OpenCV
- NumPy

Install the required dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt`

```text
opencv-python
numpy
```

---

# Download the Dataset

Download the industrial donut image dataset from:

https://drive.google.com/drive/folders/1TmYb-5OsvrAGDtW-S9UiKJ9RRMq3jZLd?usp=sharing

Extract the downloaded folder to any location on your computer.

---

# Configure the Input Directory

Open **`run.py`** and update the following line:

```python
INPUT_DIR = r"path/to/your/image_folder"
```

Replace it with the location of your downloaded dataset.

---

# Run the Project

Execute the script:

```bash
python run.py
```

or run `run.py` directly from your preferred IDE.

---

# Output

The program automatically creates an output folder named:

```text
Donutstest/
```

Inside it, three folders are generated:

```text
Donutstest/
├── masks_donut/
├── masks_hole/
└── overlays/
```

### `masks_donut/`

Contains binary masks of the segmented donut bodies.

### `masks_hole/`

Contains binary masks of the detected donut holes.

### `overlays/`

Contains the original images with segmentation results overlaid.

- 🟢 Green — Donut body
- 🔴 Red — Donut hole

---

# Notes

- No manual creation of output folders is required.
- All supported images inside the input folder are processed automatically.
- Invalid or unreadable images are skipped without stopping the program.
- Each input image generates:
  - Donut body mask
  - Donut hole mask
  - Segmentation overlay
