import os
import subprocess
import webview
import threading
from flask import Flask, render_template
print(os.getcwd())
app = Flask(__name__)


@app.route('/')
def index():
    # Hiển thị giao diện chào mừng
    return render_template('index.html')

@app.route('/start_game')
def start_game():
    # Sử dụng đường dẫn tương đối, vì SnakeGame.py nằm cùng thư mục với app.py
    snake_game_path = 'SnakeGame.py'

    # Chạy trò chơi Snake bằng subprocess
    subprocess.Popen(['python', snake_game_path])

    return "Snake game started!"

# Khởi động Flask trên một luồng riêng
def run_flask():
    app.run()

if __name__ == '__main__':
    # Khởi động Flask trên một luồng riêng để giữ cho luồng chính trống
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Tạo cửa sổ PyWebView để hiển thị giao diện SnakeGame khi truy cập vào /start_game
    webview.create_window('Snake Game', 'http://localhost:5000/start_game')
    webview.start()