import cv2
import numpy as np
from .constants import MOTION_PREV_FRAME, MOTION_THRESHOLD

"""
Motion detection based on frame difference method
:param frame: Original frame (BGR format)
:param min_area: Minimum motion area pixel count (threshold)
:param debug: Enable debug logging
:return: True=motion detected (infer), False=no motion (skip)
"""
def detect_motion(frame, min_area=500, debug=False):

    global MOTION_PREV_FRAME
    
    if debug:
        print(f"\n[MOTION DEBUG] Original frame size: {frame.shape}, total pixels: {frame.size}")
    
    # Preprocess: resize + grayscale + gaussian blur (denoising)
    small_frame = cv2.resize(frame, (320, 240))
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    if debug:
        print(f"[MOTION DEBUG] Preprocessed size: {gray.shape}, pixel mean: {np.mean(gray):.2f}")
    
    # Initialize with first frame (force inference)
    if MOTION_PREV_FRAME is None:
        MOTION_PREV_FRAME = gray
        if debug:
            print("[MOTION DEBUG] First frame, initialize background, force inference")
        return True
    
    # Calculate frame difference + binarization
    frame_delta = cv2.absdiff(MOTION_PREV_FRAME, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    
    if debug:
        delta_sum = np.sum(frame_delta)
        thresh_sum = np.sum(thresh) / 255
        print(f"[MOTION DEBUG] Frame delta sum: {delta_sum:.0f}, motion pixels: {thresh_sum:.0f}")
    
    # Find contours (compatible with OpenCV 3/4)
    contours = None
    if cv2.__version__.startswith('4'):
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if debug:
        print(f"[MOTION DEBUG] Detected contours: {len(contours) if contours else 0}")
    
    # Check valid motion areas
    motion_detected = False
    max_contour_area = 0
    if contours:
        for contour in contours:
            area = cv2.contourArea(contour)
            max_contour_area = max(max_contour_area, area)
            if area > min_area:
                motion_detected = True
                break
    
    if debug:
        print(f"[MOTION DEBUG] Max contour area: {max_contour_area:.0f}, threshold: {min_area}, motion detected: {motion_detected}")
    
    # Update previous frame only if no motion (avoid background overwrite from minor jitter)
    if not motion_detected:
        MOTION_PREV_FRAME = gray
        if debug:
            print("[MOTION DEBUG] No valid motion, update background frame")
    
    # Log final result (only non-debug critical info)
    if motion_detected:
        print(f"🔍 Valid motion detected (max contour area: {max_contour_area:.0f} ≥ threshold {min_area}), perform inference")
    else:
        print(f"🔍 No valid motion (max contour area: {max_contour_area:.0f} < threshold {min_area}), skip inference")
    
    return motion_detected