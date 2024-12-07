import pandas as pd 
import numpy as np
from sklearn.cluster import KMeans 
import matplotlib.pyplot as plt 
import seaborn as sns 
import joblib

def load_data(csv_file):
    # Load CSV into a DataFrame
    df = pd.read_csv(csv_file)

    # Extract RGB values and Hex colors
    rgb_values = df[["R", "G", "B"]].values
    hex_colors = df["hex_color"].tolist()

    return rgb_values, hex_colors

def kmeans_clustering(data, k):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data)

    # Save the trained model
    # Sort centers by brightness (sum of R, G, B)
    sorted_indices = np.argsort(np.sum(kmeans.cluster_centers_, axis=1))
    sorted_centers = kmeans.cluster_centers_[sorted_indices]
    sorted_labels = np.zeros_like(kmeans.labels_)
    for new_label, original_label in enumerate(sorted_indices):
        sorted_labels[kmeans.labels_ == original_label] = new_label
        
    print("These are the centers", sorted_centers)
    joblib.dump(sorted_centers, "skin_analysis_model.joblib")
    print("Model saved to 'skin_analysis_model.joblib'.")
    return sorted_labels, sorted_centers

def plot_clusters(data, labels, centers, hex_colors):
    fitzpatrick_labels  = ["Type VI",  "Type V", "Type IV", "Type III", "Type II","Type I"]

    plt.figure(figsize=(10, 7))

    # Plot each point with its corresponding hex color
    for i, rgb in enumerate(data):
        plt.scatter(rgb[0], rgb[1], color=hex_colors[i], alpha=0.8)

    # Highlight cluster centers  and annotate them with Fitzpatrick labels
    for i, center in enumerate(centers):
        plt.scatter(center[0], center[1], color="black", marker="x", s=100)  # Plot centroid
        plt.text(center[0] + 5, center[1] + 5, fitzpatrick_labels[i], fontsize=12, color="black")  # Label the centroid

    plt.title("Skin Tone Clusters with Fitzpatrick Labels")
    plt.xlabel("Red Channel")
    plt.ylabel("Green Channel")
    plt.grid(True)
    plt.legend()
    # plt.show()

def save_model(model, filename):
    # joblib.dump(model, filename)
    # print(f"Model saved to {filename}")

    print(f"Model type: {type(model)}")
    joblib.dump(model, "skin_analysis_model.joblib")

def load_model(filename):
    model = joblib.load(filename)
    print(f"model loaded from {filename}")
    return model

data, other = load_data("clustered_skin.csv")
k = 6
kmeans_clustering(data, k)


# print(centers)

# df = pd.read_csv("clustered_skin.csv")
# print(df.loc[ 0:240, "R":"B"])
# sns.histplot(df)

# (n = 6)

# print(df.head())
# print(df.tail())