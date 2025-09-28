from flask import Flask, request, send_file
import cv2, requests, numpy as np
import tempfile
# url = input("Enter the URL of the image: ")
app = Flask(__name__)

@app.route('/cartoonify', methods=['POST'])
def cartoonify():
    url = request.form.get('url')
    response = requests.get(url)
    if response.status_code != 200:
        return "Image not found", 404

    img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        return "Failed to decode image", 400

    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g = cv2.medianBlur(g, 5)
    e = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    c = cv2.bilateralFilter(img, 9, 250, 250)
    cartoon = cv2.bitwise_and(c, c, mask=e)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    cv2.imwrite(temp_file.name, cartoon)
    return send_file(temp_file.name, mimetype='image/jpeg')

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render assigns PORT dynamically
    app.run(host="0.0.0.0", port=port)


