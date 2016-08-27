import math
import re

## this is a stand alone function for variances along with code for testing
## I realize variables are labeled "sd" or "std" instead of "var"
## if it bothers you change it

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
    if lower<0:
        lower=0
    higher=sd+.5/(10**sd_decimals)    
    low=math.floor(lower)
    high=math.ceil(higher)
    sample_count=0
    population_count=0
    if Type!='Sample':
        possibilities=loop(low,high)
        if grim:
            for j in possibilities:
##                print j
                if int(j[0])==0:
                    if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [round_up(ave,mean_decimals) for ave in averages_zero[j[1]][1]]:
                        if round_up(j[0],sd_decimals)==sd:
                            population_count+=1
                elif int(j[0])%2==0:
                    if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [round_up(ave,mean_decimals) for ave in averages_even[j[1]][1]]:
                        if round_up(j[0],sd_decimals)==sd:
                            population_count+=1
                else:
                    if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [round_up(ave,mean_decimals) for ave in averages_odd[j[1]][1]]:
                        if round_up(j[0],sd_decimals)==sd:
                            population_count+=1
        else:
            for j in possibilities:
                if round_up(j[0],sd_decimals)==sd:
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
                        if round_up(j[0]*size/(size-1),sd_decimals)==sd:
                            sample_count+=1
                        else:
                            if round_up(round(j[0]*size/(size-1),10),sd_decimals)==sd:
                                sample_count+=1
                elif int(j[0])%2==0:
                    if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [round_up(ave,mean_decimals) for ave in averages_even[j[1]][1]]:
                        if round_up(j[0]*size/(size-1),sd_decimals)==sd:
                            sample_count+=1
                        else:
                            if round_up(round(j[0]*size/(size-1),10),sd_decimals)==sd:
                                sample_count+=1
                else:
                    if round_up('.'+repr(mean).split('.')[1],mean_decimals) in [round_up(ave,mean_decimals) for ave in averages_odd[j[1]][1]]:
                        if round_up(j[0]*size/(size-1),sd_decimals)==sd:
                            sample_count+=1
                        else:
                            if round_up(round(j[0]*size/(size-1),10),sd_decimals)==sd:
                                sample_count+=1
        else:
            for j in possibilities:
                if round_up(round(j[0]*size/(size-1),10),sd_decimals)==sd:
                    sample_count+=1
    if mean:
        return sample_count,population_count
    else:
        return sample_count,population_count


#thorough testing
std_places=2
ave_places=2

for r in range(5,100):
    import importlib
    mod = importlib.import_module('patterns.'+str(r))
    global_pattern_zero=mod.pattern_zero[:]
    global_pattern_even=mod.pattern_even[:]
    global_pattern_odd=mod.pattern_odd[:]
    global_averages_even=mod.averages_even.copy()
    global_averages_odd=mod.averages_odd.copy()
    global_pattern_zero_rounded=[round_up('.'+repr(n).split('.')[1],5) for n in global_pattern_zero]
    global_averages_zero={round_up('.'+repr(n).split('.')[1],5):global_averages_even[n] for n in global_averages_even if round_up('.'+repr(n).split('.')[1],5) in global_pattern_zero_rounded}
    test=global_pattern_zero[:]
    for n in range(1,3):
        if n%2==0:
            for value in global_pattern_even:
                test.append(value+n)
        else:
            for value in global_pattern_odd:
                test.append(value+n)
    print r, len(test),test[-1]
    pattern_zero=mod.pattern_zero[:]
    pattern_even=mod.pattern_even[:]
    pattern_odd=mod.pattern_odd[:]
    averages_even=mod.averages_even.copy()
    averages_odd=mod.averages_odd.copy()
    pattern_zero_rounded=[round_up('.'+repr(n).split('.')[1],5) for n in pattern_zero]
    averages_zero={round_up('.'+repr(n).split('.')[1],5):averages_even[n] for n in averages_even if round_up('.'+repr(n).split('.')[1],5) in pattern_zero_rounded}
    for i in test:
        #for 'Population':
##        std=round_up(i,std_places)
        ##for 'Sample':
        std=round_up(i*float(r)/(r-1),std_places)
        if int(i)==0:
            ave=round_up(repr(global_averages_zero[round_up('.'+repr(i).split('.')[1],5)][0]),ave_places)
        elif int(i)%2==0:
            ave=round_up(repr(global_averages_even[round_up('.'+repr(i).split('.')[1],var_precision)][0]),ave_places)
        else:
            ave=round_up(repr(global_averages_odd[round_up('.'+repr(i).split('.')[1],var_precision)][0]),ave_places)
        ##for 'Population'
##        if grimmer(std,std_places,r,'Population',ave,ave_places)[1]!=1:
##            print i,std,ave,r,low,high,grimmer(std,std_places,r,'Population',ave,ave_places)

        ##for 'Sample':
        if grimmer(std,std_places,r,'Sample',ave,ave_places)[0]!=1:
            print i,std,ave,r,low,high,grimmer(std,std_places,r,'Sample',ave,ave_places)


######random testing
import random
def variance(data,u):
        return sum([(i-u)**2 for i in data])/len(data)

##for r in range(5,100):
##    print r
##    std_places=2
##    ave_places=2
##    for i in range(100):
##        test=[random.randint(0,10) for k in range(r)]
##        mean=round_up(sum(test)/float(len(test)),ave_places)
##        true_mean=round_up(sum(test)/float(len(test)),16)
##        #for 'Population':
##        std=round_up(variance(test,true_mean),std_places)
##        if grimmer(std,std_places,r,'Population',mean,ave_places)[1]<1:
##            print grimmer(std,std_places,r,'Population',mean,ave_places),test
##        print grimmer(std,std_places,r,'Population',mean,ave_places),std,mean

        #for 'Sample'
##        std=round_up((variance(test,true_mean)*len(test)/(len(test)-1)),std_places)
##        if grimmer(std,std_places,r,'Sample',mean,ave_places)[0]<1:
##            print grimmer(std,std_places,r,'Sample',mean,ave_places),std,mean,test
##            print grimmer(std,std_places,r,'Sample',mean,ave_places),std,mean

        


