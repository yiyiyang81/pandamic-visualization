import doctest


def which_delimiter(s):
    ''' (str) -> str
    take a string of number seperated by space or comma or tab and return
    the one that appears most often in the string.
    >>> which_delimiter('0 1 2,3')
    ' '
    >>> which_delimiter('0,1,2\\t3')
    ','
    >>> which_delimiter('0,1\\t2\\t3')
    '\\t'
    >>> which_delimiter('')
    Traceback (most recent call last):
    AssertionError: Empty Input
    '''
    counter = 0

    if len(s) == 0:
        raise AssertionError("Empty Input")

    if s.count(' ') == 0 and s.count(',') == 0 and s.count('\t') == 0:
        raise AssertionError("No delimiter")

    most_common = s[0]      #select a random character in input string
    for i in s:
        if i.isdigit() == False and s.count(i) > counter:
                counter = s.count(i)
                most_common = i

    return most_common


def stage_one(input_filename,output_filename):
    '''(str,str) ->int
    take names of two files, replace all the most appeared delimiters with tab and replace
    all the / and . with hyphen, return number of lines of the output file.
    >>> stage_one("data-short.txt", "stage1-short.tsv")
    10
    >>> stage_one("data.txt", "stage1.tsv")
    3000
    '''

    f = open(input_filename, 'r', encoding = 'utf-8')
    g = open(output_filename, 'w', encoding = 'utf-8')
    in_file = f.readlines()
    n1 = []
    n2 = []

    for j in in_file:
        j = j.replace(which_delimiter(j),'\t')
        n1.append(j)

    for i in n1:
        if i.count('/') != 0:
            i = i.replace('/','-')
        n2.append(i)

    #clean up . for date section only
    for k in n2:
        if k[:32].count('.') != 0:
            k = k[:32].replace('.','-')+k[32:]
        g.write(k.upper())

    f.close()
    g.close()
    return len(n2)


def stage_two(input_filename, output_filename):
    '''(str, str) -> int
    takes name of two files, clean all the lines that has more than 9 elements and write
    a new file with cleaned up data, return the number of lines of new file.
    >>> stage_two("stage1-short.tsv", "stage2-short.tsv")
    10
    >>> stage_two("stage1.tsv", "stage2.tsv")
    3000
    '''

    f = open(input_filename, 'r', encoding = 'utf-8')
    g = open(output_filename, 'w', encoding = 'utf-8')
    input_file = f.readlines()
    new_file = []
    
    for l in input_file:
        temp = l.split('\t')

        if temp[5][0] == "H" and temp[6][0].isdigit() == True:
            temp[5] = temp[5]+temp[6]
            temp.remove(temp[6])

        while "APPLICABLE" in temp:
            temp.remove("APPLICABLE")   
            temp[5] = temp[5].replace(' ', '')  #remove space between postal code

        if len(temp) == 10:
            temp[7] = temp[7] + '.' + temp[8]
            temp.remove(temp[8])

        s = "\t".join(temp)
        g.write(s)
        new_file.append(temp)

    f.close()
    g.close()
    return len(new_file)


if __name__ == "__main__":
    doctest.testmod()