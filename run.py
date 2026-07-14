import cv2
import numpy as np
import os
import glob

def preprocess_image(image):
    try:
        b, g, r = cv2.split(image)
        diff = cv2.subtract(r, b)
        
        diff_norm = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX)
        blurred = cv2.GaussianBlur(diff_norm, (5, 5), 0)
        
        pad = 20
        padded = cv2.copyMakeBorder(blurred, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
        
        _, thresh = cv2.threshold(padded, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_open, iterations=1)
        
        kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close, iterations=1)
        
        return closed[pad:-pad, pad:-pad]
    except Exception as e:
        raise RuntimeError(f"Preprocessing failed: {str(e)}")

def extract_masks(thresh, original_shape):
    try:
        donut_mask = np.zeros(original_shape[:2], dtype=np.uint8)
        hole_mask = np.zeros(original_shape[:2], dtype=np.uint8)
        
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        
        if hierarchy is not None:
            for i, cnt in enumerate(contours):
                area = cv2.contourArea(cnt)
                parent_idx = hierarchy[0][i][3]
                
                if parent_idx == -1:
                    if area < 300: 
                        continue
                    cv2.drawContours(donut_mask, [cnt], -1, 255, -1)
                else:
                    if area < 10 or area > 5000: 
                        continue
                        
                    parent_area = cv2.contourArea(contours[parent_idx])
                    if parent_area < 300:
                        continue
                        
                    cv2.drawContours(hole_mask, [cnt], -1, 255, -1)
                    
        return donut_mask, hole_mask
    except Exception as e:
        raise RuntimeError(f"Contour extraction failed: {str(e)}")

def generate_overlay(image, donut_mask, hole_mask):
    try:
        overlay = image.copy()
        overlay[donut_mask == 255] = [0, 255, 0]
        overlay[hole_mask == 255] = [0, 0, 255]
        return cv2.addWeighted(image, 0.7, overlay, 0.3, 0)
    except Exception as e:
        raise RuntimeError(f"Overlay generation failed: {str(e)}")

def run_pipeline(input_folder, output_root="Donutstest"):
    try:
        if not os.path.exists(input_folder):
            raise FileNotFoundError(f"Input folder '{input_folder}' does not exist.")
            
        for folder in ["masks_donut", "masks_hole", "overlays"]:
            os.makedirs(os.path.join(output_root, folder), exist_ok=True)
            
        image_paths = glob.glob(os.path.join(input_folder, "*.*"))
        if not image_paths:
            raise ValueError(f"No images found in '{input_folder}'.")
            
        for img_path in image_paths:
            try:
                filename = os.path.basename(img_path)
                image = cv2.imread(img_path)
                if image is None: continue
                
                thresh = preprocess_image(image)
                donut_mask, hole_mask = extract_masks(thresh, image.shape)
                overlay = generate_overlay(image, donut_mask, hole_mask)
                
                cv2.imwrite(os.path.join(output_root, "masks_donut", f"donut_{filename}"), donut_mask)
                cv2.imwrite(os.path.join(output_root, "masks_hole", f"hole_{filename}"), hole_mask)
                cv2.imwrite(os.path.join(output_root, "overlays", f"overlay_{filename}"), overlay)
            except Exception as img_err:
                print(f"Skipping {filename} due to error: {str(img_err)}")
    except Exception as e:
        print(f"Pipeline execution halted: {str(e)}")

if __name__ == "__main__":
    INPUT_DIR = r"" 
    run_pipeline(INPUT_DIR)
