import graph
import precision_calculator

import csv
import argparse
from time import sleep
import json
import math

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--loadfile", help="Data File name", default="data.csv")
    parser.add_argument("--savefile", help="Data File name", default="thetas.json")
    parser.add_argument("-i", "--iteration", help="Number of iteration", default=1000, type=int)
    parser.add_argument("-l", "--learnrate", help="learning rate", default=0.1, type=float)
    parser.add_argument("-d", "--display", help="Display graph", action="store_true")
    parser.add_argument("-p", "--precision", help="Calculate precision", action="store_true")
    parser.add_argument("-v", "--verbose", help="Verbose mode", action="store_true")

    return parser.parse_args()

def check_arguments(args):
    if (args.learnrate < 0.01 or args.learnrate > 1.1):
        if args.learnrate <= 0:
            print("ERROR: Learning rate value should not be less than or equal to 0.")
            exit(1)
        print("Warning: Learning rate value is not optimal and might lead to poor results. Should be between 0.01 and 1.1.")
    if (args.iteration < 500 or args.iteration > 5000):
        if args.iteration <= 0:
            print("ERROR: Iteration value should not be less than or equal to 0.")
            exit(1)
        print("Warning: Iteration value is not optimal and might lead to poor results or slow calculations. Should be between 500 and 5000.")
    if args.loadfile.endswith('.csv') == False:
        print("ERROR: The load file must be a CSV file.")
        exit(1)
    if args.savefile.endswith('.json') == False:
        print("ERROR: The save file must be a JSON file.")
        exit(1)

# Normalize the data to a range of 0 to 1
# This is important to prevent large values from skewing the results
def normalize(data):
    x_min = min(data)
    x_max = max(data)
    normalized = [(x - x_min) / (x_max - x_min) for x in data]
    return normalized, x_min, x_max

def read_data(args):
    price = []
    mileage = []
    try:
        with open(args.loadfile, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            if args.verbose:
                print(f"[     Km] [ Price]")
            for row in reader:
                mileage.append(float(row['km']))
                price.append(float(row['price']))
                if args.verbose:
                    print(f"[{row['km']:>7}] [{row['price']:>6}]")
        if not mileage or not price:
            print("Error: The CSV file is empty or does not contain valid data.")
            exit(1)
        if len(mileage) != len(price):
            print("Error: The CSV file must have the same number of 'km' and 'price' entries.")
            exit(1)
        return mileage, price
    except FileNotFoundError:
        print(f"Error ! '{args.loadfile}' does not exist.")
        exit(1)
    except KeyError:
        print("The csv file must contain 'km' and 'price' columns.")
        exit(1)

def estimate_price(theta0, theta1, x):
    return theta0 + theta1 * x

def train_model(args, mileage, price):
    learning_rate = args.learnrate
    iterations = args.iteration
    theta0 = 0.0
    theta1 = 0.0
    m = len(mileage)
    
    print(f"Training model with {m} data points...")
    for x in range(iterations):
        sum_errors_theta0 = 0
        sum_errors_theta1 = 0
        for i in range(m):
            error = estimate_price(theta0, theta1, mileage[i]) - price[i]
            sum_errors_theta0 += error
            sum_errors_theta1 += error * mileage[i]
        
        tmp_theta0 = theta0 - learning_rate * (sum_errors_theta0 / m)
        tmp_theta1 = theta1 - learning_rate * (sum_errors_theta1 / m)

        if args.verbose:
            sleep(0.01)  # Simulate some processing time
            print(f"Iteration {x}/{iterations}: theta0 = {tmp_theta0}, theta1 = {tmp_theta1}", end='\r')
            if x % 100 == 0:
                print("")

        # Simultaneous update
        theta0 = tmp_theta0
        theta1 = tmp_theta1


        if not args.verbose:
            load_bar = "[" + "=" * ((x + 1) * 50 // iterations) + " " * (50 - (x + 1) * 50 // iterations) + "]"
            print(load_bar, x + 1, "/", iterations, end='\r')

    print("\nTraining completed.")
    return theta0, theta1

def save_model(theta0, theta1, x_min, x_max, filename):
    with open(filename, 'w') as f:
        json.dump({
            'theta0': theta0,
            'theta1': theta1,
            'x_min': x_min,
            'x_max': x_max
        }, f)


# {"theta0": 0, "theta1": 0, "x_min": 0, "x_max": 1}
# default values for thetas and normalization

if __name__ == "__main__":
    
    args = parse_arguments()
    check_arguments(args)

    mileage, price = read_data(args)
    normalized_mileage, x_min, x_max = normalize(mileage)

    theta0, theta1 = train_model(args, normalized_mileage, price)

    if args.verbose:
        print(f"\nTheta0: {theta0}\nTheta1: {theta1}")

    save_model(theta0, theta1, x_min, x_max, args.savefile)


    if args.precision:
        predictions = [estimate_price(theta0, theta1, x) for x in normalized_mileage]
        precision_calculator.give_score(price, predictions)

    if not args.display:
        graph.show_base_graph(mileage, price, theta0, theta1, x_min, x_max)