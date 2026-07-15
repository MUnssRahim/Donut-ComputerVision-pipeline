# Post-Processing: Mask Refinement and Constraint Handling

## Overview

The initial thresholding stage successfully separates most donut regions from the conveyor belt. However, the raw binary masks still contain several imperfections, including background noise, fragmented donut boundaries, reflections, and unwanted machine components. These artifacts reduce segmentation quality and introduce false detections.

To improve the final masks, a series of post-processing operations and filtering constraints were applied. Multiple parameter values and alternative approaches were evaluated during development before selecting the final implementation.

---

# Constraint 1: Removal of Small Noise

## Problem

The thresholded image contains numerous small white regions caused by flour residue, conveyor belt texture, sensor noise, and small reflections. These isolated regions increase the number of false contours and reduce segmentation accuracy.

## Applied Solution

A **Morphological Opening** operation (erosion followed by dilation) using a **3 × 3 elliptical kernel** was applied to remove isolated foreground pixels while preserving larger donut regions.

## Result

Most small noisy regions were successfully removed without significantly altering the donut shapes. This reduced false contour detections and produced cleaner binary masks for the next processing stage.

## Alternative Evaluated

Larger kernels and multiple opening iterations were tested during development. Although they removed additional background noise, they also eroded valid donut boundaries, particularly partially visible donuts near the image edges. Therefore, a single opening operation using a **3 × 3 kernel** was selected.

---

# Constraint 2: Reconnecting Fragmented Donut Boundaries

## Problem

Uneven illumination and intensity variations occasionally fragmented the segmented donut bodies, causing a single donut to appear as multiple disconnected regions.

## Applied Solution

A **Morphological Closing** operation (dilation followed by erosion) using a **9 × 9 elliptical kernel** was applied after opening.

## Result

Closing successfully repaired most fragmented donut boundaries, producing smoother and more continuous masks. This improved contour extraction and reduced incomplete donut detections.

## Alternative Evaluated

Smaller kernels were unable to reconnect fragmented regions effectively, while larger kernels often merged nearby foreground objects and distorted donut boundaries. The selected kernel provided the best compromise between connectivity and shape preservation.

---

# Constraint 3: Image Boundary Protection

## Problem

Several donuts are only partially visible near the image borders. During morphological processing, kernels extend beyond the image boundary, causing distortion near the edges.

## Applied Solution

A constant **20-pixel black border** was added around each image before thresholding and morphological operations. The padding was removed once processing was complete.

## Result

Padding preserved the structure of donuts near the image boundaries and reduced edge-related distortions during morphological processing.

## Alternative Evaluated

Processing images without padding resulted in incomplete contours and distorted edge objects. Padding consistently produced cleaner masks for partially visible donuts.

---

# Constraint 4: Removal of Invalid Contours

## Problem

Even after morphological refinement, numerous unwanted contours remained due to conveyor reflections, flour particles, background texture, and machine components.

## Applied Solution

Area-based filtering was applied to every detected contour.

- Small parent contours were discarded.
- Extremely small child contours were removed.
- Extremely large child contours were rejected.

Only contours satisfying the predefined area constraints were retained.

## Result

Area filtering significantly reduced false detections while preserving the majority of valid donut bodies and holes.

## Alternative Evaluated

Lower area thresholds retained excessive background noise, whereas larger thresholds removed partially visible donuts and valid hole regions. The selected threshold values produced the most balanced segmentation across the test images.

---

# Constraint 5: Separation of Donut Bodies and Holes

## Problem

After thresholding, both the donut body and the inner hole appear as separate contours. Without additional processing, these contours cannot be distinguished automatically.

## Applied Solution

Contour hierarchy information obtained using **RETR_CCOMP** was used to classify contours.

- Parent contours represent donut bodies.
- Child contours represent donut holes.

Only child contours associated with valid parent contours were accepted.

## Result

Hierarchy filtering successfully separated donut bodies from their inner holes while reducing false hole detections originating from isolated background regions.

## Alternative Evaluated

Shape-based filtering and the **Hough Circle Transform** were evaluated during development. However, partially visible donuts, irregular object boundaries, conveyor reflections, and deformed dough reduced their reliability. Contour hierarchy proved to be more robust and consistent for the available industrial dataset.

---

# Constraint 6: Binary Mask Generation

## Problem

Contour boundaries alone are insufficient for visualization and evaluation.

## Applied Solution

Accepted contours were filled completely to generate two separate binary masks:

- Donut Body Mask
- Donut Hole Mask

## Result

Separate masks simplified visualization and allowed the donut bodies and holes to be evaluated independently.

---

# Constraint 7: Visual Verification

## Problem

Binary masks alone make it difficult to verify whether the segmented regions accurately correspond to the original donuts.

## Applied Solution

The generated masks were overlaid on the original RGB images.

- **Green** represents the detected donut body.
- **Red** represents the detected donut hole.

## Result

The overlay images enabled rapid visual inspection of segmentation quality and made remaining false positives and missed detections easier to identify during testing.

---

# Overall Post-Processing Results

The post-processing stage significantly improved the quality of the final segmentation masks. Small noisy regions were removed, fragmented donut boundaries were reconnected, invalid contours were discarded, and donut bodies were successfully separated from their corresponding holes.

Despite these improvements, some challenging cases remained. Severe paint degradation on the left machine base occasionally produced large false positives due to its similar appearance to the donut dough. Uneven illumination in darker image corners sometimes reduced segmentation quality, while reflections from metallic conveyor components occasionally generated small false hole detections.

Overall, the selected post-processing pipeline provided the best balance between segmentation accuracy, robustness, and computational efficiency while remaining entirely based on classical computer vision techniques.

---

# Post-Processing Outputs

The refined segmentation results produced after post-processing are available on Google Drive for inspection and evaluation.

**Results Folder**

https://drive.google.com/drive/folders/1ITMzEp5ASysKT3esZ3thFWdcd7SYFQzO?usp=drive_link

The results folder contains three separate directories:

- **masks_donut/** – Binary masks containing the refined segmented donut bodies.
- **masks_hole/** – Binary masks containing the refined segmented donut holes.
- **overlays/** – Final segmentation images with the generated masks overlaid on the original industrial images (Green: donut body, Red: donut hole).

These outputs demonstrate the effectiveness of the post-processing stage by providing both the refined binary masks and the final visualization of the segmentation results.
