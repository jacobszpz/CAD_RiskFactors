import numpy as np
import matplotlib.pyplot as plt

def plot_top_features(features: list[str], coefficients: list[float], top_n: int = 20) -> None:
    """
    Plot the top N most important features (positive and negative) in a vertical bar chart.

    :param features: List of feature names
    :param coefficients: List of coefficients corresponding to the features
    :param top_n: Number of top features to visualize, default is 20
    """
    # Sort the features based on their coefficients
    sorted_indices = np.argsort(coefficients)

    # Select the top N positive and negative features
    top_positive_features = features[sorted_indices[-top_n:]]
    top_negative_features = features[sorted_indices[:top_n]]

    # Combine positive and negative features and coefficients
    top_features = np.hstack([top_negative_features, top_positive_features])
    top_coefficients = np.hstack([coefficients[sorted_indices[:top_n]], coefficients[sorted_indices[-top_n:]]])

    # Assign colors to the features
    colors = ['red' if coef < 0 else 'blue' for coef in top_coefficients]

    # Visualize the top features in a vertical bar chart
    plt.figure(figsize=(10, 10))
    plt.bar(range(2 * top_n), top_coefficients, color=colors)
    plt.xticks(range(2 * top_n), top_features, rotation=90)
    plt.ylabel('Coefficient')
    plt.title('Top {} Most Important Positive and Negative Features'.format(top_n))
    plt.show()

