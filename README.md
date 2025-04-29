
# Lab Report Extraction API

This project provides a scalable and accurate solution to process lab report images and extract all lab test names, their corresponding values, and reference ranges. The logic is implemented in Python and deployed as a FastAPI service.

## Problem Statement

Given a dataset of lab report images, develop a Python-based FastAPI service that exposes a POST endpoint `/get-lab-tests`. This endpoint accepts an image file and returns the extracted lab test data in a structured JSON format.

**Strictly no LLMs (Large Language Models) are used.**  
All extraction logic is custom and based on traditional OCR and parsing techniques.

---

## Features

- Accepts lab report images (PNG, JPG, JPEG) via API
- Extracts:
  - Lab test name
  - Test value
  - Reference range (as a string)
  - Unit
  - Boolean flag indicating if the value is out of range
- Returns results in the exact format required by the competition

---

## API Usage

### **Endpoint**

```
POST /get-lab-tests
```

### **Request**

- Content-Type: `multipart/form-data`
- Field: `file` (the lab report image)

### **Response Format**

```json
{
  "is_success": true,
  "data": [
    {
      "test_name": "HB ESTIMATION",
      "test_value": "9.4",
      "bio_reference_range": "12.0-15.0",
      "test_unit": "g/dL",
      "lab_test_out_of_range": false
    },
    {
      "test_name": "PCV (PACKED CELL VOLUME)",
      "test_value": "48.7",
      "bio_reference_range": "36.0-46.0",
      "test_unit": "%",
      "lab_test_out_of_range": true
    }
  ]
}
```

- `is_success`: Boolean, true if extraction succeeded.
- `data`: List of extracted lab tests, each with:
  - `test_name`: Name of the test (string)
  - `test_value`: Value as string
  - `bio_reference_range`: Reference range as string `"low-high"`
  - `test_unit`: Unit as string
  - `lab_test_out_of_range`: Boolean, true if value is outside the reference range

---

## Setup & Running Locally

1. **Clone this repository and enter the project directory:**
   ```bash
   git clone 
   cd 
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR:**
   - **Windows:** Download from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) and note the install path.
   - **macOS:** `brew install tesseract`
   - **Linux:** `sudo apt-get install tesseract-ocr`

4. **(Windows only) Set the Tesseract path in `main.py`:**
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

5. **Run the API server:**
   ```bash
   uvicorn main:app --reload
   ```

6. **Test the API:**
   - Go to `http://localhost:8000/docs` for Swagger UI and upload an image.
   - Or use a script:
     ```python
     import requests
     url = "http://localhost:8000/get-lab-tests"
     files = {"file": open("path/to/lab_report.png", "rb")}
     response = requests.post(url, files=files)
     print(response.json())
     ```

---

## Dataset

Download the dataset from the [provided Google Drive link](https://drive.google.com/file/d/1LzG7oJ-cqGHK9KbwXnWfkWgnQ3xi8Cr9/view?usp=sharing) and use the images for testing.

---
