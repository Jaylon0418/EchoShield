import threading
import time
import pyperclip  # 读取剪贴板
import re

class KeyLogger:
    def __init__(self):
        self.current_text = ""  # 存储输入的文本
        self.lock = threading.Lock()
        self.last_clipboard = ""  # 记录上次剪贴板内容，避免重复

    def start(self):
        """启动剪贴板监听线程"""
        self.listener_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        self.listener_thread.start()
        print("Keylogger (Clipboard Mode) started successfully.")

    def monitor_clipboard(self):
        """监听剪贴板内容"""
        while True:
            try:
                clipboard_text = pyperclip.paste().strip()  # 读取剪贴板内容
                if clipboard_text and clipboard_text != self.last_clipboard:
                    self.last_clipboard = clipboard_text  # 更新记录

                    # 仅提取中文和标点
                    chinese_text = "".join(re.findall(r"[\u4e00-\u9fa5，。！？；：“”‘’（）【】—…]", clipboard_text))

                    # 避免复制代码等无关内容
                    if chinese_text and len(chinese_text) < 100:  # 限制长度，防止误检测
                        with self.lock:
                            self.current_text += chinese_text
                        print(f"捕获的中文文本: {self.current_text}")  # Debug 输出

            except Exception as e:
                print(f"剪贴板监听错误: {e}")

            time.sleep(0.5)  # 每 0.5 秒检测一次剪贴板

    def get_text(self):
        """获取当前记录的文本"""
        with self.lock:
            print(f"get_text() 返回: {self.current_text}")  # Debug
            return self.current_text

    def clear_text(self):
        """清空当前文本"""
        with self.lock:
            self.current_text = ""
        print("Keylogger: 文本已清空")  # Debug log

# **创建全局实例**
keylogger_instance = KeyLogger()
keylogger_instance.start()