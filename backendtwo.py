import cv2
import numpy as np

def process_image(image_path):
    """
    Process the uploaded image to detect skin tone and match it with an undertone.

    Args:
        image_path (str): Path to the input image.

    Returns:
        tuple: Skin tone and undertone detected.
    """
    try:
        # Load the image
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError("Invalid image file. Please upload a valid image.")

        # Extract skin regions
        skin_region = extract_skin(image)

        # Detect skin tone
        tone = detect_skin_tone(skin_region)

        # Match undertone
        undertone = match_undertone(tone)

        return tone, undertone

    except Exception as e:
        raise RuntimeError(f"Error processing image: {e}")


def extract_skin(image):
    """
    Extract skin regions from the input image using color-based segmentation.

    Args:
        image (numpy.ndarray): Input image.

    Returns:
        numpy.ndarray: Image with skin regions extracted.
    """
    # Convert image to HSV for better color segmentation
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([0, 48, 80], dtype="uint8")
    upper_bound = np.array([20, 255, 255], dtype="uint8")

    # Create a skin mask
    skin_mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Apply mask to the original image
    skin = cv2.bitwise_and(image, image, mask=skin_mask)

    return skin


def detect_skin_tone(image):
    """
    Detect the skin tone from the processed image.

    Args:
        image (numpy.ndarray): Processed image containing skin regions.

    Returns:
        str: Detected skin tone (e.g., 'Light', 'Medium', 'Dark').
    """
    # Convert to LAB color space for better tone detection
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    mean_color = cv2.mean(lab)[:3]  # Get the mean color in LAB space

    # Classify skin tone based on the lightness component (L)
    if mean_color[0] < 128:
        return "Light"
    elif mean_color[0] < 200:
        return "Medium"
    else:
        return "Dark"


def match_undertone(tone):
    """
    Match the detected skin tone with an undertone.

    Args:
        tone (str): Detected skin tone.

    Returns:
        str: Matched undertone (e.g., 'Cool', 'Neutral', 'Warm').
    """
    undertones = {
        "Light": "Cool",
        "Medium": "Neutral",
        "Dark": "Warm",
    }

    return undertones.get(tone, "Unknown")


def save_results(image_path, output_path, skin_tone, undertone):
    """
    Save the results of the detection process.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        skin_tone (str): Detected skin tone.
        undertone (str): Matched undertone.
    """
    # Load the original image
    image = cv2.imread(image_path)

    # Overlay text for skin tone and undertone
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f"Tone: {skin_tone}, Undertone: {undertone}"
    cv2.putText(image, text, (10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Save the result
    cv2.imwrite(output_path, image)


if __name__ == "__main__":
    # Example usage
    input_image = "example.jpg"  # Replace with the path to your input image
    output_image = "result.jpg"  # Replace with the path to save the output image

    try:
        tone, undertone = process_image(input_image)
        print(f"Detected Skin Tone: {tone}")
        print(f"Matched Undertone: {undertone}")

        # Save the output image with results
        save_results(input_image, output_image, tone, undertone)
        print(f"Results saved to {output_image}")

    except RuntimeError as e:
        print(e)
