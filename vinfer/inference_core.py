import time
import ollama
from .constants import EXIT_FLAG, DEFAULT_PROMPT
from .utils import detect_language

def infer_frame(args, raw_image_data, timeout: int = 30):
    import ollama
    client = ollama.Client()
    if args.debug:
        print(f"🔍 Calling Ollama inference (image size: {len(raw_image_data)/1024:.1f}KB)")
    start_infer = time.time()
    
    if (args.prompt != DEFAULT_PROMPT) and args.accelerate: 
        lang = detect_language(args.prompt)
        if lang == "zh":
            constraint = "，请确保你的回答控制在50字以内，语言简洁。"
        elif lang == "en":
            constraint = ", please ensure your answer is within 50 words and concise."
        else:
            constraint = "，请确保回答控制在50字/50 words以内。/ Please keep your answer within 50 words/50 Chinese characters."
    else:
        constraint = ""
        
    try:
        prompt = args.prompt + constraint
        stream = client.chat(
            model=args.model,
            messages=[{"role": "user", "content": prompt, "images": [raw_image_data]}],
            stream=True,
            think=False,
            keep_alive="24h",
            options={
                "max_tokens": 200,
                "temperature": 0.0,
                "num_ctx": 512
            }
        )
        
        result = ""
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                result += chunk['message']['content']
        
        infer_cost = time.time() - start_infer
        return result.strip(), infer_cost
    
    except Exception as e:
        return f"Inference failed: {str(e)}", time.time() - start_infer