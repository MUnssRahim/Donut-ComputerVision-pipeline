# Post-Processing: Mask Refinement and Constraint Handling

## Overview

Although the preprocessing stage successfully generates a binary image containing the donut regions, the thresholded output still contains unwanted artifacts such as background noise, fragmented donut boundaries, reflections, and machine components. Therefore, a dedicated post-processing stage was implemented to refine the segmentation masks before generating the final output.

Several constraints were introduced to improve the quality of the extracted masks while preserving valid donut structures. Different parameter values and alternative approaches were also evaluated during development before selecting the final pipeline.

---

# Constraint 1: Removal of Small Noise

## Problem

The thresholded image contains numerous small white regions originating from flour residue, conveyor texture, sensor noise, and small reflections. These regions can easily be detected as contours, increasing the number of false positives.

## Applied Solution

A **Morphological Opening** operation (erosion followed by dilation) was applied using a **3 × 3 elliptical kernel**.

Opening removes isolated foreground pixels while preserving the larger donut regions.

## Why This Method?

Larger opening kernels and multiple opening iterations were tested during experimentation. Although they successfully removed additional background noise, they also removed valid pixels from partially visible donuts and reduced segmentation quality. Therefore, a single opening operation using a 3 × 3 kernel was selected.

---

# Constraint 2: Reconnecting Broken Donut Boundaries

## Problem

Uneven illumination and intensity variations occasionally create small gaps in the segmented donut boundaries. These gaps may divide a single donut into multiple disconnected regions.

## Applied Solution

A **Morphological Closing** operation (dilation followed by erosion) was performed using a **9 × 9 elliptical kernel**.

This reconnects fragmented regions and produces smoother object boundaries.

## Why This Method?

Smaller kernels were unable to reconnect many of the fragmented boundaries.

Larger kernels were also evaluated. Although they filled additional gaps, they began merging nearby foreground regions and slightly distorted donut shapes. The selected kernel provided the best compromise between connectivity and shape preservation.

---

# Constraint 3: Image Boundary Protection

## Problem

Several donuts are partially visible near the image borders. During morphological processing, convolution kernels extend outside the image, causing distortion near the boundaries.

## Applied Solution

A constant **20-pixel black border** was added around every image before thresholding and morphological operations. The padding was removed after processing was completed.

## Why This Method?

Without padding, boundary objects became distorted after morphological operations, producing incomplete contours. Padding preserved object structure while allowing the kernels to operate normally.

---

# Constraint 4: Removal of Invalid Contours

## Problem

Even after morphological processing, several unwanted contours remain due to conveyor reflections, flour particles, machine components, and background texture.

## Applied Solution

Each contour was filtered according to its area.

- Small parent contours were discarded.
- Extremely small child contours were removed.
- Extremely large child contours were also rejected.

Only contours satisfying the predefined area constraints were retained.

## Why Area Filtering Instead of Circle Detection?

Initially, the Hough Circle Transform (`cv2.HoughCircles`) was considered because donuts are approximately circular.

However, this approach was not adopted for several reasons:

- Several donuts are partially visible near the image boundaries.
- The donuts are not perfect circles due to slight shape variations.
- Conveyor reflections generate false circular edges.
- Machine components also contain curved structures that increase false detections.

Contour-based filtering proved significantly more robust because it detects complete as well as partially visible donuts without assuming a perfect circular shape.

Different contour area thresholds were tested throughout development. Lower thresholds produced numerous false positives, whereas larger thresholds removed valid donuts near the image boundaries. The final thresholds were therefore selected as the best balance between sensitivity and robustness.

---

# Constraint 5: Separation of Donut Bodies and Holes

## Problem

After thresholding, both the donut body and the center hole appear as separate contours. Without additional processing, these contours cannot be distinguished automatically.

## Applied Solution

Contour hierarchy information obtained using **RETR_CCOMP** was used to classify every contour.

- Parent contours represent the outer donut boundary.
- Child contours represent the inner hole.

Only child contours associated with valid parent contours were accepted.

## Why Hierarchy Instead of Shape-Based Classification?

Shape descriptors such as circularity were considered during development. However, several donuts become slightly deformed after thresholding and some are only partially visible near the image boundaries. Relying on shape measurements would incorrectly reject these valid donuts.

Contour hierarchy provides a simpler and more reliable solution because every valid hole naturally exists inside a parent donut contour.

---

# Constraint 6: Binary Mask Refinement

## Problem

Contours alone only represent object boundaries. Complete object regions are required for visualization and further analysis.

## Applied Solution

Accepted contours were filled completely to generate two binary masks:

- Donut Body Mask
- Donut Hole Mask

Generating separate masks simplifies subsequent analysis and allows each region to be evaluated independently.

---

# Constraint 7: Overlay Verification

## Problem

Binary masks alone make it difficult to determine whether the segmented regions accurately correspond to the original donuts.

## Applied Solution

The refined masks were superimposed onto the original RGB image.

- Green indicates the donut body.
- Red indicates the donut hole.

The overlay images were used throughout development to visually inspect segmentation quality and identify remaining false positives or missing regions.

---

# Summary

The post-processing stage significantly improves the quality of the segmented masks by removing background noise, reconnecting fragmented donut boundaries, filtering invalid contours, and separating donut bodies from their inner holes. During development, several alternative approaches—including larger morphological kernels, different contour thresholds, Hough Circle Transform, and shape-based filtering—were evaluated. However, these methods either increased false detections, failed to detect partially visible donuts, or removed valid donut regions. Consequently, contour hierarchy combined with morphological refinement and area-based filtering provided the most reliable and computationally efficient solution for the industrial conveyor belt images used in this study.
