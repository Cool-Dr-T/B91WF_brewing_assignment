import pandas as pd
import matplotlib.pyplot as plt
from math import pi
import os

filename=os.path.join(os.getcwd(),'_data','sensory_data.pkl')
df=pd.read_pickle(filename)
print(df.head())

# from http://medialab.github.io/iwanthue/ - colourblind friendly colours...
reference_colour="#699298"
pretty_colours=["#ff8fb5","#d09c00","#5b4789","#01bde8"]

samples=[111,402,727,917]

sample_number=111

sample=df[df['beer']==sample_number]
print(sample.describe())
mean_values=sample.mean().tolist()[2:] # removing the first two columns here just for ease of use 'taster' and 'beer'
 
# number of variable
categories=df.columns[2:]
print('plotting radar plot for: {}'.format(categories))
N = len(categories)
 
# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
fig = plt.figure(figsize=(10,10))

for i, beer in enumerate(samples):
    c_plot=pretty_colours[i]
    sample=df[df['beer']==beer]
    mean_values=sample.mean().tolist()[2:] # removing the first two columns here just for ease of use 'taster' and 'beer'
    # Initialise the spider plot
    ax = plt.subplot(2,2,i+1, polar=True)
    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
 
    # Draw one axe per variable + add labels labels yet
    #set title
    ax.set_title('beer sample: {}'.format(beer))
    ax.set_xticks(ticks=angles[:-1])
    ax.set_xticklabels(labels=categories)
 
    # Draw ylabels and and set limits
    ax.set_rlabel_position(0)
    ax.set_yticks(ticks=[1,2,3,4,5])
    ax.set_yticklabels(["1","2","3","4","5"])
    ax.set_ylim(0,6)
    # ------- PART 2: Add plots
    # Plot each individual = each line of the data 
    # control - using original dataframe here (not really safe)
    values=df.loc[0].drop(['taster','beer']).values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="control", color=reference_colour)
    ax.fill(angles, values, color=reference_colour, alpha=0.1)
    # sample
    mean_values += mean_values[:1]
    ax.plot(angles, mean_values,color=c_plot, linewidth=1, linestyle='solid', label='sample: {}'.format(beer))
    ax.fill(angles, mean_values, color=c_plot, alpha=0.1)

plt.subplots_adjust(wspace=0.4,hspace=0.2)
filename_pic=os.path.join(os.getcwd(),'_output','simple_radar_sample_all.png')
plt.savefig(filename_pic,bbox_inches='tight')
plt.show()
