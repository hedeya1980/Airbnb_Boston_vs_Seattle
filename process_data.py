import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import seaborn as sns

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def load_data(boston_filepath, seattle_filepath):
    # load Boston dataset
    boston = pd.read_csv(boston_filepath)
    boston['Dataset']='Boston'
    # load Seattle dataset
    seattle = pd.read_csv(seattle_filepath)
    seattle['Dataset']='Seattle'
    # merge datasets
    for col in boston:
        if col not in seattle.columns:
            #print(col)
            boston.drop(columns=col, inplace=True)
    for col in seattle:
        if col not in boston.columns:
            #print(col)
            seattle.drop(columns=col, inplace=True)
    df = pd.concat([boston, seattle], axis=0)
    return df

def null_columns(df, show=True, drop_threshold=0.98):
    null_percent=pd.DataFrame(df.isnull().sum()/df.shape[0]).reset_index()
    null_percent.columns=['Col. Name', 'Null Percent']
    null_percent.sort_values('Null Percent', ascending=False, inplace=True)
    col_to_drop=list(null_percent[null_percent['Null Percent']>drop_threshold]['Col. Name'])
    if show:
        print(null_percent)
    
    return col_to_drop
    
def clean_listings_data(df):
    
    cat_cols=df.select_dtypes(exclude=['int64', 'float64']).columns # Categorical columns
    
    # Replace 't', 'f' with 1, 0
    for col in cat_cols:
        if {'t', 'f'}.issubset(set(df[col].unique())):
            df[col].replace({'t':1, 'f':0}, inplace=True)

    # Convert rates from string to float
    rate_cols=df.columns[df.columns.str.contains('rate')]
    df[rate_cols]=df[rate_cols].apply(lambda x: x.str.replace('%', '').astype(float)/100)
    df[rate_cols].head()
    
    # Drop some columns (these columns were having only 1 unique value in each of the 2 cities datasets, and 'host_total_listings_count' is a duplicate of another column)
    cols_to_drop=['scrape_id',
                 'last_scraped',
                 'experiences_offered',
                 'neighbourhood_group_cleansed',
                 'state',
                 'country_code',
                 'country',
                 'has_availability',
                 'calendar_last_scraped',
                 'requires_license',
                 'license',
                 'jurisdiction_names',
                 'host_total_listings_count',
                 'neighbourhood']
    df.drop(columns=cols_to_drop, inplace=True)
    
    # Rename 'neighbourhood_cleansed' after dropping 'neighbourhood'
    df.rename(columns={'neighbourhood_cleansed':'neighbourhood'}, inplace=True)
    
    # Drop columns with null values more than 98%
    df.drop(columns=null_columns(df, show=False, drop_threshold=0.95), inplace=True)
    
    # Convert Price columns to 'float' instead of 'Object'
    price_columns=[]
    for col in list(df.select_dtypes(exclude=['int64', 'float64']).columns):
        if df[col].str.contains('$', regex=False).any():
            if not df[col].str.contains('[A-Za-z]', regex=True).any():
                price_columns.append(col)
    df[price_columns]=df[price_columns].apply(lambda x:x.str.replace('[$, ]','', regex=True)).astype(float)
    
    # Create a new feature 'price_per_accommodate'
    df['price_per_accommodate']=df['price']/df['accommodates']
    
    # Split Amenities into separate columns
    df['amenities'] = df['amenities'].str.replace('[{}"]','', regex=True)
    amenities = df['amenities'].str.get_dummies(sep=',')
    df.drop(columns='amenities')
    df=pd.concat([df, amenities], axis=1)
        
    return df

def clean_calendars_data(df):
    
    # Perform datatype conversions
    df['date']=pd.to_datetime(df['date'])
    df['price']=df['price'].str.replace('[$, ]','', regex=True).astype(float)
    df['available'].replace({'t':1, 'f':0}, inplace=True)
    
    # Add new features
    df['month']=df.date.dt.month
    df['month_name']=df.date.dt.month_name()
    df['year']=df.date.dt.year
    df['month-year']=df.date.dt.strftime('%m-%Y')
    
    return df

def save_data(df, database_filename, table_name):
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql(table_name, engine, index=False, if_exists='replace')
    
def main():
    if len(sys.argv) == 5:

        boston_filepath, seattle_filepath, database_filepath, table_name = sys.argv[1:]

        print('Loading data...\n    Boston: {}\n    Seattle: {}'
              .format(boston_filepath, seattle_filepath))
        df = load_data(boston_filepath, seattle_filepath)

        print('Cleaning data...')
        if boston_filepath.split('.')[0].find('listing')>0:
            df = clean_listings_data(df)
        elif boston_filepath.split('.')[0].find('calendar')>0:
            df = clean_calendars_data(df)
        
        print('Saving data...\n    DATABASE: {}/{}'.format(database_filepath, table_name))
        save_data(df, database_filepath, table_name)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the "Boston" and "Seattle" '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument, and the table name as the fourth argument.'\
              '\n\nExample: python process_data.py '\
              'Boston/listings.csv Seattle/listings.csv '\
              'BostonSeattle.db cleanedListings')


if __name__ == '__main__':
    main()