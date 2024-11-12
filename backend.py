import cv2
import numpy as np

def process_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Invalid image file. Please upload a valid image.")

    # Preprocess the image (e.g., extract skin regions)
    skin_region = extract_skin(image)

    # Detect skin tone
    tone = detect_skin_tone(skin_region)

    # Match undertone
    undertone = match_undertone(tone)

    return tone, undertone

def extract_skin(image):
    # Convert image to HSV for better color segmentation
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([0, 48, 80], dtype="uint8")
    upper_bound = np.array([20, 255, 255], dtype="uint8")
    skin_mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Apply mask to the image
    skin = cv2.bitwise_and(image, image, mask=skin_mask)
    return skin

def detect_skin_tone(image):
    # Convert to LAB color space for skin tone detection
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    mean_color = cv2.mean(lab)[:3]

    # Use heuristics to classify skin tone based on LAB color space
    if mean_color[0] < 128:
        return "Light"
    elif mean_color[0] < 200:
        return "Medium"
    else:
        return "Dark"

def match_undertone(tone):
    undertones = {
        "Light": "Cool",
        "Medium": "Neutral",
        "Dark": "Warm",
    }
    return undertones.get(tone, "Unknown")
