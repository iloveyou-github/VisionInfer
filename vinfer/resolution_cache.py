import subprocess
from .constants import RESOLUTION_CACHE

def get_rtsp_resolution(rtsp_url, debug=False):
    cache_key = rtsp_url
    if cache_key in RESOLUTION_CACHE:
        return RESOLUTION_CACHE[cache_key]
    
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'csv=p=0',
            '-rtsp_transport', 'tcp',
            rtsp_url
        ]
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=10
        )
        output = result.stdout.decode().strip()
        if output and ',' in output:
            width, height = map(int, output.split(','))
            RESOLUTION_CACHE[cache_key] = (width, height)
            if debug:
                print(f"📌 RTSP resolution: {width}x{height} (cached)")
            return width, height
        else:
            RESOLUTION_CACHE[cache_key] = (640, 480)
            print("📌 Resolution detection failed, using default 640x480")
            return 640, 480
    except Exception as e:
        RESOLUTION_CACHE[cache_key] = (640, 480)
        print(f"📌 Resolution detection exception: {e}, using default 640x480")
        return 640, 480