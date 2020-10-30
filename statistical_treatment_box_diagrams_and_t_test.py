import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os

# import data from pickle file - from sensory profile data sheet
filename=os.path.join(os.getcwd(),'_data','sensory_data.pkl')
df=pd.read_pickle(filename)
# print basic statistical data
print(df.describe())
# extract sensory profile categories from dataframe
sensory_parameters=df.columns[2:]
print('{} sensory parameters evaluated'.format(len(sensory_parameters)))

# strip out the control sample for plotting below, store it as a reference ('ref')
samples=df[df['beer']!=0]
ref=df[df['beer']==0]
sample_names=samples['beer'].unique() # sample names for plotting
# create list of control value
control_means=[]

# build figure and create a boxplot of all sensory profile parameters
fig = plt.figure(figsize=(10, 10))
for i, col in enumerate(sensory_parameters,3):
    ax=fig.add_subplot(3,3,i)
    value_ref=ref[col].mean()
    control_means.append(value_ref)
    samples.boxplot(column=col,by='beer',ax=ax,grid=False)
    ax.axhline(value_ref,c='r')
    ax.set_ylim((0,6))

control_arr=np.array(control_means)
# finally create a histogram for all of them and plot standard deviations for all
width=0.15 # bar width
x=np.arange(len(sensory_parameters)) # x-axis for bar chart
# collect means and standard deviations from the input data as lists 
means=[]
stds=[]
# melt the imported data into one data frame to process into the means and stds lists above
md=pd.melt(samples,id_vars=['beer'],value_vars=sensory_parameters, var_name='sensory',value_name='score')
for beer in sample_names:
    beer_md=md[md['beer']==beer]
    for s in sensory_parameters:
        means.append(beer_md[beer_md['sensory']==s].mean().values[1])
        stds.append(beer_md[beer_md['sensory']==s].std().values[1])

# split the means and standard deviations into a series of lists to put them on the graph        
bar_series=np.array_split(means,4)
bar_std_series=np.array_split(stds,4)
# create an ax object that spans two plot spaces in the grid that has been defined and add the data to it as a bar
ax=fig.add_subplot(3,3,(1,2))
for c,bars in enumerate(bar_series):
    ax.bar(x+(c*width),bars,yerr=bar_std_series[c],width=width,label=sample_names[c])

# calculate statistical data
groupb_means=np.array(bar_series[1])
groupb_stds=np.array(bar_std_series[1])
## calculate t statistics
N=10 # samples...
t=(groupb_means-control_arr)/(groupb_stds*np.sqrt(2/N))
degfree=2*N-2
p=1-stats.t.cdf(t,df=degfree)

for n, param in enumerate(sensory_parameters):
    if abs(t[n])>2*p[n]:
        print('statistical difference found in {} data from t-test (t: {:.2f}, p: {:.3f})'.format(param,abs(t[n]),2*p[n]))

# format histogram plot and label
ax.set_title('sample histogram and std. dev.')
ax.set_xticks(x+(0.5*len(sensory_parameters)*width/2))
ax.set_xticklabels(sensory_parameters,fontsize=8)
ax.set_ylim((0,6))
ax.legend(ncol=4,fontsize=6)

# format the whole figure and save it as a separate file
plt.subplots_adjust(wspace=0.2,hspace=0.4)
filename_boxplots=os.path.join(os.getcwd(),'_output','sensory_data_boxplots_and_bar.png')
plt.savefig(filename_boxplots,bbox_inches='tight')
plt.show()


