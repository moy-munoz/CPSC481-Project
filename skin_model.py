    # def analyze_colors(self, file_path):
    #     # Load image
    #     image = cv2.imread(file_path)
    #     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #     reshaped = image.reshape((-1, 3))

    #     # Perform KMeans clustering
    #     n_colors = 5
    #     kmeans = KMeans(n_clusters=n_colors, random_state=0)
    #     kmeans.fit(reshaped)

    #     # Convert centers to int and format as hex
    #     colors = kmeans.cluster_centers_.astype(int)
    #     hex_colors = ["#{:02x}{:02x}{:02x}".format(c[0], c[1], c[2]) for c in colors]
    #     return hex_colors