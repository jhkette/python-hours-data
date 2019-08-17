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
    fin_br_list = [b.strip(' ') for b in br_val]
    if not "." in fin_br_list[0]:
        if int(fin_br_list[0]) < 9 or 'PM' in breaks:
            new = int(fin_br_list[0]) + 12
            final_break_start = str(new) +':00'
        else: 
            final_break_start = fin_br_list[0] + ':00'
    else: 
        mins = fin_br_list[0].split('.')
        hour = int(mins[0]) 
        if 'PM' in breaks or hour <= 9:
            hour = hour + 12
        mins = ':' + mins[1] 
        final_break_start = str(hour) + mins
    if not "."  in fin_br_list[1]:
        if int(fin_br_list[1]) <= 9 or 'PM' in breaks:
            new = int(fin_br_list[1]) + 12
            final_break_end = str(new) +':00'
        else: final_break_end  =fin_br_list[1] + ':00'
    else:
        mins = fin_br_list[1].split('.')
        hour = int(mins[0])
        if 'PM' in breaks or hour <= 9:
            hour = hour + 12
        mins = ':'+mins[1] 
        final_break_end = str(hour) + mins
    return final_break_start, final_break_end 



def percentage_calc(shift, sale):
    if shift >= sale:
        return sale - shift
    else: 
        percentage =(shift/sale) * 100
        return percentage


def process_shifts(path_to_csv):
    # create a list of times from 00:00 to 23:00
    times = pd.date_range(start=pd.Timestamp('08:00'), end=pd.Timestamp('23:00'), freq='60T').strftime('%H:%M')
    hours_dict = dict.fromkeys(times, 0) 
    try:
        with open(path_to_csv, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, skipinitialspace=True)
            next(csv_reader) #skip header
            for line in csv_reader:
                if line: #check for blank line
                    start, end, wage, breaks = line[3], line[1], float(line[2]), line[0]
                    work_range = pd.date_range(start=pd.Timestamp(start), end=pd.Timestamp(end), freq='30T').strftime('%H:%M')
                    work_final = work_range.delete(-1)
                    for hour in work_final:
                        wrk_hr = hour[:2]+':00'
                        f_wage = Decimal(.5 * wage).quantize(Decimal("1.00000"))
                        hours_dict[wrk_hr] += f_wage
                    # managing breaks data
                    final_break_start, final_break_end = return_break(breaks)
                    # The shortest break is 10 mins so I'm    
                    breaktime = pd.date_range(start=pd.Timestamp(final_break_start), end=pd.Timestamp(final_break_end), freq='10T').strftime('%H:%M')
                    br_final = breaktime.delete(-1) #delete last instance of list 
                    for f in br_final:
                        b = f[:2]+':00'
                        f_break = Decimal((1/6) * wage).quantize(Decimal("1.00000"))
                        hours_dict[b] -= f_break

            for key,value in hours_dict.items():
                new = int(value)  
                hours_dict[key] = new
            return hours_dict     
    except IOError:
        print ("Could not read file:",path_to_csv)
        sys.exit()

            
def process_sales(path_to_csv):   
    times = pd.date_range(start=pd.Timestamp('08:00'), end=pd.Timestamp('23:00'), freq='60T').strftime('%H:%M')
    hours_dict = dict.fromkeys(times, 0)
    try:
         with open('transactions.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file, skipinitialspace=True)
            next(csv_reader)
            for line in csv_reader:
                if line:
                    sales, time= Decimal(line[0]), line[1]
                    time_list = time.split(':')
                    time_hr =  time_list[0]+ ':00'
                    if time_hr in hours_dict:
                        hours_dict[time_hr] += sales 
            for k,v in hours_dict.items():
                    new = float(v)  
                    hours_dict[k] = new
            return hours_dict
    except IOError:
        print ("Could not read file:")
        sys.exit()


shifts = process_shifts('./data.csv')
sales = process_sales('./transactions.csv')


print(shifts)



def compute_percentage(shifts, sales):
    times = pd.date_range(start=pd.Timestamp('08:00'), end=pd.Timestamp('23:00'), freq='60T').strftime('%H:%M')
    hours_dict = dict.fromkeys(times, 0)
    for k in hours_dict:
        value = percentage_calc(shifts[k], sales[k])
        f_value = round(value)
     
        hours_dict[k] = f_value
    return hours_dict



p = compute_percentage(shifts, sales)
# print(p)

def best_and_worst_hour(percentages):
    hours = {}
    best_worst = []
    for key, value in sorted(percentages.items(), key=lambda item: item[1]):
        hours.update( {key : value} )
    for key in hours:
        if hours[key] > 0:
            best_worst.append(key) 
            break
    worst = next(iter(hours))
    best_worst.append(worst) 
    print(best_worst)
   
    return best_worst
   

  
  
best_and_worst_hour(p)
