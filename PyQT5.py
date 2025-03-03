import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from keylogger import keylogger_instance
from DBAI import get_ai_response

class FloatingChatWindow(QWidget):
    def __init__(self, keylogger):
        super().__init__()
        self.keylogger = keylogger
        self.last_ai_response = ["", ""]  
        self.thinking_timer = QTimer()  
        self.thinking_state = 0  

        print("FloatingChatWindow initialized")  

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.old_pos = None  

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setAlignment(Qt.AlignRight)  

        self.minimize_button = QPushButton("_")
        self.minimize_button.setFixedSize(20, 20)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(100, 100, 100, 150);
                color: white;
                font-size: 14px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(150, 150, 150, 200);
            }
        """)
        self.minimize_button.clicked.connect(self.showMinimized)

        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(200, 50, 50, 150);
                color: white;
                font-size: 14px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(255, 50, 50, 200);
            }
        """)
        self.close_button.clicked.connect(self.close)

        button_layout.addWidget(self.minimize_button)
        button_layout.addWidget(self.close_button)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            background-color: rgba(50, 50, 50, 180);
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
        """)

        self.api_response_display = QTextEdit()
        self.api_response_display.setReadOnly(True)
        self.api_response_display.setStyleSheet("""
            background-color: rgba(30, 30, 30, 180);
            color: cyan;
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
        """)

        layout.addLayout(button_layout)  
        layout.addWidget(self.chat_display)
        layout.addWidget(self.api_response_display)
        self.setLayout(layout)
        self.setGeometry(100, 100, 400, 300)  

        self.update_chat()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        border_color = QColor(200, 200, 200, 180)  
        pen = QPen(border_color)
        pen.setWidth(5)  
        painter.setPen(pen)
        
        background_brush = QBrush(QColor(0, 0, 0, 150))  
        painter.setBrush(background_brush)

        painter.drawRoundedRect(self.rect(), 15, 15)

    def update_chat(self):
        try:
            text = self.keylogger.get_text()
            print(f"更新悬浮窗文本: {text}")  

            if text.endswith("。"):  
                print("检测到句号，向 DBAI 发送请求...")
                self.start_thinking_animation()  
                QTimer.singleShot(500, lambda: self.send_to_api(text))  
                self.keylogger.clear_text()  

        except Exception as e:
            print(f"更新悬浮窗时出错: {e}")
        QTimer.singleShot(500, self.update_chat)  

    def start_thinking_animation(self):
        """启动 '思考中...' 并确保 UI 立即更新"""
        self.thinking_state = 0
        self.update_thinking_text() 
        self.thinking_timer.timeout.connect(self.update_thinking_text)
        self.thinking_timer.start(500)  

    def update_thinking_text(self):
        """更新 '思考中...' 并确保 UI 变化生效"""
        thinking_states = ["思考中.", "思考中..", "思考中..."]
        self.chat_display.setText(thinking_states[self.thinking_state])
        self.thinking_state = (self.thinking_state + 1) % 3  
        QApplication.processEvents()

    def stop_thinking_animation(self):
        """停止 '思考中...' 动画"""
        self.thinking_timer.stop()

    def send_to_api(self, text):
        """调用 DBAI 获取 AI 结果，并更新 UI"""
        try:
            ai_response = get_ai_response(text)
            print(f"DBAI 响应: {ai_response}")  

            self.stop_thinking_animation()  

            lines = ai_response.strip().split("\n")  
            first_line = lines[0] if len(lines) > 0 else "（无内容）"
            second_line = lines[1] if len(lines) > 1 else "（无更多内容）"

            self.last_ai_response = [first_line, second_line]
            self.chat_display.setText(first_line)
            self.api_response_display.setText(second_line)

            self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())
            self.api_response_display.verticalScrollBar().setValue(self.api_response_display.verticalScrollBar().maximum())

        except Exception as e:
            print(f"DBAI API 调用失败: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    print("Initializing keylogger...")  
    window = FloatingChatWindow(keylogger_instance)  
    window.show()
    sys.exit(app.exec_())
