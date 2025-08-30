
from flask import Flask, request, jsonify
import subprocess
import threading
import sys
import os
from flask import Flask, request, jsonify
import subprocess
import sys

app = Flask(__name__)

@app.route("/start", methods=["POST"])
def start():
    try:
        data = request.get_json()
        phone = data.get("phone")

        if not phone:
            return jsonify({"error": "Thiếu số điện thoại"}), 400

        # Gọi main.py với tham số phone
        result = subprocess.run(
            [sys.executable, "main.py", phone],
            capture_output=True,
            text=True
        )

        return jsonify({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
