import training_model as model

import matplotlib.pyplot as plt
import numpy as np

import warnings


def display_graph(plt):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")  # Capture tous les warnings

        plt.show()

        for warning in w:
            if issubclass(warning.category, UserWarning):
                print(f"Could not display the graph : {warning.message}")
                print("Saving the graph as 'regression.png'")
                plt.savefig("regression.png")

def show_base_graph(x_original, y, theta0, theta1, x_min, x_max):
    plt.grid(True)
    plt.scatter(x_original, y, color='blue', label='Data point', s=10)

    x_line = np.linspace(min(x_original), max(x_original), 100)
    x_norm_line = [(x - x_min) / (x_max - x_min) for x in x_line]
    y_line = [model.estimate_price(theta0, theta1, x_norm) for x_norm in x_norm_line]
    plt.plot(x_line, y_line, color='red', label='Linear Regression')

    y_max = max(y)
    x_max_km = max(x_original)
    y_min = min(y)
    euro_per_km = (y_max - y_min) / (x_max_km - min(x_original))
    ideal_line = [y_max - euro_per_km * x for x in x_line]
    plt.plot(x_line, ideal_line, color='green', linestyle='--', label='Km/€')

    plt.xlabel('Mileage (km)')
    plt.ylabel('Price (€)')
    plt.title('Linear Regression')
    plt.legend()

    display_graph(plt)