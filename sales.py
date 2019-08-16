import csv
import sys
import pandas as pd
from decimal import *


times = pd.date_range(start=pd.Timestamp('00:00'), end=pd.Timestamp('23:00'), freq='60T').strftime('%H:%M')
hours_dict = dict.fromkeys(times, 0) 
with open('transactions.csv', 'r') as csv_file:
    try:
        csv_reader = csv.reader(csv_file, skipinitialspace=True)
        next(csv_reader)
        for line in csv_reader:
            if line:
                sales, time= Decimal(line[0]), line[1]
                time_list = time.split(':')
                time_ch =  time_list[0]+ ':00'
                if time_ch in hours_dict:
                    hours_dict[time_ch] += sales 
                else:
                    print('nope')
        for k,v in hours_dict.items():
                new = float(v)  
                hours_dict[k] = new
        return hours_dict
    except IOError:
            print ("Could not read file:")
            sys.exit()


# d = dict()

# for i in range(100):
#     key = i % 10
#     
print(hours_dict)