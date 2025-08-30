from flask import Flask, request, jsonify
import subprocess, sys

app = Flask(__name__)
processes = {}

@app.route("/start", methods=["POST"])
def start():
    data = request.get_json()
    phone = data.get("phone")
    if not phone:
        return jsonify({"error": "Thiếu số điện thoại"}), 400

    # Chạy main.py nền
    proc = subprocess.Popen(
        [sys.executable, "main.py", phone],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    processes[phone] = proc
    return jsonify({"message": f"Đã bắt đầu chạy main.py với {phone}"})

@app.route("/status/<phone>", methods=["GET"])
def status(phone):
    proc = processes.get(phone)
    if not proc:
        return jsonify({"status": "Không tìm thấy process cho số này"})
    if proc.poll() is None:
        return jsonify({"status": "Đang chạy"})
    else:
        return jsonify({"status": "Đã hoàn thành"})

@app.route("/stop/<phone>", methods=["POST"])
def stop(phone):
    proc = processes.get(phone)
    if proc and proc.poll() is None:
        proc.terminate()
        return jsonify({"message": f"Đã dừng process của {phone}"})
    return jsonify({"message": "Không có process đang chạy cho số này"})
