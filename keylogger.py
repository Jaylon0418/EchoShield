import threading
import time
import pyperclip 
import re

class KeyLogger:
    def __init__(self):
        self.current_text = "" 
        self.lock = threading.Lock()
        self.last_clipboard = ""  

    def start(self):
       
        self.listener_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        self.listener_thread.start()
        print("Keylogger (Clipboard Mode) started successfully.")

    def monitor_clipboard(self):
      
        while True:
            try:
                clipboard_text = pyperclip.paste().strip() 
                if clipboard_text and clipboard_text != self.last_clipboard:
                    self.last_clipboard = clipboard_text 

                    
                    chinese_text = "".join(re.findall(r"[\u4e00-\u9fa5，。！？；：“”‘’（）【】—…]", clipboard_text))

                   
                    if chinese_text and len(chinese_text) < 100: 
                        with self.lock:
                            self.current_text += chinese_text
                        print(f"捕获的中文文本: {self.current_text}") 

            except Exception as e:
                print(f"剪贴板监听错误: {e}")

            time.sleep(0.5)  

    def get_text(self):
        
        with self.lock:
            print(f"get_text() 返回: {self.current_text}") 
            return self.current_text

    def clear_text(self):
       
        with self.lock:
            self.current_text = ""
        print("Keylogger: 文本已清空")


keylogger_instance = KeyLogger()
keylogger_instance.start()
