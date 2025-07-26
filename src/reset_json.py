import json

if __name__ == '__main__' :
    with open("thetas.json", 'w') as f:
        json.dump({
            'theta0': 0,
            'theta1': 0,
            'x_min': 0,
            'x_max': 1
        }, f)
