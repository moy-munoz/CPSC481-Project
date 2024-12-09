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

    return rgb_values #, hex_colors

def kmeans_clustering(data):
    # K-Means Clustering
    kmeans = KMeans(n_clusters=6, random_state=42)
    kmeans.fit(data)

    # sorts the centers of the clusters by darkest to lightest
    sorted_centers = kmeans.cluster_centers_[np.argsort(np.sum(kmeans.cluster_centers_, axis=1))]

    # training a Random Forest Classifier
    dtc = tree.DecisionTreeClassifier()
    y = ["Type 6", "Type 5", "Type 4", "Type 3", "Type 2", "Type 1"]

    dtc.fit(sorted_centers, y) # Train using data and sorted labels from K-Means

    joblib.dump(dtc, "decision.joblib")

def main():
    csv_file = "clustered_skin.csv"
    data = load_data(csv_file)
    kmeans_clustering(data)

main()