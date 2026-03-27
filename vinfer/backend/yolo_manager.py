import subprocess
import os
import signal
import psutil
import time
from ..utils import logger
from ultralytics import YOLO

yolo_model = None

def yolo_load_model(model_name):
    
    global yolo_model
    
    print(f'Loading {model_name} ......')
    try:
        yolo_model = YOLO(f"./models/{model_name}")  # 自动下载（如果本地没有）
    except Exception as e:
        print(f'Failed to load : {e}')
    

def yolo_infer_frame_yolo(raw_image_data):

    global yolo_model

    # out = None
    # if args.savevideo:
    #     # 6. 自动创建保存目录
    #     os.makedirs(args.savepath, exist_ok=True)
    #     # 生成输出视频文件名
    #     video_filename = get_output_video_filename(args.modelversion, args.task)
    #     video_path = os.path.join(args.savepath, video_filename)
    #     # 创建视频写入对象
    #     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #     out = cv2.VideoWriter(video_path, fourcc, fps, (frame_width, frame_height))
    #     print(f'视频将保存至：{video_path}')
    
    if not yolo_model:
        return None
      
    results = yolo_model(raw_image_data, verbose=False)
        
    annotated_frame = results[0].plot()
    # for r in results:
    #     annotated_frame = r.plot()  # 对每个结果帧绘制标注
    
    # if args.savevideo and out is not None:
    #     out.write(annotated_frame)
    return  annotated_frame
