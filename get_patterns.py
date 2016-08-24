import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

##sample sizes that are multiples of 40 round incorrectly, so I wrote my own function
def round_up(number,places):
    if type(number)==type('string'):
        pass
    else:
        number=repr(number)
    if number[-1]=='5':
        decimals=len(number.split('.')[-1])
        if places<decimals:
            return round(float(number[:-1]+'6'),places)
        else:
            return round(float(number),places)
    else:
        return round(float(number),places)



###smaller numbers are viewed to have less floating point errors than larger numbers

for N in range(5,100):
    f=open(os.path.join(BASE_DIR,'raw_variances',str(N)+'.txt'))
    f.readline()
    all_data=[[float(i.split('\t')[0]),eval(i.strip().split('\t')[-1])] for i in f]
    data=[[int(i[0]),round_up('.'+repr(i[0]).split('.')[1],12)] for i in all_data]
    #step1
    #check pattern 0
##    print 'pattern 0'
    pattern_zero=[i[1] for i in data if i[0]==0]
    size=len(set(pattern_zero))
    pattern_zero_decimals=12
    for j in range(7,12)[::-1]:
        pattern=[round_up(i,j) for i in pattern_zero]
        newsize=len(set(pattern))
        if size!=newsize:
            size=newsize
            pattern_zero_decimals=j
            pattern_0=sorted(list(set(pattern)))
        else:
            pass


    #step2
    #check pattern 1
##    print 'pattern 1'
    pattern_one=[i[1] for i in data if i[0]==1]
    size=len(set(pattern_one))
    pattern_one_decimals=12
    for j in range(7,12)[::-1]:
        pattern=[round_up(i,j) for i in pattern_one]
        newsize=len(set(pattern))
        if size!=newsize:
            size=newsize
            pattern_one_decimals=j
            pattern_1=sorted(list(set(pattern)))
        else:
            pass


    #step3
    #check pattern 2
##    print 'pattern 2'
    pattern_two=[i[1] for i in data if i[0]==2]
    size=len(set(pattern_two))
    pattern_two_decimals=12
    for j in range(7,12)[::-1]:
        pattern=[round_up(i,j) for i in pattern_two]
        newsize=len(set(pattern))
        if size!=newsize:
            size=newsize
            pattern_two_decimals=j
            pattern_2=sorted(list(set(pattern)))
        else:
            pass
    #step4
    #check pattern 3
##    print 'pattern 3'
    pattern_three=[i[1] for i in data if i[0]==3]
    size=len(set(pattern_three))
    pattern_three_decimals=12
    for j in range(7,12)[::-1]:
        pattern=[round_up(i,j) for i in pattern_three]
        newsize=len(set(pattern))
        if size!=newsize:
            size=newsize
            pattern_three_decimals=j
            pattern_3=sorted(list(set(pattern)))
        else:
            pass

    #step5
    #check pattern 4
##    print 'pattern 4'
    pattern_four=[i[1] for i in data if i[0]==4]
    size=len(set(pattern_four))
    pattern_four_decimals=12
    for j in range(7,12)[::-1]:
        pattern=[round_up(i,j) for i in pattern_four]
        newsize=len(set(pattern))
        if size!=newsize:
            size=newsize
            pattern_four_decimals=j
            pattern_4=sorted(list(set(pattern)))
        else:
            pass

    #step6
    #match patterns
    #get as many decimals as possible

    if pattern_zero_decimals==12:
        pattern_0=pattern_zero

    if pattern_one_decimals==12:
        pattern_1=pattern_one

    if pattern_two_decimals==12:
        pattern_2=pattern_two

    if pattern_three_decimals==12:
        pattern_3=pattern_three

    if pattern_four_decimals==12:
        pattern_4=pattern_four



    if [repr(i)[:pattern_three_decimals-2] for i in pattern_1]!=[repr(i)[:pattern_three_decimals-2] for i in pattern_3]:
        print 'odd error', N

    if [repr(i)[:pattern_four_decimals-2] for i in pattern_2]!=[repr(i)[:pattern_four_decimals-2] for i in pattern_4]:
        print 'even error', N


    ##ensure all of pattern 0 is encompassed by the other patterns
    ##for odd patterns need to make sure variances are unique for the averages

    check=[repr(i)[:pattern_two_decimals-2] for i in pattern_2]
    for i in [repr(i)[:pattern_two_decimals-2] for i in pattern_0]:
        if i not in check:
            print 'zero error', N

    pattern_size=len(pattern_1)+len(pattern_2)
    if pattern_size%N!=0:
            print 'pattern error', N
    if N%2==0:
        pass
    else:
        ##this is unnecessary now that i'm splitting up the averages
        if len(set([repr(i)[:pattern_three_decimals-2] for i in pattern_1]+[repr(i)[:pattern_three_decimals-2] for i in pattern_2]))!=pattern_size:
            print 'average problem', N


    #get the averages, limit the variance decimals to what you currently have
    #need to find longest list of averages, get decimals, map to most precise variance

    longest_averages_even={}
    longest_averages_odd={}
    for i in all_data:
        value=round_up('.'+repr(i[0]).split('.')[1],7)
##        print i[0],value
        if int(i[0])%2==0:
            if value in longest_averages_even:
                if len(i[1])>len(longest_averages_even[value]):
                    longest_averages_even[value]=i[1]
            else:
                longest_averages_even[value]=i[1]
        else:
            if value in longest_averages_odd:
                if len(i[1])>len(longest_averages_odd[value]):
                    longest_averages_odd[value]=i[1]
            else:
                longest_averages_odd[value]=i[1]
    
    averages_even={}
    averages_odd={}
    if N%2==0:
        if len(longest_averages_odd)!=len(pattern_1):
            print 'average error',N
        else:
            mydata=sorted(zip(longest_averages_odd.keys(),longest_averages_odd.values()))
            for index,i in enumerate(pattern_1):
                averages_odd[i]=list(set([round_up('.'+repr(j).split('.')[1],13) for j in mydata[index][1]]))
                if round_up(i%1,7)!=mydata[index][0]:
                    print round_up(i%1,7),mydata[index][0]
        averages_even=averages_odd
    else:
        if len(longest_averages_odd)!=len(pattern_1) or len(longest_averages_even)!=len(pattern_2):
            print 'average error',N
        else:
            mydata=sorted(zip(longest_averages_odd.keys(),longest_averages_odd.values()))
            for index,i in enumerate(pattern_1):
                averages_odd[i]=list(set([round_up('.'+repr(j).split('.')[1],13) for j in mydata[index][1]]))
                if round_up(i%1,7)!=mydata[index][0]:
                    print round_up(i%1,7),mydata[index][0]
            mydata=sorted(zip(longest_averages_even.keys(),longest_averages_even.values()))
            for index,i in enumerate(pattern_2):
                averages_even[i]=list(set([round_up('.'+repr(j).split('.')[1],13) for j in mydata[index][1]]))
                if round_up(i%1,7)!=mydata[index][0]:
                    print round_up(i%1,7),mydata[index][0]

    f=open(os.path.join(BASE_DIR,'patterns',str(N)+'.py'),'w')
    f.write('pattern_zero='+str(pattern_0))
    f.write('\n')
    f.write('pattern_odd='+str(pattern_1))
    f.write('\n')
    if N%2==0:
        f.write('pattern_even='+str(pattern_1))
        f.write('\n')
    else:
        f.write('pattern_even='+str(pattern_2))
        f.write('\n')
    f.write('averages_even='+str(averages_even))
    f.write('\n')
    f.write('averages_odd='+str(averages_odd))
    f.close()





