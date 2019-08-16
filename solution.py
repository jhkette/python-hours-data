import csv
import pandas as pd


# https://github.com/pandas-dev/pandas
# https://pandas.pydata.org/
# I'm using the pandas library to manipulate time data. 

# THE THING YOU NEED TO FIX IS 4:30 - 5:30
# Look at 4:30 - 5:30pm - this works fine

def return_break (breaks, start):
    final_break_start ='' 
    final_break_end ='' 
    br_values = breaks.split('-') 
    br_val = [b.strip('PM') for b in br_values]
    first = [b.strip(' ') for b in br_val]
    # Handle if PM is in the break string
    # you need to change this with an or statement to make it shorter
    #basically get rid of PM in breaks if else statement
    
    #  deal with one integer first numbers 
    if (len(first[0]) == 1):
        if((int(first[0]) < 9) or 'PM' in breaks):
            new = int(first[0]) + 12
            final_break_start = str(new) +':00'
            print(final_break_start)
            print('THIS IS IMPORTANT ')
        else: 
            final_break_start = first[0] + ':00'
    else: 
        mins = first[0].split('.')
        hour = int(mins[0]) + 12
        mins = ':'+mins[1] 
        final_break_start = str(hour) + mins
        print(final_break_start)

    if (len(first[1]) == 1):
        if((int(first[1]) < 9) or 'PM' in breaks):
            new = int(first[1]) + 12
            final_break_end = str(new) +':00'
            print(final_break_end )
            print('THIS IS IMPORTANT ')
        else: final_break_end  =first[1] + ':00'
    else:
        mins = first[1].split('.')
        # mins = first[1].split(':')
        hour = int(mins[0]) + 12
        mins = ':'+mins[1] 
        final_break_end = str(hour) + mins
        print(final_break_end)
    return final_break_start, final_break_end 




# create a list of times from 00:00 to 23:00
times = pd.date_range(start=pd.Timestamp('00:00'), end=pd.Timestamp('23:00'), freq='60T').strftime('%H:%M')
hours_dict = dict.fromkeys(times, 0) 
with open('./data.csv', 'r') as csv_file:
    try:
        csv_reader = csv.reader(csv_file, skipinitialspace=True)
        
        for line in csv_reader:
            start, end,  wage, breaks = line[0], line[1], int(line[2]), line[3]
            lst = pd.date_range(start=pd.Timestamp(start), end=pd.Timestamp(end), freq='30T').strftime('%H:%M')
            ls = lst.delete(-1)
            for l in ls:
                value = l[:2]+':00'
                hours_dict[value] += (.5 * wage)
            # managing breaks data
            final_break_start, final_break_end = return_break(breaks, start)   
            breaktime = pd.date_range(start=pd.Timestamp(final_break_start), end=pd.Timestamp(final_break_end), freq='10T').strftime('%H:%M')
            fin = breaktime.delete(-1) #delete last instance of list 
            print(fin)
            for f in fin:
                b = f[:2]+':00'
                hours_dict[b] -= ((1/6) * wage)
    except IOError:
        print ("Could not read file:",'./data.csv')
    

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







  

print(hours_dict)