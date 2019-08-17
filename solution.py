import sys
import csv
import pandas as pd
from decimal import *

getcontext().rounding = ROUND_FLOOR # rounding for Decimal module

# https://github.com/pandas-dev/pandas
# https://pandas.pydata.org/
# I'm using the pandas library to manipulate time data. 

# I'm also importing python's decimal module - i'm using this
# to avoid floating point errors. It also make data more readable for debugging


#  @param breaks - string
#  @return final_break_start, final_break_end string - string
# This function reformats break times to HH:MM based on format
# The earlist time work starts in dataset is 9 - so if the
# break time is less than or equal to 9 i'm assuming it in the PM

def return_break (breaks):
    final_break_start ='' 
    final_break_end ='' 
    br_values = breaks.split('-') # split at '-'
    br_val = [b.strip('PM') for b in br_values] #remove PM
    fin_br_list = [b.strip(' ') for b in br_val] # remove ' ' white space
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

#  calculate percentage from inputs or return loss
#  @param shift int
#  @param sale float
#  @return float

def percentage_calc(shift, sale):
    if shift >= sale:
        return sale - shift
    else: 
        percentage =(shift/sale) * 100
        return percentage
 
# Calculate shift costs. I create a dictionary of hours with 0 as initial value.
# Then I create another list of times - each 30min (the work times are in 30min blocks) and add wage
# to the initial hours dictionary. I use a similar principle to deduct break times. I'm using the decimal
# module here. It helps avoid floating point errors and makes debugging easier. Im returning a dictionary 
# with integer values as I was assuming this was what number meant on the guide? + the examples were integers. 
#  @param path_to_csv
#  @return dictionary
def process_shifts(path_to_csv):
    # create a list of times from 08:00 to 23:00
    times = pd.date_range(start=pd.Timestamp('08:00'), end=pd.Timestamp('23:00'), freq='60T').strftime('%H:%M')
    hours_dict = dict.fromkeys(times, 0) #hours dictionary which store values - values initally set to 0
    try:
        with open(path_to_csv, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, skipinitialspace=True)
            next(csv_reader) #skip header
            for line in csv_reader:
                if line: #check for blank line
                    start, end, wage, breaks = line[3], line[1], float(line[2]), line[0] #define variables
                    # A list or times from start to end of work at 30 min intervals
                    work_range = pd.date_range(start=pd.Timestamp(start), end=pd.Timestamp(end), freq='30T').strftime('%H:%M')
                    work_final = work_range.delete(-1) # delete final entry as this 30min is not working time
                    for hour in work_final:
                        f_wage = Decimal(.5 * wage).quantize(Decimal("1.00000"))
                        hours_dict[hour[:2]+':00'] += f_wage # add wage to hours_dict
                    # reformat break data to hh:mm
                    final_break_start, final_break_end = return_break(breaks)
                    # The shortest break is 10 mins so I'm creating a list of time at 10min intervals for breaks   
                    breaktime = pd.date_range(start=pd.Timestamp(final_break_start), end=pd.Timestamp(final_break_end), freq='10T').strftime('%H:%M')
                    br_final = breaktime.delete(-1) #delete last instance of list 
                    for f in br_final:
                        f_break = Decimal((1/6) * wage).quantize(Decimal("1.00000"))
                        hours_dict[f[:2]+':00'] -= f_break  # deduct wage from hours_dict for break
            # using for in loop to turn hours_dict value into an integer            
            for key,value in hours_dict.items():
                new = int(value)  
                hours_dict[key] = new
            return hours_dict     
    except IOError:
        print ("Could not read file:" + path_to_csv)
        sys.exit()

# Process sales by creating a list of times then adding the sales associated by each time
# @param  path_to_csv - string 
# @return hours_dict: dictionary
def process_sales(path_to_csv):
    # create a list of times from 08:00 to 23:00   
    times = pd.date_range(start=pd.Timestamp('08:00'), end=pd.Timestamp('23:00'), freq='60T').strftime('%H:%M')
    hours_dict = dict.fromkeys(times, 0) 
    try:
         with open(path_to_csv, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, skipinitialspace=True)
            next(csv_reader)
            for line in csv_reader:
                if line:
                    sales, time= Decimal(line[0]), line[1]
                    time_list = time.split(':')
                    time_hr = time_list[0]+ ':00'
                    if time_hr in hours_dict:
                        hours_dict[time_hr] += sales # add sale value to hours_dict dictionary
            for k,v in hours_dict.items():
                    new = float(v)   # convert to float
                    hours_dict[k] = new
            return hours_dict
    except IOError:
        print ("Could not read file:" + path_to_csv)
        sys.exit()

# Loop through value and calculate percentage for each time in dictionary
# @param shifts:dicionary
# @param sales:dicionary
# @return hour_dict : dictionary  
def compute_percentage(shifts, sales):
    times = pd.date_range(start=pd.Timestamp('08:00'), end=pd.Timestamp('23:00'), freq='60T').strftime('%H:%M')
    hours_dict = dict.fromkeys(times, 0) #hour list
    for k in hours_dict:
        value = percentage_calc(shifts[k], sales[k]) #call percentage_calc function to get %
        f_value = round(value)
        hours_dict[k] = f_value # add to dictionary
    return hours_dict

# Here I order the list by percentage value dictionary
# and select the first index which is greater than 0 (the best %)
# There are negative numbers in current dataset - however - there could not be so I am 
# checking for them. The first index will be the worst if there are negative numbers. If not it will 
# be the last index
# @param percentages: dictionary
# @return best_worst : list 

def best_and_worst_hour(percentages):
    hours = {}
    best_worst = []
    for key, value in sorted(percentages.items(), key=lambda item: item[1]): #sort dictionary
        hours.update( {key : value} ) #update hours
    for key in hours:
        if hours[key] > 0:
            best_worst.append(key)  # the first above 0 is the best %
            break
    negative = dict((k, v) for k, v in percentages.items() if v < 0) #filter for negative values to check if they are there
 
    if len(negative) > 0: 
        worst = next(iter(hours)) #use iter and next to get the first item in hours - this will be a negative value
        best_worst.append(worst) 
    else:
        h_elements = list(hours.keys())
        worst = h_elements[-1]  # if no negative numbers get last number in sorted list
        best_worst.append(worst)
    return best_worst
   

shifts = process_shifts('./data.csv')
sales = process_sales('./transactions.csv')
per = compute_percentage(shifts, sales)  
best_worst = best_and_worst_hour(per)

print(shifts)
print(sales)
print(per)
print(best_worst)