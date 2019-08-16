import sys
import csv
import pandas as pd
from decimal import *


# getcontext().prec = 5 
getcontext().rounding = ROUND_FLOOR

# https://github.com/pandas-dev/pandas
# https://pandas.pydata.org/
# I'm using the pandas library to manipulate time data. 

# I'm also importing python's decimal library - i'm using this
# to avoid floating point errors. It also make data more readbale for debugging


# The earlist time work starts in dataset is 9 - so if the
# break time is less than or equal to 9 i'm assuming it in the PM
def return_break (breaks):
    final_break_start ='' 
    final_break_end ='' 
    br_values = breaks.split('-') 
    br_val = [b.strip('PM') for b in br_values]
    first = [b.strip(' ') for b in br_val]
    if not ("." or ":") in first[0]:
        if int(first[0]) < 9 or 'PM' in breaks:
            new = int(first[0]) + 12
            final_break_start = str(new) +':00'
        else: 
            final_break_start = first[0] + ':00'
    else: 
        mins = first[0].split('.')
        hour = int(mins[0]) 
        if 'PM' in breaks or hour <= 9:
            hour = hour + 12
        mins = ':' + mins[1] 
        final_break_start = str(hour) + mins

    if not ("." or ":") in first[1]:
        if int(first[1]) <= 9 or 'PM' in breaks:
            new = int(first[1]) + 12
            final_break_end = str(new) +':00'
        else: final_break_end  =first[1] + ':00'
    else:
        mins = first[1].split('.')
        hour = int(mins[0])
        if 'PM' in breaks or hour <= 9:
            hour = hour + 12
        mins = ':'+mins[1] 
        final_break_end = str(hour) + mins
    return final_break_start, final_break_end 


def process_shifts(path_to_csv):
    # create a list of times from 00:00 to 23:00
    times = pd.date_range(start=pd.Timestamp('00:00'), end=pd.Timestamp('23:00'), freq='60T').strftime('%H:%M')
    hours_dict = dict.fromkeys(times, 0) 
    with open(path_to_csv, 'r') as csv_file:
        try:
            csv_reader = csv.reader(csv_file, skipinitialspace=True)
            
            next(csv_reader) #skip header
            for line in csv_reader:
                if line: #check for blank line
                    start, end, wage, breaks = line[3], line[1], float(line[2]), line[0]
                    lst = pd.date_range(start=pd.Timestamp(start), end=pd.Timestamp(end), freq='30T').strftime('%H:%M')
                    ls = lst.delete(-1)
                    for l in ls:
                        value = l[:2]+':00'
                        f_wage = Decimal(.5 * wage).quantize(Decimal("1.000"))
                        hours_dict[value] += f_wage
                    # managing breaks data
                    final_break_start, final_break_end = return_break(breaks)
                    # The shortest break is 10 mins so I'm    
                    breaktime = pd.date_range(start=pd.Timestamp(final_break_start), end=pd.Timestamp(final_break_end), freq='10T').strftime('%H:%M')
                    fin = breaktime.delete(-1) #delete last instance of list 
                    for f in fin:
                        b = f[:2]+':00'
                        f_break = Decimal((1/6) * wage).quantize(Decimal("1.000"))
                        hours_dict[b] -= f_break

            for k,v in hours_dict.items():
                new = int(v)  
                hours_dict[k] = new
            return hours_dict     
        except IOError:
            print ("Could not read file:",path_to_csv)
            sys.exit()

            
def process_sales(path_to_csv):   
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


data = process_shifts('./data.csv')
data2 = process_sales('./transactions.csv')

print(data)
print(data2)


def compute_percentage(shifts, sales):
    times = pd.date_range(start=pd.Timestamp('00:00'), end=pd.Timestamp('23:00'), freq='60T').strftime('%H:%M')
    hours_dict = dict.fromkeys(times, 0) 
    

    

        # deduct breaks
        # you need to explode at '-'
          
            
# print(times)
# print(hours)
# minimun = min(hours)
# maximun = max(hours)

# hourlist = list(range(minimun, maximun)
# print(hourlist)

# a = [1,2,3,4]
# d = dict.fromkeys(a, 0)

# hours = [[datetime.time(i).strftime("%H:%M"), 0] for i in range(9,24)]
# hours_dict = dict(hours)







  

