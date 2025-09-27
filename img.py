import cv2
import requests
import numpy as np

url = "https://example.com/path/to/your/image.jpg"  # Replace with your image URL
response = requests.get(url)
if response.status_code != 200:
    print("Image not found")
    exit()
img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
if img is None:
    print("Failed to decode image")
    exit()

# Prep grayscale & blur
g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
g = cv2.medianBlur(g, 5)

# Edges
e = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                          cv2.THRESH_BINARY, 9, 9)

# Smooth color
c = cv2.bilateralFilter(img, 9, 250, 250)

# Combine
cartoon = cv2.bitwise_and(c, c, mask=e)

cv2.imshow("Cartoon", cartoon)
cv2.imwrite("cartoon_output.jpg", cartoon)
cv2.waitKey(0)
cv2.destroyAllWindows()