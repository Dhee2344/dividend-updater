import requests
import json
import os

# ✅ API
url = "https://www.nseindia.com/api/corporates-corporateActions?index=equities"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com/"
}

session = requests.Session()
session.get("https://www.nseindia.com", headers=headers)

response = session.get(url, headers=headers)
print("Status Code:", response.status_code)

result = []

# ✅ Load old data
if os.path.exists("full_dividends.json"):
    try:
        with open("full_dividends.json", "r") as f:
            result.extend(json.load(f))
    except:
        print("Old data load error")

# ✅ Parse new data
try:
    data = response.json()

    for item in data:
        if item.get("faceVal") and item.get("exDate"):
            result.append({
                "company": item.get("comp"),
                "ex_date": item.get("exDate"),
                "dividend": str(item.get("faceVal")) + " Rs"
            })

except Exception as e:
    print("JSON error:", e)

# ✅ Remove duplicates
clean = []
seen = set()

for item in result:
    key = (item["company"], item["ex_date"])
    if key not in seen:
        seen.add(key)
        clean.append(item)

result = clean

# ✅ Save file
filename = "full_dividends.json"

with open(filename, "w") as f:
    json.dump(result, f, indent=4)

print("✅ Data saved:", len(result))

# ✅ HTTP UPLOAD (FINAL FIX)
try:
    print("🚀 Uploading via HTTP...")

    upload_url = "https://dswealthadvisors.in/upload.php"

    files = {"file": open(filename, "rb")}
    response = requests.post(upload_url, files=files)

    print("✅ Server response:", response.text)

except Exception as e:
    print("❌ Upload failed:", e)