#%%

#import sys and check have directories we need
import sys
#insert data directiry into file path
sys.path.insert(0,'Users/SarahMapplebeck/Documents/Digital_Futures/project/data')
sys.path.insert(0,'/Users/SarahMapplebeck/Documents/Digital_Futures/project/')

#check it's in there
for p in sys.path:
    print( p )


#%%
#import functions
import Functions as funcs
import pandas as pd
import re
import string
import numpy as np
from spellchecker import SpellChecker
#%%
orig_df=pd.read_csv('data/drug_deaths.csv')

orig_df.head(20)
#%% md
## Fix column headings and set index
#%%
#rename untitled to index and set as index

orig_df.set_index('ID', verify_integrity=True, inplace=True)

#view
orig_df.head()
#%%
#capitalise the first letter of each title word (except of etc) and
# remove special characters from column names
columns= funcs.titlecase(orig_df.columns)

#reset column names as newly defined columns
orig_df.columns=columns

#view df
orig_df.head()
#%% md
## Drop Irrelevant columns and ones containing >40% nulls
#%%
#drop irrelevant columns - don't need location data as contained in corresponding geo columns
#Don't need description of injury /COD - all drug overdose deaths and have columns to say which drug
#Datetype removed as irrelevant if date is the date of death or the date recorded - looking at annual figures
irrel_cols=['Unnamed0','DateType','DeathCity','ResidenceCity','InjuryCity','ResidenceCounty','ResidenceState','DeathCounty','DescriptionofInjury', 'COD']
orig_df.drop(irrel_cols,axis=1,inplace=True)

#view columns to see if dropped
orig_df.columns
#%%
#drop columns if they contain > 40% nulls
orig_df=funcs.remove_nulls_cols(40,orig_df)

#view df
orig_df.head(15)
#%% md
# Data Types


#%%
#view data types
orig_df.dtypes
#%%
# Remove nulls from date column
null_list=['null','na','<na>','n/a','none','nan']
orig_df.Date=orig_df.Date.astype('str')

#return the df with date values that do ot contain the values in null list matched with case insenitivity
orig_df = orig_df[~orig_df['Date'].str.contains('|'.join(null_list).casefold())]

#Convert to date type
orig_df['Date'] = pd.to_datetime(orig_df['Date'])

#%%
#Define lists of column dtypes to convert

binary_cols=['Heroin','Cocaine','Fentanyl','FentanylAnalogue','Oxycodone','Oxymorphone','Ethanol','Hydrocodone','Benzodiazepine','Methadone','Amphet','Tramad','MorphineNotHeroin','Hydromorphone','OpiateNOS','AnyOpioid']

string_cols=['Sex','Race','Location','InjuryPlace','MannerofDeath','DeathCityGeo','ResidenceCityGeo','InjuryCityGeo']
#%%
#remove other types of data from binary columns
orig_df=funcs.format_binary_cols(binary_cols,orig_df)

#checkcolumn known to have more than just 0/1s in it
print(orig_df.groupby(orig_df.MorphineNotHeroin)['MorphineNotHeroin'].count())
#%%
#Convert binary to int8 for less storage used
orig_df[binary_cols]=orig_df[binary_cols].astype('int8')

#Convert string style columns to string type
for i in string_cols:
    orig_df[i]=pd.Series(orig_df[i], dtype='string')
orig_df.dtypes

#%%
#Replace nulls in age by the average age of death, grouped by year
#average death age by year
orig_df['Age']=orig_df.groupby(orig_df.Date.dt.year)['Age'].apply(lambda x: x.fillna(round(x.mean())) )

#%%
#show percent nulls for each column remaining
funcs.percent_missing(orig_df)
#%%
#apply function to remove rows from data frame if the columns contain less than n nulls
orig_df=funcs.remove_null_rows(4,orig_df)
#%%
#check percentage nulls
funcs.percent_missing(orig_df)
#%%
#Reformat the geolocation columns so they just contain the longditude and latitude coordinates
geo_list=['DeathCityGeo','ResidenceCityGeo','InjuryCityGeo']

for i in geo_list:
    orig_df[i] = orig_df[i].apply(lambda x: funcs.remove_not_in_brackets(x))

#view newly formatted geo data
orig_df[geo_list]
#%%
#view percentage numbers
funcs.percent_missing(orig_df)
#%%
#view df
orig_df.head(50)
#%%
#define spellchecking function
spell = SpellChecker(distance=1)
def correct(x):
    return spell.correction(x)
#%%
#spellcheck list of string columns
spell_cols=['Sex','Race','Location','InjuryPlace','MannerofDeath']

#apply spellchecking
spell = SpellChecker(distance=1)
for i in spell_cols:
    orig_df[i]=orig_df[i].apply(lambda x: correct(x))

#%%
#format all string columns so that they are in title case
funcs.format_string_cols(string_cols,orig_df)
#%%
#Check title case and no misspelled values
orig_df.groupby(orig_df.MannerofDeath)['MannerofDeath'].count().sort_values(ascending=False)
#%%
#view
orig_df.head()

#save to csv
orig_df.to_csv('data/drug_deaths_transform_orig.csv')
#%%

#%%
