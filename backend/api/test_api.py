import requests

url = "http://127.0.0.1:5000/api/summary"

try:
    response = requests.get(url)
    if response.status_code == 200:
        print("✅ API Response Received:")
        print(response.json())
    else:
        print(f"❌ Failed with status code {response.status_code}")
        print("Details:", response.text)
except Exception as e:
    print("❌ Error occurred:", str(e))
