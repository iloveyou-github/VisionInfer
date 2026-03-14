import cv2
import numpy as np
from .constants import LAST_FRAME_FEATURE, DEDUP_THRESHOLD

"""
Frame compression: resolution scaling + JPG quality compression
:param frame: Original frame (BGR format)
:param target_size: Compressed resolution (width, height)
:param jpg_quality: JPG compression quality (0-100, higher = better quality)
:return: Compressed image data and metadata
"""
def compress_frame(frame, target_size=(320, 240), jpg_quality=70):

    try:
        # Resize (INTER_AREA is optimal for downscaling)
        frame_resized = cv2.resize(frame, target_size, interpolation=cv2.INTER_AREA)
        # JPG compression
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality]
        _, img_bytes = cv2.imencode('.jpg', frame_resized, encode_param)
        raw_image_data = img_bytes.tobytes()
        
        return {
            "data": raw_image_data,
            "shape": frame_resized.shape,
            "size_kb": round(len(raw_image_data)/1024, 1),
            "quality": jpg_quality,
            "success": True
        }
    except Exception as e:
        print(f"⚠️ Frame compression failed: {e}")
        return {"success": False}

"""
Extract frame feature: 64x64 grayscale + normalization + flatten (L2 feature)
:param frame: Original frame (BGR format)
:return: 1D feature array (4096 dimensions)
"""
def extract_frame_feature(frame):

    small_frame = cv2.resize(frame, (64, 64), interpolation=cv2.INTER_AREA)
    gray_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    normalized_frame = gray_frame / 255.0
    feature = normalized_frame.flatten()
    return feature

"""
Check for similar frames using L2 distance comparison
:param frame: Original frame (BGR format)
:param debug: Enable debug logging
:return: True=similar frame (skip), False=different frame (infer)
"""
def is_frame_duplicate(frame, debug=False):

    global LAST_FRAME_FEATURE, DEDUP_THRESHOLD
    
    current_feature = extract_frame_feature(frame)
    
    # First frame (no comparison)
    if LAST_FRAME_FEATURE is None:
        LAST_FRAME_FEATURE = current_feature
        return False
    
    # Calculate L2 distance
    l2_distance = np.linalg.norm(current_feature - LAST_FRAME_FEATURE)
    LAST_FRAME_FEATURE = current_feature
    
    # Check threshold
    if l2_distance < DEDUP_THRESHOLD:
        if debug:
            print(f"🔍 Similar frame (L2 distance: {l2_distance:.2f} < threshold {DEDUP_THRESHOLD}), skip inference")
        return True
    else:
        if debug:
            print(f"🔍 Different frame (L2 distance: {l2_distance:.2f} ≥ threshold {DEDUP_THRESHOLD}), perform inference")
        return False