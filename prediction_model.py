import json
import string
import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--filename", help="Data File name", default="thetas.json")
    parser.add_argument("-l", "--loop", help="Loop the program", action="store_true")

    return parser.parse_args()

def check_arguments(args):
    if args.filename.endswith('.json') == False:
        print("ERROR: The save file must be a JSON file.")
        exit(1)

def get_thetas_values(args):
    required_keys = {"theta0", "theta1", "x_min", "x_max"}
    try:
        with open(args.filename, "r") as read_file:
            response = read_file.read()
            json_data = json.loads(response)
            if not required_keys.issubset(json_data.keys()):
                print(f"Error! '{args.filename}' must contain the keys: {', '.join(required_keys)}.")
                exit(-1)
            return json_data["theta0"], json_data["theta1"], json_data["x_min"], json_data["x_max"]
    except FileNotFoundError:
        print(f"Error! '{args.filename}' does not exist.")
        exit(-1)
    except Exception as e:
        print(f"Error reading '{args.filename}': {e}")
        exit(-1)

def price_estimation(args) :
    theta0, theta1, x_min, x_max = get_thetas_values(args)
    while(1):
        while(1):
            s = input("Wich mileage is on your car ? ")
            if not s:
                print('\nPlease enter a value')
            elif s == 'exit':
                print("Exiting the program.")
                exit(0)
            else:
                break
        if all([c in '0123456789' for c in s]):
            input_value = float(s)
            x = (input_value - x_min) / (x_max - x_min)
            value = theta0 + theta1 * x #here is the asked fonction
            if value < 0:
                print(f"The estimated value is negative, please check your input. ({value} €)")
            else:
                print(f"The estimated price for a car with {input_value} km is: {value:.2f} €")
        else :
            print('\nPlease enter a positive integer.')
        if (not args.loop):
            break



if __name__ == '__main__' :
    args = parse_arguments()
    check_arguments(args)
    price_estimation(args)
