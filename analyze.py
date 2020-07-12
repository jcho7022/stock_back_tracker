import csv
import matplotlib.pyplot as plt

init_balance = 1
mv_start_counter = 0 
sum_200_days = 0
header_flag = True
arr_200_ma = []
arr_delta  = []
close_prices= []
dates = []

with open('SOXX.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if header_flag:
            header_flag = False
            continue
        close_prices.append((row[0] ,float(row[4])))
        dates.append(row[0])

dates = dates[201:len(dates)]

arr_200_ma   = []
arr_delta_t1 = []
arr_delta_t2 = []
arr_delta_t3 = []
i = 200
while i < len(close_prices):
    ma200 = sum(pair[1] for pair in close_prices[i-200:i]) / 200
    delta = (close_prices[i][1] - close_prices[i - 1][1])/close_prices[i-1][1]
    arr_200_ma.append((ma200, close_prices[i][0]))
    arr_delta_t1.append(delta * 1 + 1)
    arr_delta_t2.append(delta * 2 + 1)
    arr_delta_t3.append(delta * 3 + 1)
    i += 1

i = 200
buy = True
payday_count = 14
balance    = 1
balance_t1 = 1
balance_t2 = 1
balance_t3 = 1

balance_t1_arr = [] 
balance_t2_arr = []
balance_t3_arr = [] 

num_sell = 0
num_buy = 0
close_sell = 0
close_buy  = 0

while i < len(close_prices) - 1:
    if i == 200:
        i += 1
        continue

    balance_t1_arr.append(balance_t1)
    balance_t2_arr.append(balance_t2)
    balance_t3_arr.append(balance_t3)

    payday_count -= 1
    if payday_count == 0:
        balance_t1 += 500
        balance_t2 += 500
        balance_t3 += 500
        payday_count = 30
 
    if arr_200_ma[i-201][0] > close_prices[i][1] and buy:
        if arr_200_ma[i-201][0] / close_prices[i][1] < 1.004:
            balance_t1 = balance_t1 * 0.995 # some penalty
            balance_t2 = balance_t2 * 0.980
            balance_t3 = balance_t3 * 0.985
            close_sell += 1
        balance_t1 = balance_t1 * arr_delta_t1[i-200]
        balance_t2 = balance_t2 * arr_delta_t2[i-200]
        balance_t3 = balance_t3 * arr_delta_t3[i-200]
        balance_t1 -= 5
        balance_t2 -= 5
        balance_t3 -= 5
        buy = False
        num_sell += 1
    elif arr_200_ma[i-201][0] < close_prices[i][1] and not buy:
        buy = True
        num_buy += 1
        if close_prices[i][1] / arr_200_ma[i-201][0] < 1.004:
            close_buy += 1
            balance_t1 = balance_t1 * 0.995
            balance_t2 = balance_t2 * 0.990
            balance_t3 = balance_t3 * 0.985
        balance_t1 -= 5
        balance_t2 -= 5
        balance_t3 -= 5
        continue

    if buy:
        balance_t1 = balance_t1 * arr_delta_t1[i-200]
        balance_t2 = balance_t2 * arr_delta_t2[i-200]
        balance_t3 = balance_t3 * arr_delta_t3[i-200]

    i += 1

print(num_buy)
print(close_buy)
print(num_sell)
print(close_sell)
plt.plot(balance_t3_arr)
plt.show()
