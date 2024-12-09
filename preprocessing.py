import cv2 as cv
import os

def preprocesed_image(image, image_path):

    # ensure haar cascade is loaded
    haar_cascade = cv.CascadeClassifier('haar_face.xml')
    if haar_cascade.empty():
        raise ValueError("Error: Could not load Haar Cascade XML file.")

    # if the image is greater than 256, then an attempt is taken to detect and crop the face
    if image.shape[0] > 256 or image.shape[1] > 256:
        # Detect face
        face_rect = haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=4)

        # checks if a face was detected
        if len(face_rect) > 0:
            # crops the first detected face
            crop = image[face_rect[0][1]:(face_rect[0][1]+face_rect[0][3]), face_rect[0][0]:(face_rect[0][0]+face_rect[0][2])]

            image = crop
        else:
            print("Warning: No face detected. Resizing directly at:", image_path)

    # resizes the image to 256x256
    new_size = cv.resize(image, (256, 256))

    return new_size

def preprocess_and_save_images():
    # path for personal image location 
    path = "/home/jasmine/Desktop/skin_types"

    for file in os.listdir(path):
        # reads the image as a file
        image = cv.imread(os.path.join(path, file))
        # skips the image that could not be read properly
        if image is None:
            continue    
        # the function (preprocesed_image) gets called 
        image = preprocesed_image(image, os.path.join(path, file))
        # initializes the new folder path
        output_path = os.path.join(path, "output_dir_")
        # if the folder(output_dir_) does not exist, then it gets created
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        # writes the image to a new folder path
        cv.imwrite(os.path.join(output_path, file), image)

# preprocess_and_save_images()

cv.waitKey(0)