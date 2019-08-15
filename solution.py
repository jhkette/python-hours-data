import csv
import pandas as pd


# https://github.com/pandas-dev/pandas
# https://pandas.pydata.org/
# I'm using the pandas library to manipulate time data. 



def return_break (breaks, start):
    final_break_start ='' 
    final_break_end ='' 
    # Handle if PM is in the break string
    if 'PM' in breaks:
        br_values = breaks.split('-') 
        br_val = [b.strip('PM') for b in br_values]
        first = [b.strip(' ') for b in br_val]
        if (len(first[0]) == 1):
            if(int(first[0]) < 8):
                new = int(first[0]) + 12
                final_break_start = str(new) +':00'
                print(final_break_start)
                print('THIS IS IMPORTANT ')
            else: final_break_start =first[0] + ':00'
        else: 
            mins = first[0].split('.')
            hour = int(mins[0]) + 12
            mins = ':'+mins[1] 
            final_break_start = str(hour) + mins
            print(final_break_start)

        if len(first[1]) == 1:
              if(int(first[1]) < 8):
                new1 = int(first[1]) + 12
                final_break_end = str(new1) +':00'
                print('THIS IS IMPORTANT ')
        else:
            mins = first[1].split('.')
            # mins = first[1].split(':')
            hour = int(mins[0]) + 12
            mins = ':'+mins[1] 
            final_break_end = str(hour) + mins
            print(final_break_end)
            # NEED TO ACCOUNT FOR 3-4 without pm here
    else: 
            br_values = breaks.split('-') 
            first = [b.strip(' ') for b in br_values]
            if (len(first[0]) == 1):
                if(int(first[0]) < 8):
                    new = int(first[0]) + 12
                    final_break_start = str(new) +':00'
                else: final_break_start =first[0] + ':00'
            elif len(first[0]) == 2:
                final_break_start = str(first[0]) +':00'
                print(final_break_start)
            else: 
                final_break_start = first[0].replace('.', ':')
                print(final_break_start)
            if (len(first[1]) == 1):
                if(int(first[1]) < 8):
                    new = int(first[1]) + 12
                    final_break_end = str(new) +':00'
                else: final_break_end =first[1] + ':00'
            elif len(first[1]) == 2:
                final_break_end = str(first[1]) +':00'
                print(final_break_end)
            else: 
                final_break_end = first[1].replace('.', ':')
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