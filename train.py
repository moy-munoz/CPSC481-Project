import pandas as pd 
import numpy as np
from sklearn.cluster import KMeans 
from sklearn import tree 
import matplotlib.pyplot as plt 
import seaborn as sns 
import joblib

def load_data(csv_file):
    # Load CSV into a DataFrame
    df = pd.read_csv(csv_file)

    # Extract RGB values and Hex colors
    rgb_values = df[["R", "G", "B"]].values
    # hex_colors = df["hex_color"].tolist()

    return rgb_values #, hex_colors

def kmeans_clustering(data):
    # K-Means Clustering
    kmeans = KMeans(n_clusters=6, random_state=42)
    kmeans.fit(data)

    # Sort centers by brightness (sum of R, G, B)
    # sorted_indices = np.argsort(np.sum(kmeans.cluster_centers_, axis=1))
    sorted_centers = kmeans.cluster_centers_[np.argsort(np.sum(kmeans.cluster_centers_, axis=1))]

    # sorted_labels = np.zeros_like(kmeans.labels_)

    # for new_label, original_label in enumerate(sorted_indices):
    #     sorted_labels[kmeans.labels_ == original_label] = new_label

    print("Sorted Centers by Brightness:", sorted_centers)

    # Save sorted centers for K-Means predictions
    # joblib.dump(sorted_centers, "kmeans_sorted_centers.joblib")
    print("K-Means Sorted Centers saved to 'kmeans_sorted_centers.joblib'.")

    # Step 2: Train Random Forest Classifier
    dtc = tree.DecisionTreeClassifier()
    # X_train = da
    y = ["Type 6", "Type 5", "Type 4", "Type 3", "Type 2", "Type 1"]

    # print("data\n", sorted_centers)
    dtc.fit(sorted_centers, y)#, sorted_labels)  # Train using data and sorted labels from K-Means

    joblib.dump(dtc, "decision.joblib")






# def plot_clusters(data, labels, centers, hex_colors):
#     fitzpatrick_labels  = ["Type VI",  "Type V", "Type IV", "Type III", "Type II","Type I"]

#     plt.figure(figsize=(10, 7))

#     # Plot each point with its corresponding hex color
#     for i, rgb in enumerate(data):
#         plt.scatter(rgb[0], rgb[1], color=hex_colors[i], alpha=0.8)

#     # Highlight cluster centers  and annotate them with Fitzpatrick labels
#     for i, center in enumerate(centers):
#         plt.scatter(center[0], center[1], color="black", marker="x", s=100)  # Plot centroid
#         plt.text(center[0] + 5, center[1] + 5, fitzpatrick_labels[i], fontsize=12, color="black")  # Label the centroid

#     plt.title("Skin Tone Clusters with Fitzpatrick Labels")
#     plt.xlabel("Red Channel")
#     plt.ylabel("Green Channel")
#     plt.grid(True)
#     plt.legend()
#     # plt.show()


# take out
# def save_model(model, filename):
#     # joblib.dump(model, filename)
#     # print(f"Model saved to {filename}")

#     print(f"Model type: {type(model)}")
#     joblib.dump(model, "skin_analysis_model.joblib")

# def load_model(filename):
#     model = joblib.load(filename)
#     print(f"model loaded from {filename}")
#     return model

# data, other = load_data("clustered_skin.csv")
# kmeans_clustering(data)


# print(centers)

# df = pd.read_csv("clustered_skin.csv")
# print(df.loc[ 0:240, "R":"B"])
# sns.histplot(df)

# (n = 6)

# print(df.head())
# print(df.tail())