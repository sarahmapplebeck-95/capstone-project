#%%
#import sys and check have directories we need
import sys
#insert data directiry into file path
sys.path.insert(0,'/Users/SarahMapplebeck/Documents/Digital_Futures/project/data')
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
from spellchecker import SpellChecker

#%%
#define the latest file (one that needs modifying) and second latest file(one previously modified)
latest_file, second_latest_file = funcs.get_new_and_second_files('data/*.csv')

#check correct files
print(latest_file,second_latest_file)
#%%
#readin the csvs
latest_df=pd.read_csv(latest_file)
second_latest_df=pd.read_csv(second_latest_file)

#view df to modify
latest_df.head()

print(latest_df.dtypes, second_latest_df.dtypes)
#%%
#rename untitled to index and set as index

latest_df.set_index('ID', verify_integrity=True, inplace=True)
second_latest_df.set_index('ID', verify_integrity=True, inplace=True)

#view
second_latest_df.head()
#%%
#capitalise the first letter of each title word (except of etc) and
# remove special characters from column names
columns= funcs.titlecase(latest_df.columns)

#reset column names as newly defined columns
latest_df.columns=columns

#view df
latest_df.head()
#%%
latest_df.columns
#%% md
## Drop Irrelevant columns and ones containing >40% nulls
#%%
#drop irrelevant columns - don't need location data as contained in corresponding geo columns
#Don't need description of injury /COD - all drug overdose deaths and have columns to say which drug
#Datetype removed as irrelevant if date is the date of death or the date recorded - looking at annual figures
irrel_cols=['Unnamed0','DateType','DeathCity','ResidenceCity','InjuryCity','ResidenceCounty','ResidenceState','DeathCounty','DescriptionofInjury', 'COD']


cols_to_drop=[i for i in irrel_cols if i in latest_df.columns]

latest_df.drop(cols_to_drop,axis=1,inplace=True)

#view columns to see if dropped
latest_df.columns
#%%
#drop columns if they contain > 40% nulls
latest_df=funcs.remove_nulls_cols(40,latest_df)

#%% md
# Data Types


#%%
#view data types
latest_df.dtypes
#%%
# Remove nulls from date column
null_list = ['null', 'na', '<na>', 'n/a', 'none', 'nan']
latest_df.Date = latest_df.Date.astype('str')

#return the df with date values that do ot contain the values in null list matched with case insenitivity
latest_df = latest_df[~latest_df['Date'].str.contains('|'.join(null_list).casefold())]

#Convert to date type
latest_df['Date'] = pd.to_datetime(latest_df['Date'])
second_latest_df['Date']=pd.to_datetime(second_latest_df['Date'])


#%%
#Define lists of column dtypes to convert

binary_cols=['Heroin','Cocaine','Fentanyl','FentanylAnalogue','Oxycodone','Oxymorphone','Ethanol','Hydrocodone','Benzodiazepine','Methadone','Amphet','Tramad','MorphineNotHeroin','Hydromorphone','OpiateNOS','AnyOpioid']
binary_cols=[i for i in binary_cols if i in latest_df.columns]
string_cols=['Sex','Race','Location','InjuryPlace','MannerofDeath','DeathCityGeo','ResidenceCityGeo','InjuryCityGeo']
#%%
#remove other types of data from binary columns
latest_df=funcs.format_binary_cols(binary_cols,latest_df)
#%%
#Convert binary to int8 for less storage used
latest_df[binary_cols]=latest_df[binary_cols].astype('int8')
second_latest_df[binary_cols]=second_latest_df[binary_cols].astype('int8')

#Convert string style columns to string type
for i in string_cols:
    latest_df[i]=pd.Series(latest_df[i], dtype='string')
    second_latest_df[i]=pd.Series(second_latest_df[i], dtype='string')

#%%
#Replace nulls in age by the average age of death, grouped by year
#average death age by year
latest_df['Age']=latest_df.groupby(latest_df.Date.dt.year)['Age'].apply(lambda x: x.fillna(round(x.mean())) )
#%%
#show percent nulls for each column remaining
funcs.percent_missing(latest_df)
#%%
#apply function to remove rows from data frame if the columns contain less than n nulls
latest_df=funcs.remove_null_rows(4,latest_df)
#%%
funcs.percent_missing(latest_df)
#%%
#Reformat the geolocation columns so they just contain the longditude and latitude coordinates
geo_list=['DeathCityGeo','ResidenceCityGeo','InjuryCityGeo']

for i in geo_list:
    latest_df[i] = latest_df[i].apply(lambda x: funcs.remove_not_in_brackets(x))

latest_df[geo_list]
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
    latest_df[i]=latest_df[i].apply(lambda x: correct(x))
#%%
#format all string columns so that they are in title case
funcs.format_string_cols(string_cols,latest_df)
#%%
#capitalise the first letter of each title word (except of etc) and
# remove special characters from column names
columns= funcs.titlecase(latest_df.columns)

#reset column names as newly defined columns
latest_df.columns=columns

#view df
latest_df.head()
#%%
#Check title case and no misspelled values
latest_df.groupby(latest_df.Location)['Location'].count().sort_values(ascending=False)
#%%
#list of dfs to append
dfs = [second_latest_df,latest_df]

#comapre the column headings of both dfs - if not same, make
# them so by dropping relevant columns so can append dfs

if all([set(dfs[0].columns) == set(df.columns) for df in dfs]):
    pass
else:
    #list of matching columns from both dfs
    matching_cols=[x for x in list(latest_df.columns) if x in list(second_latest_df.columns)]

    #create list of columns that don't match between both dfs
    lastest=set(list(latest_df.columns))
    second_latest=set(list(second_latest_df.columns))
    nonmatching1=list(lastest-second_latest)
    nonmatching2=list(second_latest-lastest)
    not_matching_cols=nonmatching1+nonmatching2

    #if column doesn't appear in a df, drop it so they can be appended
    for i in not_matching_cols:
        for df in dfs:
            if i in df.columns:
                df=df.drop([i],axis=1,inplace=True)
            else:
                pass
    #set columns to be the same
    latest_df.columns=matching_cols


#concatonate dfs
new_df = pd.concat(dfs)

#drop dulplicate rows
new_df=new_df.drop_duplicates()

print(f'lines appended = {len(new_df)-len(latest_df)}')
new_df.head()

#%%
#return new file name with counter added on if file name already exsists
newfilename=funcs.unique_file_name('data/drug_deaths_transform.csv')

#write newdf to csv file
new_df.to_csv(newfilename)
