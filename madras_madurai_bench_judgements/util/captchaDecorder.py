import requests

def google_ocr(base64_image):
    
    api_key = "AIzaSyDCNRpug2TxiTP407h3frQH0GUH3LkFVoE"

    # Remove the "data:image/jpeg;base64," prefix if present
    if base64_image.startswith("data:image"):
        base64_image = base64_image.split(",")[1]

    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    payload = {
        "requests": [
            {
                "image": {"content": base64_image},
                "features": [{"type": "TEXT_DETECTION"}],
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    
    # Check for errors in the response
    if "error" in result:
        print("Error in API response:", result["error"]["message"])
        return ""
    
    try:
        if "responses" in result and "textAnnotations" in result["responses"][0]:
            return result["responses"][0]["textAnnotations"][0]["description"]
        else:
            print("No text detected in the image.")
            return ""
    except (KeyError, IndexError) as e:
        print("Unexpected response format:", result)
        return "" 
