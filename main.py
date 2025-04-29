from fastapi import FastAPI, File, UploadFile, status
from fastapi.responses import JSONResponse
from PIL import Image, ImageOps, ImageFilter
import pytesseract
import re
import os
import uuid

app = FastAPI()

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path: str):
    img = Image.open(image_path)
    img = ImageOps.grayscale(img)
    img = img.resize((img.width*3, img.height*3), Image.LANCZOS)
    img = img.filter(ImageFilter.SHARPEN)
    img = img.point(lambda x: 0 if x < 200 else 255)  # Thresholding
    return img

def parse_lab_data(text: str):
    patterns = [
        re.compile(r'(?P<test>.+?)\s+(?P<value>\d+\.?\d*)\s*(?P<unit>[a-zA-Z%]+)?\s*[\[\(]\s*(?P<low>\d+\.?\d*)\s*-\s*(?P<high>\d+\.?\d*)\s*[\]\)]'),
        re.compile(r'(?P<test>.+?)\s*\|\s*(?P<value>\d+\.?\d*)\s*\|\s*(?P<low>\d+\.?\d*)\s*-\s*(?P<high>\d+\.?\d*)\s*\|\s*(?P<unit>[a-zA-Z%]+)'),
        re.compile(r'(?P<test>.+?)\t(?P<value>\d+\.?\d*)\t(?P<low>\d+\.?\d*)\s*-\s*(?P<high>\d+\.?\d*)\s*(?P<unit>[a-zA-Z%]+)?')
    ]
    
    results = []
    for line in text.split('\n'):
        line = line.strip()
        for pattern in patterns:
            match = pattern.search(line)
            if match:
                try:
                    data = match.groupdict()
                    results.append({
                        "lab_test_name": data['test'].strip(),
                        "lab_test_value": float(data['value']),
                        "lab_test_unit": data.get('unit', ''),
                        "bio_reference_range": [float(data['low']), float(data['high'])],
                        "lab_test_out_of_range": None  # Will be calculated later
                    })
                    break
                except (ValueError, KeyError):
                    continue
    return results

@app.post("/get-lab-tests")
async def process_report(file: UploadFile = File(...)):
    response = {
        "is_success": True,
        "lab_tests": []
    }
    
    temp_path = f"temp_{uuid.uuid4()}.png"
    
    try:
        # Save uploaded file
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        
        # OCR Processing
        img = preprocess_image(temp_path)
        text = pytesseract.image_to_string(img)
        
        # Data extraction
        tests = parse_lab_data(text)
        
        # Calculate out-of-range status
        for test in tests:
            low, high = test['bio_reference_range']
            test_value = test['lab_test_value']
            test['lab_test_out_of_range'] = not (low <= test_value <= high)
        
        response["lab_tests"] = tests

    except Exception as e:
        response["is_success"] = False
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response
        )
        
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
