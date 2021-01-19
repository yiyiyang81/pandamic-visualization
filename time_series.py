import doctest
import datetime
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt

def date_diff(date1, date2):
    '''(str, str) -> int
    calculate how many days apart of two dates. if the first date is earlier
    than the second date, then the return value will be negative.
    >>> date_diff('2019-10-31', '2019-11-2')
    2
    >>> date_diff('2019-6-17', '2019-6-23')
    6
    >>> date_diff('2013-4-16', '2013-4-13')
    -3
    '''
    date1 = date1.split('-')
    date2 = date2.split('-')
    date1 = datetime.date(int(date1[0]), int(date1[1]), int(date1[2]))
    date2 = datetime.date(int(date2[0]), int(date2[1]), int(date2[2]))
    
    diff = date2 - date1 

    return diff.days


def get_age(date1, date2):
    '''(str, str) -> int
    calculate how many complete years aprart the two dates are assuming that
    there are 365.2425 days per year.if the first date is earlier than the 
    second date, then the return value will be negative.
    >>> get_age('2018-10-31', '2019-11-2')
    1
    >>> get_age('2018-10-31', '2000-11-2')
    -17
    >>> get_age('1998-08-08', '2018-08-08')
    20
    '''
    return int(date_diff(date1,date2)/365.2425)


def stage_three(input_filename,output_filename):
    '''(str,str) ->dict
    take names of two files, replace all the most appeared delimiters with tab and
    replace all the / and . with hyphen, return number of lines of the output file.
    >>> stage_three("stage2-short.tsv", "stage3-short.tsv")
    {'0': {'I': 2}, '1': {'I': 2}, '2': {'I': 2}, '3': {'I': 1}, '4': {'I': 1}, '6': {'I': 1}, '7': {'I': 1}}
    >>> stage_three("stage2.tsv", "stage3.tsv")
    '''

    f = open(input_filename, 'r', encoding = 'utf-8')
    g = open(output_filename, 'w+', encoding = 'utf-8')

    in_file = f.readlines()

    index_date = in_file[0].split('\t')
    index_date = index_date[2]


    duplicate1_in_file = in_file[:]
    d_o_r = []

    for l in duplicate1_in_file:
        count_d_o_r = 0

        while count_d_o_r != 2:
            l = l[l.find('\t')+1:]
            count_d_o_r +=1
        
        index_d_o_r = l[0:10]#trim the string to only desired date
        
        while index_d_o_r[-1].isdigit() == False:
            index_d_o_r = index_d_o_r[:len(index_d_o_r)-1]
        d_o_r.append(index_d_o_r)


    replaced1_in_file = []

    for f in in_file:
        for r in d_o_r:
            if r in f:
                f = f.replace(r, str(date_diff( index_date, r)))
                replaced1_in_file.append(f)



    d_o_b = []
    duplicate2_in_file = replaced1_in_file[:]

    for l in duplicate2_in_file:
        count_d_o_b = 0
        
        while count_d_o_b != 3:
            l = l[l.find('\t')+1:]
            count_d_o_b +=1

        index_d_o_b = l[0:10]

        while index_d_o_b[-1].isdigit() == False:
            index_d_o_b = index_d_o_b[:len(index_d_o_b)-1]
            l = l.replace(index_d_o_b, str(get_age(index_d_o_b, index_date)))
        d_o_b.append(index_d_o_b)


    replaced2_in_file = []

    for f in replaced1_in_file:
        for b in d_o_b:
            if b in f:
                f = f.replace(b, str(get_age(b, index_date)))
                replaced2_in_file.append(f)


    stage_three = []
    status_I = ['INFECTED', 'INFECTÉE', 'INFECTÉ', 'INF']
    status_R = ['RECOVERED', 'RECUPÉRÉE', 'RECUPÉRÉ']
    status_D = ['DEAD', 'MORTE', 'MORT', 'DEA', 'MOR']

    for f in replaced2_in_file:
        for i in status_I: 
            if i in f:
                f = f.replace(i, "I")
        for i in status_R:
            if i in f:
                f = f.replace(i, "R")
        for i in status_D:
            if i in f or f=="M":
                f = f.replace(i, "D")
        else:
                f = f
        stage_three.append(f)
        g.write(f)


    trimmed_list = []

    for l in stage_three:
        counter = 0

        while counter != 1:
            l = l[l.find('\t')+1:]
            counter +=1
            trimmed_list.append(l)

    trimmed_list = sorted(trimmed_list)#sort trimmed list so first entry is in ascending order
    

    status_list = []

    for l in trimmed_list:
        counter = 0     

        while counter != 5:
            l = l[l.find('\t')+1:]
            counter +=1
        status_list.append(l)


    dict_return = {}
    dict_child = {}     #create small dictionary that should be in the big dictionary
    temp = trimmed_list[0].find('\t')
    x1 = trimmed_list[0][:temp]     #set initial value as the first day of first line of trimmed_list
    ctr = 0

    for x in trimmed_list:

        day = x[:x.find('\t')]#set day as first entry of each line 

        print("X1 = " + x1)
        print(day)
        if day == x1:
            temp = status_list[ctr].find('\t')
            status = status_list[ctr][:temp]
            if status not in dict_child:
                dict_child[status] = 1
            else:
                dict_child[status] +=1

        else: 
            dict_return[x1] = dict_child    #runs here if day column is not the same as previous one anymore
            dict_child = {}     #reset dict_child as an empty dictionary
            x1 = day        #update x1 to be a new day
            temp = status_list[ctr].find('\t')
            status = status_list[ctr][:temp]

            if status not in dict_child:
                dict_child[status] = 1
            else:
                dict_child[status] +=1

        ctr += 1

    dict_return[x1] = dict_child

    g.close()

    print(dict_return)

    return dict_return



def plot_time_series(dict):
    '''(dict)-> list
    take a dictionary of dictionaires as input and return a list of lists where each
    sublist represents each day of pandemic with format [# infected, #recovered, #dead].
    >>> d = stage_three('stage2-short.tsv', 'stage3-short.tsv')
    >>> plot_time_series(d)
    [[2, 0, 0], [2, 0, 0], [2, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]]
    '''
    all = []

    for d in dict:
        s = dict.get(d) 
        day = []       

        if s.get('I') != None:
            day.append(s.get('I'))
        else:
            day.append(0)

        if s.get('R') != None:
            day.append(s.get('R'))
        else:
            day.append(0)

        if s.get('D') != None:
            day.append(s.get('D'))
        else:
            day.append(0)

        all.append(day)

    inf = rec = dea = 0
    infected = []
    recovered = []
    dead = []

    for l in all:
        inf += l[0]
        infected.append(inf)
        rec += l[1]
        recovered.append(rec)
        dea += l[2]
        dead.append(dea)


    x = list(range(len(all)))
    plt.plot(x, infected)
    plt.plot(x, recovered)
    plt.plot(x, dead)
    plt.title("Time series of early pandemic")
    plt.xlabel('Days into Pandemi')
    plt.ylabel('Number of People')
    plt.legend(['Infected', 'Recovered', 'Dead'])
    
    plt.savefig('time_series.png')
    return all



if __name__ == "__main__":
    doctest.testmod()