# Results and Failure Analysis

## Results

The proposed segmentation pipeline was evaluated on 10 industrial conveyor images. The generated overlay images were visually inspected to evaluate the quality of donut body and hole segmentation.

Overall, the pipeline produced satisfactory results. The majority of donut bodies were successfully segmented, and the corresponding inner holes were correctly identified for most complete donuts. The generated masks closely followed the actual donut boundaries, producing clear separation between the donut body and its center hole.

The algorithm also demonstrated consistent performance across all five frames despite slight variations in donut positions and conveyor lighting. Most donuts were detected individually, and partially visible donuts near the image boundaries were still successfully segmented, although with incomplete masks due to limited visibility.

The preprocessing pipeline effectively reduced image noise while preserving the overall donut shape, allowing contour extraction to generate accurate masks for most objects. The generated overlay images confirm that the proposed approach is suitable for segmenting donuts under normal industrial operating conditions.

However, several limitations were observed during experimentation. Most of these limitations were caused by environmental conditions rather than the contour extraction itself.

---

# Failure Analysis and Attempted Improvements

## 1. Severe Paint Degradation on the Machine Base

The largest source of segmentation error is the machine base located on the left side of every image. The paint on this surface has severely degraded over time, exposing patches whose intensity becomes very similar to the donut dough after preprocessing. Consequently, the contour extraction consistently detects this entire region as a large donut object, producing significant false positive segmentation.

### Attempted Improvements

Different parent contour area thresholds were tested in an attempt to remove this false detection. Although increasing the minimum contour area reduced some unwanted regions, it also removed partially visible donuts near the image borders. Since this background object remains fixed in every frame, contour filtering alone could not eliminate the problem.

### Recommended Solution

- Crop the left side of the image before processing.
- Define a fixed Region of Interest (ROI).
- Apply a permanent exclusion mask for the machine base.

---

## 2. Small Gaps Around Donut Boundaries

Some donuts contain small missing sections along their outer boundaries, particularly in darker regions of the conveyor.

### Attempted Improvements

Larger morphological closing kernels were tested to reconnect these broken boundaries. Although the gaps became smaller, increasing the kernel size caused nearby regions to merge together and slightly distorted the donut shapes. The current kernel size therefore provided the best balance between connectivity and shape preservation.

### Recommended Solution

- Apply illumination correction before segmentation.
- Use adaptive morphological operations based on object size.

---

## 3. Missing Hole Detection

Most donut holes were detected correctly; however, a few donuts contained incomplete or missing hole masks due to low contrast inside the donut center.

### Attempted Improvements

The minimum child contour area threshold was reduced to preserve smaller hole contours. While this recovered several missing holes, it also introduced additional false hole detections caused by conveyor reflections and image noise. Increasing the maximum child contour area did not noticeably improve the results.

### Recommended Solution

- Improve local image contrast.
- Use adaptive contour filtering instead of fixed area thresholds.

---

## 4. Uneven Illumination

The conveyor exhibits noticeable lighting variation due to overhead illumination and vertical reflections. Although Otsu thresholding automatically determines a threshold value for each image, it still applies one global threshold to the entire frame.

Consequently, brighter regions are segmented more accurately than darker regions.

### Attempted Improvements

Different Gaussian blur kernel sizes were evaluated before thresholding. Increasing the blur reduced random noise but also softened donut edges, resulting in less accurate contours. Adjusting preprocessing parameters improved certain images but reduced segmentation quality in others.

### Recommended Solution

- Apply adaptive thresholding.
- Perform illumination normalization before segmentation.
- Improve lighting consistency during image acquisition.

---

## 5. Background Noise

Small isolated regions remain visible around conveyor edges and machine components due to background pixels having similar intensity to the donuts.

### Attempted Improvements

Additional morphological opening operations were tested to remove these small regions. Although the background noise decreased, several valid donut pixels were also removed, especially from partially visible donuts. Increasing the contour area threshold produced similar trade-offs.

### Recommended Solution

- Remove connected components below a dynamic size threshold.
- Combine contour filtering with additional shape-based filtering.

---

## 6. Fixed Processing Parameters

The preprocessing pipeline uses fixed Gaussian kernel sizes, morphological kernels, and contour area thresholds.

While these parameters perform well on the current dataset, they may not generalize well to different conveyor speeds, camera positions, image resolutions, or donut sizes.

### Attempted Improvements

Multiple combinations of Gaussian blur sizes, morphological kernel sizes, and contour area thresholds were evaluated throughout the development process. Individual parameter settings improved segmentation for specific images but reduced performance for others. No single parameter combination produced perfect results across every test image.

### Recommended Solution

- Dynamically scale parameters according to image resolution.
- Automatically estimate contour thresholds based on object size.
- Optimize parameters using a larger validation dataset.

---

# Overall Discussion

The experimental results demonstrate that the proposed classical computer vision pipeline is capable of accurately segmenting donut bodies and their inner holes under normal industrial conditions. Most segmentation errors originate from environmental challenges rather than the contour extraction algorithm itself.

Parameter tuning significantly improved segmentation quality during development. However, each attempted improvement introduced a trade-off between reducing false positives and preserving valid donut regions. Increasing contour thresholds removed legitimate objects, larger morphological kernels distorted donut boundaries, and additional noise removal operations eliminated small but valid features.

Consequently, the final parameter values were selected as the best compromise after evaluating multiple combinations across all five test images.

The remaining limitations are primarily caused by severe paint degradation on the machine base, uneven illumination, reflections, and background clutter. These issues are difficult to eliminate completely using classical image processing alone. Future improvements would likely require Region of Interest (ROI) masking, adaptive thresholding, illumination normalization, or learning-based segmentation methods to achieve higher robustness in real industrial environments.
