from flask import Flask, request, send_file, render_template
import cv2, requests, numpy as np
import tempfile, os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Cartoonify API is running! Use POST /cartoonify with an image URL or visit /input to try it."

@app.route("/input")
def input_page():
    return render_template("index.html")

@app.route("/cartoonify", methods=["POST"])
def cartoonify():
    url = request.form.get("url")
    if not url:
        return "Missing image URL", 400

    try:
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

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        cv2.imwrite(temp_file.name, cartoon)
        return_data = send_file(temp_file.name, mimetype="image/jpeg")
        os.unlink(temp_file.name)
        return return_data

    except Exception as e:
        return f"Error processing image: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
