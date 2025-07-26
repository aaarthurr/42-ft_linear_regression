import math

def give_score(real_price, prediction):
    print("------------------------------ STATS ------------------------------")
    print(f"The current settings give a presicision of :{round(r2_score(real_price, prediction) * 100, 2)}%")
    print(f"And gives an average error of :{round(calculate_pourcent_error(real_price, prediction), 2)}%")
    lowest_error, lowest_index, biggest_error, biggest_index, average_error = average_absolute_error(real_price, prediction)
    print(f"The average error is: {round(average_error, 2)}")
    print(f"The lowest error is: {round(lowest_error, 2)} [real price: {round(real_price[lowest_index], 2)}, prediction: {round(prediction[lowest_index], 2)}]")
    print(f"The biggest error is: {round(biggest_error, 2)} [real price: {round(real_price[biggest_index], 2)}, prediction: {round(prediction[biggest_index], 2)}]")
    print("-------------------------------------------------------------------")

def r2_score(real_price, prediction):
    mean_y = sum(real_price) / len(real_price)
    ss_tot = sum((y - mean_y) ** 2 for y in real_price)
    ss_res = sum((real_price[i] - prediction[i]) ** 2 for i in range(len(real_price)))
    return 1 - (ss_res / ss_tot)

def average_absolute_error(real_price, prediction):
    lowest_error = float('inf')
    lowest_index = -1
    biggest_error = 0
    biggest_index = -1
    average_error = 0
    for i in range(len(real_price)):
        error = abs(real_price[i] - prediction[i])
        average_error += error
        if error < lowest_error:
            lowest_error = error
            lowest_index = i
        if error > biggest_error:
            biggest_error = error
            biggest_index = i   
    average_error /= len(real_price)
    return lowest_error, lowest_index, biggest_error, biggest_index, average_error

def calculate_pourcent_error(real_price, prediction):
    average = 0
    for i in range(len(real_price)):
        if (real_price[i] == 0):
            continue
        average += abs(real_price[i] - prediction[i]) / abs(real_price[i]) * 100
    return average / len(real_price)