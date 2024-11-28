# Feature extraction functions

# def extract_features(image):
#     lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
#     mean_l = np.mean(lab[:, :, 0])
#     mean_a = np.mean(lab[:, :, 1])
#     mean_b = np.mean(lab[:, :, 2])

#     # Calculate saturation
#     saturation = np.sqrt((mean_a - 128)**2 + (mean_b - 128)**2)
#     return {"Brightness": mean_l, "Saturation": saturation}
