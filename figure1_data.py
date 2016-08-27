import math
import re
##this script generates the data for figure 1, takes a couple days with one core


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



var_precision=12

#use floats for values except for size and Type, size is int Type is either "Sample", "Population", or random string
def grimmer(sd,sd_decimals,size,Type,mean=None,mean_decimals=None):
    global possibilities
    global averages_even
    global averages_odd
    global pattern_even
    global pattern_odd
    global averages_zero
    global low
    global high
    global pattern
    import importlib
    mod = importlib.import_module('patterns.'+str(size))
    pattern_zero=mod.pattern_zero[:]
    pattern_even=mod.pattern_even[:]
    pattern_odd=mod.pattern_odd[:]
    averages_even=sorted(zip(mod.averages_even.copy().keys(),mod.averages_even.copy().values()))
    averages_odd=sorted(zip(mod.averages_odd.copy().keys(),mod.averages_odd.copy().values()))
    pattern_zero_rounded=[round_up('.'+repr(n).split('.')[1],5) for n in pattern_zero]
    averages_zero={round_up('.'+repr(n).split('.')[1],5):mod.averages_even.copy()[n] for n in mod.averages_even.copy() if round_up('.'+repr(n).split('.')[1],5) in pattern_zero_rounded}
    averages_zero=sorted(zip(averages_zero.copy().keys(),averages_zero.copy().values()))
    def loop(low,high):
        possibilities=[]
        if low==0:
            for index,i in enumerate(pattern_zero):
                possibilities.append([i,index])
            low=1
        loop=0
        X=True
        if low%2==0:
            pattern_1=pattern_even
            pattern_2=pattern_odd
        else:
            pattern_1=pattern_odd
            pattern_2=pattern_even
        while True:
            if X==True:
                for index,i in enumerate(pattern_1):
                    value=low+i+loop
                    possibilities.append([value,index])
                    if value>=high:
                        X=False
                        break
                loop+=1
                if X==False:
                    break
                for index,i in enumerate(pattern_2):
                    value=low+i+loop
                    possibilities.append([value,index])
                    if value>=high:
                        X=False
                        break
                loop+=1
            else:
                break
        return possibilities
    if mean==None:
        grim=False
    else:
        if round_up(round_up(mean*size,0)/size,mean_decimals)==mean:
            grim=True
        else:
            return "GRIM failed"
    lower=sd-.5/(10**sd_decimals)
    higher=sd+.5/(10**sd_decimals)    
    low=math.floor(lower**2)
    high=math.ceil(higher**2)
    sample_count=0
    population_count=0
    if Type!='Sample':
        possibilities=loop(low,high)
        if grim:
            for j in possibilities:
##                print j
                if int(j[0])==0:
                    if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [round_up(ave,mean_decimals) for ave in averages_zero[j[1]][1]]:
                        if round_up(j[0]**.5,sd_decimals)==sd:
                            population_count+=1
                elif int(j[0])%2==0:
                    if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [round_up(ave,mean_decimals) for ave in averages_even[j[1]][1]]:
                        if round_up(j[0]**.5,sd_decimals)==sd:
                            population_count+=1
                else:
                    if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [round_up(ave,mean_decimals) for ave in averages_odd[j[1]][1]]:
                        if round_up(j[0]**.5,sd_decimals)==sd:
                            population_count+=1
        else:
            for j in possibilities:
                if round_up(j[0]**.5,sd_decimals)==sd:
                    population_count+=1

    if Type!='Population':
        #recalculate low and high for sample variance
        low=math.floor(low*(size-1)/size)
        high=math.ceil(high*(size-1)/size)
        possibilities=loop(low,high)
        if grim:
            for j in possibilities:
                if int(j[0])==0:
                    if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [round_up(ave,mean_decimals) for ave in averages_zero[j[1]][1]]:
                        if round_up((j[0]*size/(size-1))**.5,sd_decimals)==sd:
                            sample_count+=1
                elif int(j[0])%2==0:
                    if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [round_up(ave,mean_decimals) for ave in averages_even[j[1]][1]]:
                        if round_up((j[0]*size/(size-1))**.5,sd_decimals)==sd:
                            sample_count+=1
                else:
                    if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [round_up(ave,mean_decimals) for ave in averages_odd[j[1]][1]]:
                        if round_up((j[0]*size/(size-1))**.5,sd_decimals)==sd:
                            sample_count+=1
        else:
            for j in possibilities:
                if round_up((j[0]*size/(size-1))**.5,sd_decimals)==sd:
                    sample_count+=1
    return sample_count,population_count




data=[]
for N in range(5,100):
    print N
    index=0
    averages=[round(k/float(N),2) for k in range(N)]
    tempdata=[]
    while index<20:
        count=0
        for i in range(100):
            std=round(index+i/100.0,2)
            for mean in averages:
                if grimmer(std,2,N,'Sample',mean,2)[0]==0:
                    count+=1
        tempdata.append(float(count)/len(averages))
        index+=1
    data.append(tempdata)


f=open('for_figure1.txt','w')
for i in data:
    f.write(str(i))
    f.write('\n')
f.close()

            
                

