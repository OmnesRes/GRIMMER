## Load necessary modules
import pylab as plt
import numpy as np




f=open('for_figure2.txt')
data=[eval(i.strip()) for i in f]
mydata=[]
for i in data:
    mydata.append(i[0])


##plot the data with pylab
fig=plt.figure(figsize=(22.62372, 6))  
ax = fig.add_subplot(111)
fig.subplots_adjust(bottom=.18)

ax.bar([index[0] for index in enumerate(mydata)],[i for i in mydata],color='r',width=1.0,linewidth=2.0)
ax.set_xticks([i for i in range(96)])
ax.set_xticklabels([str(i) for i in range(5,100)],rotation=270)
ax.tick_params(axis='y',length=0,width=0,direction='out',labelsize=20)
ax.tick_params(axis='x',length=0,labelsize=12,pad=5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_position(['outward',0])
ax.yaxis.set_ticks_position('left')
ax.set_xticks([i+.5 for i in range(96)])
ax.set_xticklabels([str(i) for i in range(5,100)],rotation=270)
ax.set_ylabel('Percent of Inconsistencies',fontsize=30,labelpad=20)
ax.set_xlabel('Sample Size',fontsize=30,labelpad=20)
ax.set_xlim(0,95)
plt.savefig('figure2.pdf')
plt.show()
