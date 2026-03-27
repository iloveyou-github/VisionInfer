import subprocess
import os
import signal
import psutil
import time
from ..constants import ollama_process
from ..utils import logger

def start_ollama_serve():
    global ollama_process
    try:
        if is_ollama_running():
            print("✅ Ollama service is already running")
            return True
        
        print("🚀 Starting Ollama service...")
        ollama_process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid,
            shell=False
        )
        time.sleep(2)
        
        if ollama_process.poll() is None and is_ollama_running():
            print("✅ Ollama service started successfully")
            return True
        else:
            print("❌ Failed to start Ollama service")
            return False
    except Exception as e:
        print(f"❌ Exception starting Ollama: {e}")
        return False

def is_ollama_running():
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['name'] == 'ollama' and 'serve' in proc.info['cmdline']:
                return True
        return False
    except:
        return False

'''
def stop_ollama_serve():
    global ollama_process
    try:
        if ollama_process and ollama_process.poll() is None:
            os.killpg(os.getpgid(ollama_process.pid), signal.SIGTERM)
            print("✅ Ollama service terminated")
        else:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if proc.info['name'] == 'ollama' and 'serve' in proc.info['cmdline']:
                    proc.terminate()
                    print(f"✅ Terminated Ollama process (PID: {proc.info['pid']})")
    except Exception as e:
        print(f"⚠️ Exception terminating Ollama: {e}")


def stop_ollama_serve():
    """停止Ollama服务（仅清理当前用户的进程，跳过系统级进程）"""
    global ollama_process
    current_uid = os.getuid()  # 获取当前用户的UID（关键！）
    
    # 1. 停止程序自身启动的ollama进程（原有逻辑保留）
    if ollama_process and ollama_process.poll() is None:
        try:
            ollama_process.terminate()
            ollama_process.wait(timeout=10)
            logger.info(f"Stopped self-started Ollama process (PID: {ollama_process.pid})")
        except Exception as e:
            logger.warning(f"Failed to stop self-started Ollama process: {e}")
        finally:
            ollama_process = None
    
    # 2. 清理残留进程：仅清理当前用户启动的Ollama进程（核心优化）
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'uids']):
        try:
            # 跳过无权限访问的进程（如root进程）
            proc_uids = proc.info['uids']
            if not proc_uids:
                continue
            # 仅处理当前用户启动的进程（匹配real UID）
            if proc_uids.real != current_uid:
                continue
            
            # 匹配Ollama进程（排除grep/无关进程）
            is_ollama = False
            if proc.info['name'] and 'ollama' in proc.info['name'].lower():
                is_ollama = True
            if proc.info['cmdline'] and 'ollama serve' in ' '.join(proc.info['cmdline']).lower():
                is_ollama = True
            
            if is_ollama:
                pid = proc.info['pid']
                if pid == os.getpid() or pid == 1:  # 跳过自身/init进程
                    continue
                # 终止当前用户的Ollama进程
                proc.terminate()
                proc.wait(timeout=5)
                logger.info(f"Cleaned residual Ollama process (PID: {pid}, user-owned)")
        except psutil.NoSuchProcess:
            continue  # 进程已退出，忽略
        except psutil.AccessDenied:
            # 明确跳过无权限的系统级进程，不记录警告（关键！）
            continue
        except Exception as e:
            logger.warning(f"Failed to clean user-owned Ollama process: {e}")
'''

def stop_ollama_serve():
    
    try:
        os.system("sudo pkill -f ollama")
    except:
        pass

    try:
        for proc in psutil.process_iter(attrs=['pid']):
            try:
                pid = proc.info['pid']

                try:
                    cmdline = open(f"/proc/{pid}/cmdline", "rb").read().decode("latin1")
                    if "ollama" in cmdline:
                        if pid == os.getpid():
                            continue
                        os.kill(pid, signal.SIGKILL)
                except:
                    continue
            except:
                continue
    except:
        pass


def get_ollama_usage_data():
    return {"status": "Not implemented", "models": []}

def get_ollama_inference_perf(model_name):
    return {"status": "Not implemented", "model": model_name}

def print_ollama_usage():
    """Print Ollama API usage data (compatible with low versions)"""
    print("\n" + "="*60)
    print("📊 Ollama API Usage Monitoring (compatible with low versions)")
    print("="*60)
    usage_data = get_ollama_usage_data()
    
    for key, value in usage_data.items():
        print(f"\n🔹 {key}:")
        if isinstance(value, list):
            if len(value) == 0:
                print("  No data")
            else:
                for idx, item in enumerate(value):
                    print(f"  [{idx+1}] Model name: {item.get('name', 'Unknown')}")
                    if "pid" in item:
                        print(f"     PID: {item.get('pid', 'Not obtained')}")
                    if "size" in item and item["size"] > 0:
                        print(f"     Size: {round(item.get('size', 0)/1024/1024/1024, 2)}GB")
                    if "modified_at" in item and item["modified_at"] != "Unknown":
                        print(f"     Last updated: {item.get('modified_at', 'Unknown')}")
                    if "ports" in item and item["ports"] != "None":
                        print(f"     Ports used: {item.get('ports', 'None')}")
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                print(f"  - {sub_key}: {sub_value}")
        else:
            print(f"  {value}")
    print("\n" + "="*60)

def print_ollama_perf(model_name):
    """Print inference performance data (standard fields from official docs)"""
    print("\n" + "="*80)
    print("📊 Ollama /api/generate Inference Performance Monitoring (official standard fields)")
    print("="*80)
    perf_data = get_ollama_inference_perf(model_name)
    
    for key, value in perf_data.items():
        print(f"\n🔹 {key}:")
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                print(f"  - {sub_key}: {sub_value}")
        else:
            print(f"  {value}")
    print("\n" + "="*80)