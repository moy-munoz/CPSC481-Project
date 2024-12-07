import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QListWidget,
    QListWidgetItem
)
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from sklearn.cluster import KMeans
from extract_features import extract_features
import joblib
from sklearn import datasets

class ColorAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Skin Color Analysis App")
        self.setGeometry(100, 100, 800, 600)
        self.model = joblib.load("/home/jasmine/Desktop/AI_Project_Skin/skin_analysis_model.joblib")
        print(f"Model type: {type(self.model)}")
        self.init_ui()

    def init_ui(self):
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Upload button
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)

        # Image preview label
        self.image_label = QLabel("Your image will appear here")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Results section
        results_layout = QVBoxLayout()
        results_layout.addWidget(QLabel("Detected Colors:"))
        self.colors_list = QListWidget()
        results_layout.addWidget(self.colors_list)
        layout.addLayout(results_layout)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.display_image(file_path)
            colors = self.process_image(file_path)
            self.display_colors(colors)
        else:
            self.colors_list.clear()
            self.colors_list.addItem("No image selected.")

    def display_image(self, file_path):
        pixmap = QPixmap(file_path).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)

    def process_image(self, file_path):
        image = cv2.imread(file_path)
        skin_map = extract_features(image)
        if skin_map:
            detected_colors = []
            for rgb_tuple, hex_color in skin_map.items():
                print(f"Detected RGB: {rgb_tuple}, Hex: {hex_color}")

                # Make a prediction using the loaded model
                print("type:", type([[rgb_tuple[0], rgb_tuple[1], rgb_tuple[2]]]))

                # prediction = self.model.predict(int(rgb_tuple[0]))#, rgb_tuple[1], rgb_tuple[2]]])[0]  # Predict cluster label
                # print(f"Prediction: {prediction}")
                input_data = [[rgb_tuple[0], rgb_tuple[1], rgb_tuple[2]]]
                prediction = self.model.predict(input_data)[0]
                # Append the hex color, RGB tuple, and prediction label to the results
                detected_colors.append({"hex_color": hex_color, "rgb_tuple": rgb_tuple, "prediction": prediction})
            return detected_colors
        else:
            return ["No skin detected in the image."]
        print(skin_map)
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

    def display_colors(self, colors):
        self.colors_list.clear()  # Clear previous results
        if not predictions or not isinstance(predictions, list):
            self.colors_list.addItem("No colors detected or invalid input.")
            return

        if len(predictions) == 1 and "No skin detected" in predictions[0]:
            self.colors_list.addItem(predictions[0])
            return

        hex_color = predictions[0]
        label = predictions[1]  # Prediction label from the model

        try:
            # Create a QListWidgetItem and set its background color
            item = QListWidgetItem(f"{label} ({hex_color})")  # Combine label and color
            item.setBackground(QColor(hex_color))  # Set the background to the color
            # Set text color to be readable (white on dark colors, black on light colors)
            item.setForeground(Qt.white if QColor(hex_color).lightness() < 128 else Qt.black)
            self.colors_list.addItem(item)  # Add the item to the list widget
        except Exception as e:
            self.colors_list.addItem(f"Error displaying color: {str(e)}")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ColorAnalysisApp()
    main_window.show()
    sys.exit(app.exec_())