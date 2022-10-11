#imports
import glob
import os
import re
import pandas as pd
import numpy as np

#from spellchecker import SpellChecker

def get_new_and_second_files(files_in_path):
  'function to get return the latest and second latest mofified files in a directory'
  #list of files in dir
  list_of_files = glob.iglob(files_in_path)

  #return a list of the files in date order
  files = sorted(list_of_files, key=os.path.getmtime)

  #return the newest and second newest
  latest_file=files[-1]
  second_latest_file=files[-2]
  return latest_file,second_latest_file



def remove_special_chars(s):
  'function to remove special characters and spaces '
  #remove special characters from names and replace with a space
  s=re.sub('[^a-zA-Z0-9\n\.]', '', s)
  return s

def titlecase(columns):
  'function that capitalises the first letter of each word in\
  the column headings and removes any special characters so all column\
   headings are formatted the same'
  df_cols=[]
  #if col heading contains special character capatialise
  #the first letter, keep rest of casing the same, append to list
  for i in columns:
    if not i.isalnum():
      i=i[0].upper() + i[1:]
      df_cols.append(i)
    else:
      i=i
      df_cols.append(i)
  cols=[]
  #remove specoial characters in the column headings
  for i in df_cols:
    i=remove_special_chars(i)
    cols.append(i)
  return cols



#%%
def remove_nulls_cols(null_percent,df):
  'function to drop columns based on the percentage of nulls they contain'
  droplist=[]
  #perecnt nulls
  percent_missing = df.isna().sum() / df.shape[0] * 100.00
  #drop column if percent nulls > null percent
  for index, val in percent_missing.iteritems():
    if val >= null_percent:
      droplist.append(index)
  df=df.drop(droplist,axis=1)
  #print which columns have been dropped
  print('Columns removed:', droplist)
  return df


def remove_null_rows(null_percent,df):
  'function to drop rows based on the percentage of nulls they contain'
  droplist=[]

  #perecnt nulls
  percent_missing = df.isna().sum() / df.shape[0] * 100.00

  #drop row if percent nulls > null percent
  for index, val in percent_missing.iteritems():
    if val > 0 and val<= null_percent:
      indices=df[df[index].isnull()].index.tolist()
      for i in indices:
        if i not in droplist:
          droplist.append(i)
  df=df.drop(index=droplist, axis=0)
  return df
#%%


def format_binary_cols(binary_cols,orig_df):
  'function to remove any extra acharcters from binary columns containing 1/0,\
  as well as convert Y/Ns to 1/0s and remove any rows with no 1/0s'

  #groupby values in binary columns
  for i in binary_cols:
    check=orig_df.groupby(i)[i].count()

    #if >2 tyoes of value perform reformatting - replacing values and droppping
    if check.shape[0] >2:
      orig_df[i]=pd.Series(orig_df[i], dtype="string")
      orig_df[i]=orig_df[i].str.replace('^.*[1].*$','1', regex=True)
      orig_df[i]=orig_df[i].str.replace('^.*[0].*$','0', regex=True)
      orig_df[i]=orig_df[i].str.replace('^.*[Y].*$','1', regex=True)
      orig_df[i]=orig_df[i].str.replace('^.*[N].*$','0', regex=True)

      droplist=[]
      droplist.append(orig_df[~orig_df[i].str.contains('^[01]*$', regex=True)].index)
      for i in droplist:
        orig_df=orig_df.drop(index=i)

  return orig_df


def percent_missing(df):
  'function to return the percentage of null values in each column'
  percent_missing=df.isna().sum() / df.shape[0] * 100.00
  return 'Percent nulls in each column:', percent_missing


def remove_not_in_brackets(s):
  'function to remove any characters outside of brackets, then\
   remove any brackets or apostrophies'
  s=re.findall('\(.*?\)',s)
  s=str(s).replace('[','').replace(']','').replace('(','').replace(')','').replace('\'','')
  return s
#%%

def format_string_cols(col_list,df):
  for i in col_list:
    df[i]=df[i].str.title()
  return df



def unique_file_name(path):
  'function to add 1 to new file name if filename already exists'

  #split path into the filename and is extension
  filename, extension = os.path.splitext(path)
  counter = 1

  #while the path exists, filename is filename+counter+extension
  while os.path.exists(path):
    path = filename + str(counter) + extension
    counter += 1

  return path

