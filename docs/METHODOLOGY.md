# Methodology

## Overview

The objective of this work is to segment donut bodies and their inner holes from industrial conveyor belt images using classical computer vision techniques. The proposed pipeline consists of image preprocessing, binary segmentation, contour extraction, contour filtering, mask generation, and visualization. Each image is processed independently to produce separate masks for the donut body and the donut holes.

The overall workflow is illustrated below:

```
Input Image
      │
      ▼
Red-Blue Channel Subtraction
      │
      ▼
Intensity Normalization
      │
      ▼
Gaussian Blur
      │
      ▼
Image Padding
      │
      ▼
Otsu Thresholding
      │
      ▼
Morphological Opening
      │
      ▼
Morphological Closing
      │
      ▼
Contour Extraction
      │
      ▼
Contour Hierarchy Analysis
      │
      ▼
Area Filtering
      │
      ▼
Donut Mask + Hole Mask
      │
      ▼
Overlay Generation
```

---

# 1. Image Acquisition

The input images consist of RGB images captured from an industrial production line. The images contain multiple donuts placed on a moving conveyor belt under varying lighting conditions. These images also contain background objects, reflections, conveyor markings, and machine components that introduce additional challenges during segmentation.

---

# 2. Color Channel Enhancement

Instead of directly converting the image into grayscale, the RGB image is separated into its individual color channels.

The red channel is subtracted from the blue channel using

```python
diff = cv2.subtract(r, b)
```

This operation enhances the contrast between the donut dough and the conveyor belt because the donuts contain stronger red and yellow components than the surrounding background.

---

# 3. Intensity Normalization

After channel subtraction, image intensities are normalized to span the complete grayscale range.

```python
cv2.normalize(...)
```

Normalization improves image contrast and produces a more consistent intensity distribution before thresholding.

---

# 4. Noise Reduction

A Gaussian Blur is applied to smooth the image.

```python
cv2.GaussianBlur(...,(5,5),0)
```

The smoothing process suppresses small noisy pixels while preserving the overall shape of the donuts. This produces cleaner binary segmentation during thresholding.

---

# 5. Image Padding

Before thresholding, a padding border is added around the image.

```python
cv2.copyMakeBorder(...)
```

Padding prevents objects located near the image boundaries from being distorted during subsequent morphological operations.

After processing, the padding is removed to restore the original image dimensions.

---

# 6. Binary Image Generation

The enhanced grayscale image is converted into a binary image using Otsu's thresholding method.

```python
cv2.THRESH_BINARY + cv2.THRESH_OTSU
```

Unlike manually selecting a threshold value, Otsu's algorithm automatically determines the optimum threshold based on the intensity histogram of each image.

The output is a binary image where the foreground represents potential donut regions.

---

# 7. Morphological Processing

To improve segmentation quality, two morphological operations are performed.

### Morphological Opening

Opening removes isolated white pixels and small noise components.

```python
cv2.MORPH_OPEN
```

---

### Morphological Closing

Closing fills small gaps and reconnects broken donut boundaries.

```python
cv2.MORPH_CLOSE
```

Together, these operations produce smoother and more continuous object boundaries.

---

# 8. Contour Extraction

Contours are extracted from the processed binary image using

```python
cv2.findContours(...)
```

The contour retrieval mode `RETR_CCOMP` is selected because it preserves the parent-child relationship between contours.

This relationship is essential for distinguishing the outer donut body from the inner donut hole.

---

# 9. Contour Filtering

Each detected contour is analyzed according to its hierarchy and area.

### Parent Contours

Contours without a parent are treated as candidate donut bodies.

Very small contours are discarded to eliminate noise.

---

### Child Contours

Contours inside parent contours are treated as candidate donut holes.

Additional minimum and maximum area constraints are applied to reject reflections and small background artifacts.

This filtering stage significantly reduces false detections.

---

# 10. Mask Generation

After contour filtering, two binary masks are generated.

- Donut Body Mask
- Donut Hole Mask

Each contour is filled completely to produce solid binary masks representing the segmented objects.

---

# 11. Overlay Visualization

To simplify visual inspection, the generated masks are overlaid onto the original RGB image.

- Green represents the segmented donut body.
- Red represents the detected donut hole.

The overlay enables quick verification of segmentation accuracy by comparing the detected regions with the original image.

---

# 12. Output Generation

For every input image, the pipeline automatically saves three outputs:

- Binary donut mask
- Binary hole mask
- Overlay visualization

These outputs are stored separately for further analysis and performance evaluation.

---

# Summary

The proposed methodology follows a classical computer vision pipeline consisting of color channel enhancement, normalization, Gaussian smoothing, adaptive thresholding, morphological refinement, contour hierarchy analysis, contour filtering, binary mask generation, and overlay visualization. The combination of these stages enables reliable segmentation of donut bodies and their inner holes while reducing the effects of background noise and small image artifacts.
