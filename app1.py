from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
from backend import redact_image   # from your earlier backend.py
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    # Save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Read image
    image = cv2.imread(filepath)

    # Run AI redaction
    redacted = redact_image(image)

    # Save redacted image
    output_path = os.path.join(OUTPUT_FOLDER, "redacted_" + file.filename)
    cv2.imwrite(output_path, redacted)

    return render_template("result.html",
                           original=file.filename,
                           redacted="redacted_" + file.filename)

from flask import send_from_directory

# Serve uploaded files
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Serve output (redacted) files
@app.route("/outputs/<filename>")
def output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

# Download redacted file
@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(path, as_attachment=True)
    
if __name__ == "__main__":
    app.run(debug=True)
