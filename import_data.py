import pandas as pd
import os 
cols=['taster','beer','aroma hop','maltiness','fruity estery','sweetness','bitterness','body','aftertaste']
df=pd.read_clipboard()
df.columns=cols
filename=os.path.join(os.getcwd(),'_data','sensory_data.pkl')
df.to_pickle(filename)
print(df.head())
