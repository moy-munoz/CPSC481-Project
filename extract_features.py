import cv2 
import numpy as np
import os


def read_files():
    path = "/home/jasmine/Desktop/skin_types"

    skin_median = []

    # reading files from a specific folder path 
    for file in os.listdir(path):
        image_path = os.path.join(path, file)
        image = cv2.imread(image_path)

        # the list skin_median, appends the median of the skin from the images  
        # calls the function extract_features
        skin_median.append(extract_features(image))

    # creates a csv file based on the skin_median 
    # calls the function format_csv
    format_csv(skin_median)


def extract_features(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # creates the lower and upper bound of the skin colors 
    # lower being a dark skin color and upper being a light skin color
    lower_bound = np.array([0, 48, 80], dtype="uint8")
    upper_bound = np.array([20, 255, 255], dtype="uint8")
    # creates a skin mask to extract the areas with the skin colors of the image
    skin_mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    # convert BGR to RGB 
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # flatten the image 
    # creates separate RGB values and isolates the skin region by using skin_mask > 0
    skin_region_R = rgb_image[:, :, 0][skin_mask > 0]
    skin_region_G = rgb_image[:, :, 1][skin_mask > 0]
    skin_region_B = rgb_image[:, :, 2][skin_mask > 0]
    
    # get the median and convert to an integer
    skin_median_R = int(np.median(skin_region_R))
    skin_median_G = int(np.median(skin_region_G))
    skin_median_B = int(np.median(skin_region_B))

    # store the median in a tuple
    rgb_list = [skin_median_R, skin_median_G, skin_median_B]
    # creates the hexadecimal for the RGB values
    # hex_color = "#{0:02x}{1:02x}{2:02x}".format(skin_median_R, skin_median_G, skin_median_B)

    # returns a map: rgb_tuple is the key and hex_color is the value
    # return {rgb_tuple: hex_color}
    return rgb_list



def format_csv(extract_features_list):
    file_path = "clustered_skin.csv"
    # opens and writes to a csv file
    with open(file_path, mode='w', newline='') as f:
        # write header based on the rgb tuple and the hex_color
        f.write("R,G,B\n")

        # accesses the list of maps 
        for i in extract_features_list:
            # gathers the items from the map and writes them to the csv file
            f.write(f"{i[0]},{i[1]},{i[2]}\n") 

    print("CSV created")


read_files()

cv2.waitKey(0)