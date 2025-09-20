# AI-based PII Redaction Tool

This project is a **Flask web application** that automatically redacts sensitive information (PII) such as names, dates, and signatures from uploaded images using AI and OpenCV.  

---

## 🚀 Features
- Upload images containing sensitive data  
- Automatically detect and redact PII using AI models  
- Preview original and redacted images on the webpage  
- Download the redacted image for secure use  
- Extendable for additional PII detection (faces, ID numbers, etc.)  

---

## 🛠️ Tech Stack
- **Python 3**  
- **Flask** – Backend web framework  
- **OpenCV** – Image processing  
- **EasyOCR / Tesseract** – Text detection  
- **HTML, CSS (Jinja templates)** – Frontend  

---


## ⚙️ Installation
1. Clone the repository:
```bash
git clone https://github.com/your-username/pii-redaction-tool.git
cd pii-redaction-tool
```
2.Create and activate a virtual environment:
  ```bash
  python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
 ```
3.Install dependencies:
  ```bash
  pip install -r requirements.txt
```
4.▶️ Running the App

Start the Flask server:
```bash
python app1.py
```
Then open your browser and go to:
👉 http://127.0.0.1:5000/

---

## 📘 Usage

Go to the home page.

Upload an image with sensitive data.

The system redacts PII and shows:

Original image

Redacted image

Option to download the redacted file.\

---


## 🧩 Example

Input: An image with names & signatures

Output: Same image but with those parts blacked out

---

## 📌 Future Enhancements


Cloud deployment (AWS/GCP/Heroku)

Add encryption for uploads





