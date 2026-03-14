import time
import queue
import threading
import cv2
import numpy as np
from .constants import (
    FRAME_THREAD_RUNNING, FRAME_INTERVAL, LAST_FRAME_FEATURE,
    EXIT_FLAG, FRAME_QUEUE, FRAME_INFO_QUEUE, FRAME_THREAD
)
from .frame_processing import compress_frame, is_frame_duplicate
from .utils import get_usb_frame, extract_frame_stable
from .motion_detection import detect_motion

def frame_producer_thread(args):
    """Fixed frequency frame extraction thread with compression + deduplication"""
    global FRAME_THREAD_RUNNING, FRAME_INTERVAL, LAST_FRAME_FEATURE
    FRAME_THREAD_RUNNING = True
    last_frame_time = 0
    
    # Parse compression resolution
    try:
        compress_width, compress_height = map(int, args.compress_size.split('x'))
        compress_size = (compress_width, compress_height)
    except:
        print(f"⚠️ Invalid compression resolution parameter, using default 320x240")
        compress_size = (320, 240)
    
    while FRAME_THREAD_RUNNING and not EXIT_FLAG:
        current_time = time.time()
        if current_time - last_frame_time < FRAME_INTERVAL:
            time.sleep(0.1)
            continue
        
        try:
            # Extract frame
            frame = None
            if args.source_type == "usb":
                frame = get_usb_frame(args.usb_dev)
            elif args.source_type == "rtsp":
                frame = extract_frame_stable(args.source_url, "rtsp")
            
            if frame is None:
                if args.debug:
                    print("⚠️ Frame extraction failed, skip this time")
                last_frame_time = time.time()
                continue
            
            # Frame deduplication (time-based)
            if (args.dedup or args.motion_gate) and is_frame_duplicate(frame, args.debug):
                last_frame_time = time.time()
                continue
            
            # Frame compression
            start_img = time.time()
            compress_result = compress_frame(
                frame, 
                target_size=compress_size, 
                jpg_quality=args.jpg_quality
            )
            img_cost = time.time() - start_img
            
            if not compress_result["success"]:
                if args.debug:
                    print("⚠️ Frame compression failed, skip this time")
                last_frame_time = time.time()
                continue
            
            # Put to queue (overwrite old frame)
            try:
                if not FRAME_QUEUE.empty():
                    FRAME_QUEUE.get_nowait()
                if not FRAME_INFO_QUEUE.empty():
                    FRAME_INFO_QUEUE.get_nowait()
                
                FRAME_QUEUE.put(compress_result["data"], timeout=0.1)
                FRAME_INFO_QUEUE.put({
                    "img_cost": img_cost,
                    "frame_shape": compress_result["shape"],
                    "img_size_kb": compress_result["size_kb"],
                    "jpg_quality": compress_result["quality"]
                }, timeout=0.1)
                
                if args.debug:
                    print(f"✅ Latest frame ready (size: {compress_result['shape']}, size: {compress_result['size_kb']}KB, encode time: {img_cost:.2f}s)")
            except queue.Full:
                if args.debug:
                    print("⚠️ Inference queue full, skip frame extraction")
            
            last_frame_time = time.time()
        
        except Exception as e:
            if not EXIT_FLAG and args.debug:
                print(f"⚠️ Frame extraction/encoding exception: {e}")
            last_frame_time = time.time()
    
    print("✅ Frame extraction thread exited")

def start_frame_producer(args):
    global FRAME_THREAD
    if FRAME_THREAD and FRAME_THREAD.is_alive():
        return
    FRAME_THREAD = threading.Thread(target=frame_producer_thread, args=(args,), daemon=True)
    FRAME_THREAD.start()
    print(f"🚀 Frame extraction thread started (frequency: {FRAME_INTERVAL}s/frame)")

def stop_frame_producer():
    global FRAME_THREAD_RUNNING
    FRAME_THREAD_RUNNING = False
    if FRAME_THREAD and FRAME_THREAD.is_alive():
        FRAME_THREAD.join(timeout=2)
    # Clear queues
    while not FRAME_QUEUE.empty():
        FRAME_QUEUE.get_nowait()
    while not FRAME_INFO_QUEUE.empty():
        FRAME_INFO_QUEUE.get_nowait()
    print("✅ Frame extraction thread stopped")