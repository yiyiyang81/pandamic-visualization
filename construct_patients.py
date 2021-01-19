import doctest
import matplotlib as plt
import matplotlib.pyplot as plt

class Patient:
    '''
    >>> p = Patient( '0', '0', '42', 'WOMAN', 'H3Z2B5', 'I', '102,2', '12')
    >>> str(p)
    '0\\t42\\tF\\tH3Z\\t0\\tI\\t12\\t39.0'
    >>> p1 = Patient('0', '1', '42', 'F', 'H3Z', 'I', '40,0 C', '13')
    >>> p.update(p1)
    >>> str(p)
    '0\\t42\\tF\\tH3Z\\t0\\tI\\t13\\t39.0;40.0'
    '''
    def __init__(self, n, dd, a, sg, p, s, t, ds):
        
        self.num = int(n)
        self.day_diagnosed = int(dd)
        self.age = int(a)

        #check for all the cases of gender
        if sg == "M" or sg == "H" or sg == "HOMME" or sg == "MALE" or sg == "MAN" or sg == "BOY":
            self.sex_gender = "M"

        elif sg == "F" or sg == "FEMME" or sg == "FEMALE" or sg == "GIRL" or sg == "WOMAN":
            self.sex_gender = "F"

        else:
            self.sex_gender = "X"

        #check for all the cases of postal code
        if p =="N.A." or p =="N-A" or p =="NA" or p =="NON" or p =="NONAPPLICABLE" or p == "NOTAPPLICABLE":
            self.postal = "000"

        elif p[0] != "H" or p[1].isdigit() == False or p[2].isalpha() == False:#check if is a valid form of postal code
            self.postal = "000"

        else:
            self.postal = p[0:3]

        self.state = s
        self.temps = []

        if t == "NA" or t == "N.A." or t == "N-A" or t == "NON APPLICABLE" or t == "NON" or t == "NOT APPLICABLE":
            t = 0
        else:
            if t.find("°") != -1:
                t = t.replace("°", "")
            if t.find("C") != -1:
                t = t.replace("C", "")
            if t.find("F") != -1:
                t = t.replace("F", "")
            if t.find(',') != -1 :
                t = t.replace(',', '.')

            t = float(t)

            if t>45:
                t = (t-32)*5/9

        self.temps.append(round(t, 2))

        self.days_symptomatic = int(ds)


    def __str__(self):
        temp = []
        for x in self.temps:
            temp.append(str(x))

        temps_list = ";".join(temp)

        s = str(self.num) + "\t" + str(self.age) + "\t" + self.sex_gender + "\t" + self.postal

        s += "\t" + str(self.day_diagnosed) + "\t" + self.state + "\t" + str(self.days_symptomatic) + "\t" + temps_list
        return s


    def update(self, p):

        if self.num == p.num and self.sex_gender == p.sex_gender and self.postal == p.postal:
            self.days_symptomatic = p.days_symptomatic
            self.state = p.state

            for i in p.temps:
                self.temps.append(i)#append into the temperature list

        else: 
            raise AssertionError("not the same patient, cannot update")


def stage_four(input_filename, output_filename):
    '''(str, str) -> dict
    creates a new Patient object for each line and return a dictionary for all the patient
    with patient's number as key and other data as its value.
    >>> p = stage_four('stage3-short.tsv', 'stage4-short.tsv')
    >>> str(p[0])
    '0\\t73\\tM\\tH3W\\t0\\tI\\t5\\t40.0;41.0'
    '''
    f = open(input_filename, 'r', encoding = 'utf-8')
    g = open(output_filename, 'w+', encoding = 'utf-8')
    
    in_file = f.readlines()
    p = {}

    for l in in_file:
        i = l.split('\t')
        
        #create a patient object
        pat = Patient(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
        
        if pat.num in p:
            try:
                p[pat.num].update(pat)
            except AssertionError:
                #if not the same patient, does not update, continue to next
                continue
        else:
            p[pat.num] = pat
    
    sorted_dict={}

    #sort the patient list by patient number
    for k in sorted(p.keys()):
        sorted_dict[k] = p[k]

    #write the sorted list into the output file
    for k in sorted_dict:
        g.write(str(sorted_dict[k])+'\n')

    f.close()
    g.close()

    return sorted_dict


def fatality_by_age(patients):
    '''(dict) -> list
    plot the probability of fatality versus age, generate a graph and
    return a list of fatality by age group.
    >>> p = stage_four('stage3-short.tsv', 'stage4-short.tsv')
    >>> fatality = fatality_by_age(p)
    >>> print(fatality)
    []
    >>> p = stage_four('stage3.tsv', 'stage4.tsv')
    >>> fatality = fatality_by_age(p)
    '''

    big_pat_list = {} 

    for k in patients:
        pat = patients[k]
        age = pat.age
        last_digit = age%10
        stat = pat.state

        if last_digit <3:
            last_digit = 0
            age = int(age/10)*10+last_digit

        elif last_digit>2 and last_digit <8:
            last_digit = 5
            age = int(age/10)*10+last_digit

        else:
            last_digit = 0
            age = int(age/10+1)*10+last_digit

        if stat == 'R' or stat == 'D': 

            if age not in big_pat_list: 
                big_pat_list[age] = {'D':0, 'R': 0}

                if stat == 'R': 
                    big_pat_list[age]['R'] +=1

                elif stat == 'D':
                    big_pat_list[age]['D'] +=1

            else: 
                if stat == 'R': 
                    big_pat_list[age]['R'] +=1

                elif stat == 'D':
                    big_pat_list[age]['D'] +=1

    fat = []

    for k in sorted(big_pat_list.keys()): 
        dead = big_pat_list[k]['D'] 
        recov = big_pat_list[k]['R']
        fat.append(dead/(dead + recov))

    x = sorted(big_pat_list.keys())
    plt.ylim((0, 1.2))
    plt.plot(x, fat)
    plt.title("Probability of death vs age")
    plt.xlabel('Age (to nearest 5)')
    plt.ylabel('Deaths / (Deaths+Recoveries)')
    plt.savefig('fatality_by_age.png')
    return fat

if  __name__ == "__main__":
    doctest.testmod()
   
