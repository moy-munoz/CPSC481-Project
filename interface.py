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
from preprocessing import preprocesed_image

class ColorAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Skin Color Analysis App")
        self.setGeometry(100, 100, 800, 600)
        self.model = joblib.load("/home/jasmine/Desktop/AI_Project_Skin/CPSC481-Project/decision.joblib")
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
        resized_image = preprocesed_image(image, file_path)

        skin_map = extract_features(resized_image)
        
        if skin_map:
            rgb_tuple = skin_map
            detected_colors = []

            input_data = [list(rgb_tuple)]

            prediction = self.model.predict(input_data)[0]

            # Store the results
            detected_colors.append({
                "rgb_tuple": rgb_tuple,
                "prediction": prediction
            })
            return detected_colors

    def display_colors(self, colors):
        self.colors_list.clear()  # Clear previous results

        if isinstance(colors, list) and "No skin detected" in colors[0]:
            self.colors_list.addItem(colors[0])
            return

        try:
            # Extract details
            rgb_tuple = colors[0]["rgb_tuple"]
            prediction = colors[0]["prediction"]
            hex_color = "#{:02x}{:02x}{:02x}".format(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])

            # Create a list item with the prediction and color
            list_item = QListWidgetItem(f"Your skin type is: {prediction}\nYour skin color in hexadecimal is: {hex_color}")
            list_item.setBackground(QColor(hex_color))
            list_item.setForeground(Qt.white if QColor(hex_color).lightness() < 128 else Qt.black)
            self.colors_list.addItem(list_item)

        except Exception as e:
            self.colors_list.addItem(f"Error displaying color: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ColorAnalysisApp()
    main_window.show()
    sys.exit(app.exec_())