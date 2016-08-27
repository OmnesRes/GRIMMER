import pylab as plt
import numpy as np



##I did not write this function, from http://depts.washington.edu/clawpack/clawpack-4.6.3/python/pyclaw/plotters/colormaps.py
def make_colormap(colors):
##-------------------------
    """
    Define a new color map based on values specified in the dictionary
    colors, where colors[z] is the color that value z should be mapped to,
    with linear interpolation between the given values of z.

    The z values (dictionary keys) are real numbers and the values
    colors[z] can be either an RGB list, e.g. [1,0,0] for red, or an
    html hex string, e.g. "#ff0000" for red.
    """

    from matplotlib.colors import LinearSegmentedColormap, ColorConverter
    from numpy import sort
    
    z = sort(colors.keys())
    n = len(z)
    z1 = min(z)
    zn = max(z)
    x0 = (z - z1) / (zn - z1)
    
    CC = ColorConverter()
    R = []
    G = []
    B = []
    for i in range(n):
        #i'th color at level z[i]:
        Ci = colors[z[i]]      
        if type(Ci) == str:
            # a hex string of form '#ff0000' for example (for red)
            RGB = CC.to_rgb(Ci)
        else:
            # assume it's an RGB triple already:
            RGB = Ci
        R.append(RGB[0])
        G.append(RGB[1])
        B.append(RGB[2])

    cmap_dict = {}
    cmap_dict['red'] = [(x0[i],R[i],R[i]) for i in range(len(R))]
    cmap_dict['green'] = [(x0[i],G[i],G[i]) for i in range(len(G))]
    cmap_dict['blue'] = [(x0[i],B[i],B[i]) for i in range(len(B))]
    mymap = LinearSegmentedColormap('mymap',cmap_dict)
    return mymap



f=open('for_figure1.txt')
data=[eval(i.strip()) for i in f]
Z=np.rot90(np.array(data),k=1)
fig=plt.figure(figsize=(22.62372, 12))
fig.subplots_adjust(bottom=0.15)
ax=fig.add_subplot(111,)
reds = make_colormap({0:'w',.3:'#ff4d4d',1:'#4d0000'})
figure=ax.imshow(Z,cmap=reds ,interpolation="nearest")
cbar=fig.colorbar(figure,pad=.02,fraction=.0105)
cbar.ax.tick_params(labelsize=20)
cbar.set_label('Percent of Inconsistencies',fontsize=20,labelpad=25,rotation=270)
ax.set_xticks([i for i in range(96)])
ax.set_xticklabels([str(i) for i in range(5,100)],rotation=270)
ax.set_yticks([i for i in range(0,20)])
ax.set_yticklabels(['0-1','1-2','2-3','3-4','4-5','5-6','6-7','7-8','8-9','9-10','10-11','11-12','12-13','13-14','14-15','15-16','16-17','17-18','18-19','19-20'][::-1])
ax.set_ylabel('Standard Deviations',fontsize=25,labelpad=15)
ax.set_xlabel('Sample Size',fontsize=30,labelpad=10)
ax.tick_params(axis='x',length=0,labelsize=12,pad=5)
ax.tick_params(axis='y',length=0,width=0)
ax.set_xlim(-.5,94.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)



##plt.savefig('figure1.pdf')
plt.savefig('figure1.png',dpi=300)
plt.show()
