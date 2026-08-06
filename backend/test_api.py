import requests
import json

url = "http://127.0.0.1:8000/api/convert"
data = {
    "text": "내일까지 보고서 제출 어려울 것 같음",
    "target_audience": "boss"
}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    with open("backend/test_result.json", "w", encoding="utf-8") as f:
        json.dump(response.json(), f, indent=2, ensure_ascii=False)
    print("Result saved to backend/test_result.json")
except Exception as e:
    print(f"Error occurred: {str(e)}")
