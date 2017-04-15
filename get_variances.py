from itertools import *
import time
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))



#my own variance function runs much faster than numpy or the Python 3 ported statistics module
def variance(data,u):
    return sum([(i-u)**2 for i in data])/len(data)


##rounding the means and variances helps to collapse them
precision_ave=16
precision_var=12

def run(n,r):
    all_deviations={}
    start=time.clock()
    for i in combinations_with_replacement(range(n), r):
        if n-1 in i:
            u=round(sum(i)/float(len(i)),precision_ave)
            var=round(variance(i,u),precision_var)
            if var not in all_deviations:
                all_deviations[var]={u:''}
            else:
                all_deviations[var][u]=''
    end=time.clock()
    duration=end-start
    data=sorted(all_deviations.keys())
    f=open(os.path.join(BASE_DIR,'raw_variances',str(r)+'.txt'),'w')
    #write a header line that includes time to complete
    f.write(str(n)+' '+str(duration))
    f.write('\n')
    for i in data:
        f.write(str(i))
        f.write('\t')
        f.write(str(sorted(all_deviations[i].keys())))
        f.write('\n')
    f.close()




##perform runs
#n can probably just be set to 7 or even lower
#code will take a while, you should run copies of this script in parallel
for r in range(5,100):
    n=30-r
    if n<=7:
        n=7
    run(n,r)
