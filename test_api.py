import requests
import json

def test_api(image_path):
    url = "http://localhost:8000/get-lab-tests"
    
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
    
    print("Status Code:", response.status_code)
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_api(r"test_images\AHD-0425-PA-0008061_E-mahendrasinghdischargecard_250427_1114@E.pdf_page_27.png")  # Replace with your test image
