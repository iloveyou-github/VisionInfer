import re
import argparse
from .constants import DEFAULT_PROMPT, YOLO_MODEL, YOLO_TASK

def add_common_arguments(parser):
    """Add common arguments for all subcommands"""
    # Model parameter (default qwen3.5-2b)
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="qwen3.5:2b",
        help="Ollama model name"
    )
    # Compression resolution (default 480x360)
    parser.add_argument(
        "--compress-size", "-s",
        type=str,
        default="480x360",
        help="Frame compression resolution (format: widthxheight)"
    )
    # JPG quality
    parser.add_argument(
        "--jpg-quality", "-q",
        type=int,
        default=70,
        help="JPG compression quality (0-100)"
    )
    # Motion gating
    parser.add_argument(
        "--motion-gate", "-g",
        action="store_true",
        help="Enable motion gating (infer only when motion detected)"
    )
    # Motion threshold
    parser.add_argument(
        "--motion-threshold", "-T",
        type=int,
        default=500,
        help="Minimum pixel threshold for motion detection"
    )
    # Deduplication
    parser.add_argument(
        "--dedup", "-D",
        action="store_true",
        help="Enable L2 similar frame deduplication (disabled if motion-gate is on)"
    )
    # Inference interval
    parser.add_argument(
        "--interval", "-i",
        type=float,
        default=1.0,
        help="Inference interval (seconds/frame)"
    )
    # Debug mode
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug logging (verbose output)"
    )
    # Prompt
    parser.add_argument(
        "--prompt", "-r",
        type=str,
        default=DEFAULT_PROMPT,
        help="User-defined prompts"
    )
    # Accelerate
    parser.add_argument(
        "--accelerate", "-a",
        action="store_true",
        help="Accelerate reasoning speed"
    )
    # Yolo version
    parser.add_argument(
        "--yolo-version", "-yv",
        type=int,
        default=11,
        choices=[8, 11, 26], 
        help="YOLO version"
    )
        # Yolo version
    parser.add_argument(
        "--yolo-task", "-yt",
        type=str, 
        default='detection', 
        choices=['detection', 'segment', 'classify', 'pose', 'obb'],
        help='任务类型：detection(定向检测)/segment(实例分割)/classify(图像分类)/pose(姿势估计)/obb(定向物体检测)，默认值：detection'
    )

def get_inference_model_name(args, check_pattern: str):
    """
    Get the inference model name according to specified rules, supporting YOLO model parsing and default model return
    
    Args:
        args: Parsed command line argument object, which should contain model, yolo_version, yolo_task attributes
        check_pattern: Check mode, execute YOLO parsing logic only when it is 'yolo'
    
    Returns:
        str: Parsed model name, return args.model in non-YOLO mode
    """

    if check_pattern != 'yolo':
        return False, args.model if hasattr(args, 'model') else ''

    # Initialize default values
    default_version = 8
    default_task = 'detection'
    yolo_version = default_version
    yolo_task = default_task

    # Get model parameter and handle empty value
    model_str = args.model if (hasattr(args, 'model') and args.model) else ''
    if not model_str:
        # Read command line parameters when there is no model value
        if hasattr(args, 'yolo_version') and args.yolo_version in [8, 11, 26]:
            yolo_version = args.yolo_version

        if hasattr(args, 'yolo_task') and args.yolo_task in ['detection', 'segment', 'classify', 'pose', 'obb']:
            yolo_task = args.yolo_task
        return True, get_model_filename(yolo_version, yolo_task)

    # Parse YOLO rules in model string
    if 'yolo' in model_str.lower():
        # Extract version number (8/11/26)
        version_match = re.search(r'(\d+)', model_str)
        if version_match:
            version = int(version_match.group(1))
            if version in [8, 11, 26]:
                yolo_version = version

        # Read command line yolo-version parameter (higher priority than model string)
        if hasattr(args, 'yolo_version') and args.yolo_version in [8, 11, 26]:
            yolo_version = args.yolo_version
        
        # Read command line yolo-task parameter
        if hasattr(args, 'yolo_task') and args.yolo_task in ['detection', 'segment', 'classify', 'pose', 'obb']:
            yolo_task = args.yolo_task

        return True, get_model_filename(yolo_version, yolo_task)

    # Return original model value in non-YOLO mode
    return False, model_str

# Placeholder for dependent get_model_filename function (ensure this function is defined in the code)
def get_model_filename(version, task):

    YOLO_TASK = task
    YOLO_MODEL = f"YOLO{version}n"

    """Placeholder function, need to be implemented according to actual business logic"""
    task_suffix_map = {
        'detection': '',       
        'segment': '-seg',     
        'classify': '-cls',    
        'pose': '-pose',       
        'obb': '-obb'      
    }
    
    suffix = task_suffix_map[task]
    model_name = f'yolo{version}n{suffix}.pt'
    print(f"model_name : {model_name}")
    return model_name