
from flask import Flask, request, jsonify
import subprocess
import threading
import sys
import os

app = Flask(__name__)

# Biến để theo dõi trạng thái chạy
running_process = None

@app.route('/')
def home():
    return jsonify({
        "message": "SMS Bombing Server đang chạy",
        "endpoints": {
            "/start": "POST - Bắt đầu bombing với phone và count",
            "/status": "GET - Kiểm tra trạng thái"
        }
    })

@app.route('/start', methods=['POST'])
def start_bombing():
    global running_process
    
    try:
        data = request.get_json()
        phone = data.get('phone')
        count = data.get('count', 1)
        
        if not phone:
            return jsonify({"error": "Vui lòng cung cấp số điện thoại"}), 400
        
        # Kiểm tra xem có process nào đang chạy không
        if running_process and running_process.poll() is None:
            return jsonify({"error": "Có một process đang chạy"}), 400
        
        # Chạy main.py với input được cung cấp
        def run_main():
            global running_process
            try:
                # Tạo input string cho main.py
                input_data = f"{phone}\n{count}\n"
                
                running_process = subprocess.Popen(
                    [sys.executable, 'main.py'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = running_process.communicate(input=input_data)
                print(f"STDOUT: {stdout}")
                if stderr:
                    print(f"STDERR: {stderr}")
                    
            except Exception as e:
                print(f"Error running main.py: {e}")
        
        # Chạy trong thread riêng để không block Flask
        thread = threading.Thread(target=run_main)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            "message": f"Đã bắt đầu bombing số {phone} với {count} lần",
            "phone": phone,
            "count": count
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    global running_process
    
    if running_process is None:
        return jsonify({"status": "Chưa có process nào chạy"})
    
    if running_process.poll() is None:
        return jsonify({"status": "Đang chạy"})
    else:
        return jsonify({"status": "Đã hoàn thành"})

@app.route('/stop', methods=['POST'])
def stop_bombing():
    global running_process
    
    try:
        if running_process and running_process.poll() is None:
            running_process.terminate()
            return jsonify({"message": "Đã dừng process"})
        else:
            return jsonify({"message": "Không có process nào đang chạy"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
